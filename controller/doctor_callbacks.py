# controller/doctor_callbacks.py
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table
import plotly.graph_objs as go
from flask_login import current_user
from pony.orm import db_session, select
from datetime import datetime, timedelta

from model import (
    get_doctor_by_user_id, Patient, Doctor, add_therapy, 
    get_patient_glucose_readings, get_unread_alerts,
    get_patient_active_therapies, update_patient_info,
    get_therapy_compliance_status
)
from view.doctor_dashboard import (
    get_patient_list_tab, get_patient_details_tab, 
    get_prescribe_therapy_tab, get_alerts_monitoring_tab,
    get_patient_detail_content
)

def register_doctor_callbacks(app):
    """Register doctor dashboard callbacks"""
    
    # Tab content callback
    @app.callback(
        Output('doctor-tab-content', 'children'),
        Input('doctor-tabs', 'active_tab')
    )
    def update_doctor_tab_content(active_tab):
        if active_tab == "patient-list":
            return get_patient_list_tab()
        elif active_tab == "patient-details":
            return get_patient_details_tab()
        elif active_tab == "prescribe-therapy":
            return get_prescribe_therapy_tab()
        elif active_tab == "alerts-monitoring":
            return get_alerts_monitoring_tab()
        return html.Div("Select a tab")
    
    # Update doctor dashboard stats
    @app.callback(
        [Output('total-patients-count', 'children'),
         Output('high-priority-alerts', 'children'),
         Output('total-active-therapies', 'children'),
         Output('compliance-issues-count', 'children')],
        Input('url', 'pathname')
    )
    @db_session
    def update_doctor_stats(pathname):
        if not current_user.is_authenticated or current_user.role != 'doctor':
            return "--", "--", "--", "--"
        
        doctor = get_doctor_by_user_id(current_user.id)
        if not doctor:
            return "--", "--", "--", "--"
        
        # Total patients count
        patients_count = len(doctor.patients)
        
        # High priority alerts
        high_priority_alerts = get_unread_alerts(doctor_id=doctor.id)
        high_priority_count = len([a for a in high_priority_alerts if a.severity == 'high'])
        
        # Total active therapies prescribed by this doctor
        total_therapies = len(doctor.prescribed_therapies)
        
        # Compliance issues - count patients with medication compliance alerts
        compliance_issues = 0
        for patient in doctor.patients:
            patient_alerts = get_unread_alerts(patient_id=patient.id)
            has_compliance_issue = any(
                alert.alert_type in ['medication_compliance', 'patient_non_compliance', 'medication_reminder']
                for alert in patient_alerts
            )
            if has_compliance_issue:
                compliance_issues += 1
        
        return str(patients_count), str(high_priority_count), str(total_therapies), str(compliance_issues)
    
    # Patients table
    @app.callback(
        Output('patients-table', 'children'),
        Input('doctor-tabs', 'active_tab')
    )
    @db_session
    def update_patients_table(active_tab):
        if active_tab != "patient-list":
            return ""
        
        if not current_user.is_authenticated or current_user.role != 'doctor':
            return "Access denied"
        
        doctor = get_doctor_by_user_id(current_user.id)
        if not doctor:
            return "Doctor record not found"
        
        patients = doctor.patients
        
        if not patients:
            return dbc.Alert("No patients assigned", color="info")
        
        # Create table data
        table_data = []
        for patient in patients:
            # Get latest glucose reading
            recent_readings = get_patient_glucose_readings(patient.id, days=1)
            latest_glucose = recent_readings[-1].value if recent_readings else "No data"
            
            # Get active therapies count
            active_therapies = get_patient_active_therapies(patient.id)
            therapies_count = len(active_therapies)
            
            table_data.append({
                'Patient ID': patient.id,
                'Username': patient.user.username,
                'Latest Glucose': str(latest_glucose),
                'Active Therapies': therapies_count,
                'Last Reading': recent_readings[-1].measurement_time.strftime('%m/%d %H:%M') if recent_readings else "No data"
            })
        
        return dash_table.DataTable(
            data=table_data,
            columns=[
                {'name': 'Patient ID', 'id': 'Patient ID'},
                {'name': 'Username', 'id': 'Username'},
                {'name': 'Latest Glucose', 'id': 'Latest Glucose'},
                {'name': 'Active Therapies', 'id': 'Active Therapies'},
                {'name': 'Last Reading', 'id': 'Last Reading'}
            ],
            style_cell={'textAlign': 'left', 'fontSize': '14px'},
            style_header={'backgroundColor': 'lightblue'},
            id='patients-table-component'
        )
    
    # Populate patient dropdown for patient details tab
    @app.callback(
        Output('selected-patient', 'options'),
        Input('doctor-tabs', 'active_tab')
    )
    @db_session
    def update_selected_patient_options(active_tab):
        if active_tab != 'patient-details':
            return dash.no_update
        
        if not current_user.is_authenticated or current_user.role != 'doctor':
            return []
        
        doctor = get_doctor_by_user_id(current_user.id)
        if not doctor:
            return []
        
        options = [
            {
                'label': f"{patient.user.username} (ID: {patient.id})",
                'value': patient.id
            }
            for patient in doctor.patients
        ]
        return options
    
    # Populate patient dropdown for therapy prescription tab
    @app.callback(
        Output('therapy-patient-select', 'options'),
        Input('doctor-tabs', 'active_tab')
    )
    @db_session
    def update_therapy_patient_options(active_tab):
        if active_tab != 'prescribe-therapy':
            return dash.no_update
        
        if not current_user.is_authenticated or current_user.role != 'doctor':
            return []
        
        doctor = get_doctor_by_user_id(current_user.id)
        if not doctor:
            return []
        
        options = [
            {
                'label': f"{patient.user.username} (ID: {patient.id})",
                'value': patient.id
            }
            for patient in doctor.patients
        ]
        return options
    
    # Patient detail content
    @app.callback(
        Output('patient-detail-content', 'children'),
        Input('selected-patient', 'value')
    )
    @db_session
    def update_patient_detail(patient_id):
        if not patient_id:
            return html.Div("Select a patient to view details")
        
        if not current_user.is_authenticated or current_user.role != 'doctor':
            return "Access denied"
        
        return get_patient_detail_content()
    
    # Patient info display
    @app.callback(
        Output('patient-info-display', 'children'),
        Input('selected-patient', 'value')
    )
    @db_session
    def update_patient_info(patient_id):
        if not patient_id:
            return ""
        
        try:
            patient = Patient[patient_id]
            return html.Div([
                html.P(f"Username: {patient.user.username}"),
                html.P(f"Risk Factors: {patient.risk_factors or 'Not specified'}"),
                html.P(f"Medical History: {patient.medical_history or 'Not specified'}"),
                html.P(f"Comorbidities: {patient.comorbidities or 'Not specified'}")
            ])
        except:
            return "Patient not found"
    
    # Patient compliance info
    @app.callback(
        Output('patient-compliance-info', 'children'),
        Input('selected-patient', 'value')
    )
    @db_session
    def update_patient_compliance_info(patient_id):
        if not patient_id:
            return "Select a patient to view compliance information"
        
        try:
            # Get therapy compliance status
            compliance_data = get_therapy_compliance_status(patient_id, days=7)
            
            if not compliance_data:
                return html.P("No active therapies found for this patient")
            
            compliance_items = []
            for therapy_info in compliance_data:
                therapy = therapy_info['therapy']
                compliance_pct = therapy_info['compliance_percentage']
                
                color = "success" if compliance_pct >= 80 else "warning" if compliance_pct >= 60 else "danger"
                
                compliance_items.append(
                    dbc.Card([
                        dbc.CardBody([
                            html.H6(f"{therapy.drug_name}", className="card-title"),
                            html.P(f"Prescribed: {therapy.dose_amount}{therapy.dose_unit}, {therapy.daily_doses}x/day"),
                            html.P(f"Compliance: {compliance_pct:.1f}%", className=f"text-{color}")
                        ])
                    ], className="mb-2")
                )
            
            return compliance_items
            
        except Exception as e:
            return html.P(f"Error loading compliance data: {str(e)}")

    # Doctor glucose chart
    @app.callback(
        Output('doctor-glucose-chart', 'figure'),
        Input('selected-patient', 'value')
    )
    @db_session
    def update_doctor_glucose_chart(patient_id):
        if not patient_id:
            return {}
        
        try:
            readings = get_patient_glucose_readings(patient_id, days=30)
            
            if not readings:
                return {
                    'data': [],
                    'layout': {
                        'title': 'No glucose readings available',
                        'xaxis': {'title': 'Date'},
                        'yaxis': {'title': 'Glucose (mg/dL)'}
                    }
                }
            
            # Separate before and after meal readings
            before_meal_x = []
            before_meal_y = []
            after_meal_x = []
            after_meal_y = []
            
            for reading in readings:
                if reading.is_before_meal:
                    before_meal_x.append(reading.measurement_time)
                    before_meal_y.append(reading.value)
                else:
                    after_meal_x.append(reading.measurement_time)
                    after_meal_y.append(reading.value)
            
            traces = []
            
            if before_meal_x:
                traces.append(go.Scatter(
                    x=before_meal_x,
                    y=before_meal_y,
                    mode='markers+lines',
                    name='Before Meals',
                    marker=dict(color='blue')
                ))
            
            if after_meal_x:
                traces.append(go.Scatter(
                    x=after_meal_x,
                    y=after_meal_y,
                    mode='markers+lines',
                    name='After Meals',
                    marker=dict(color='red')
                ))
            
            return {
                'data': traces,
                'layout': {
                    'title': 'Patient Glucose Trend (Last 30 Days)',
                    'xaxis': {'title': 'Date & Time'},
                    'yaxis': {'title': 'Glucose Level (mg/dL)'},
                    'hovermode': 'closest'
                }
            }
        except:
            return {}
    
    # Recent readings for doctor view
    @app.callback(
        Output('doctor-recent-readings', 'children'),
        Input('selected-patient', 'value')
    )
    @db_session
    def update_doctor_recent_readings(patient_id):
        if not patient_id:
            return ""
        
        try:
            readings = get_patient_glucose_readings(patient_id, days=7)
            recent_readings = readings[-10:] if len(readings) > 10 else readings
            
            if not recent_readings:
                return "No recent readings"
            
            # Create table data
            table_data = []
            for reading in reversed(recent_readings):  # Show most recent first
                status = get_glucose_status(reading.value, reading.is_before_meal)
                table_data.append({
                    'Date & Time': reading.measurement_time.strftime('%m/%d %H:%M'),
                    'Value': f"{reading.value} mg/dL",
                    'Timing': 'Before Meal' if reading.is_before_meal else 'After Meal',
                    'Status': status
                })
            
            return dash_table.DataTable(
                data=table_data,
                columns=[
                    {'name': 'Date & Time', 'id': 'Date & Time'},
                    {'name': 'Value', 'id': 'Value'},
                    {'name': 'Timing', 'id': 'Timing'},
                    {'name': 'Status', 'id': 'Status'}
                ],
                style_cell={'textAlign': 'left', 'fontSize': '12px'},
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{Status} = High'},
                        'backgroundColor': '#ffebee',
                        'color': 'black',
                    },
                    {
                        'if': {'filter_query': '{Status} = Low'},
                        'backgroundColor': '#fff3e0',
                        'color': 'black',
                    }
                ]
            )
        except:
            return "Error loading readings"
    
    # Prescribe therapy callback
    @app.callback(
        Output('prescribe-therapy-output', 'children'),
        [Input('prescribe-therapy-btn', 'n_clicks')],
        [State('therapy-patient-select', 'value'),
         State('drug-name-select', 'value'),
         State('daily-doses', 'value'),
         State('dose-amount', 'value'),
         State('dose-unit', 'value'),
         State('therapy-instructions', 'value')],
        prevent_initial_call=True
    )
    @db_session
    def prescribe_therapy(n_clicks, patient_id, drug_name, daily_doses, dose_amount, dose_unit, instructions):
        if not n_clicks:
            return ""
        
        if not current_user.is_authenticated or current_user.role != 'doctor':
            return dbc.Alert("Access denied", color="danger")
        
        # Validate required fields
        if not patient_id:
            return dbc.Alert("Please select a patient", color="warning")
        if not drug_name:
            return dbc.Alert("Please select a drug name", color="warning")
        if not daily_doses or daily_doses < 1:
            return dbc.Alert("Please enter valid daily doses (minimum 1)", color="warning")
        if not dose_amount or dose_amount <= 0:
            return dbc.Alert("Please enter valid dose amount (greater than 0)", color="warning")
        if not dose_unit:
            return dbc.Alert("Please select a dose unit", color="warning")
        
        doctor = get_doctor_by_user_id(current_user.id)
        if not doctor:
            return dbc.Alert("Doctor record not found", color="danger")
        
        # Add therapy
        success = add_therapy(
            patient_id, doctor.id, drug_name, daily_doses, 
            dose_amount, dose_unit, instructions or ""
        )
        
        if success:
            return dbc.Alert(
                f"Therapy prescribed successfully: {drug_name} {dose_amount}{dose_unit}, {daily_doses} times/day",
                color="success"
            )
        else:
            return dbc.Alert("Failed to prescribe therapy. Please check patient exists and try again.", color="danger")
    
    # Current patient therapies
    @app.callback(
        Output('current-patient-therapies', 'children'),
        Input('therapy-patient-select', 'value')
    )
    @db_session
    def update_current_therapies(patient_id):
        if not patient_id:
            return "Select a patient"
        
        try:
            therapies = get_patient_active_therapies(patient_id)
            
            if not therapies:
                return dbc.Alert("No active therapies", color="info")
            
            therapy_list = []
            for therapy in therapies:
                therapy_list.append(
                    dbc.ListGroupItem([
                        html.H6(therapy.drug_name, className="mb-1"),
                        html.P(f"{therapy.dose_amount} {therapy.dose_unit}, {therapy.daily_doses} times/day", className="mb-1"),
                        html.Small(f"Instructions: {therapy.instructions or 'None'}")
                    ])
                )
            
            return dbc.ListGroup(therapy_list)
        except:
            return "Error loading therapies"
    
    # Priority alerts
    @app.callback(
        Output('priority-alerts-list', 'children'),
        Input('doctor-tabs', 'active_tab')
    )
    @db_session
    def update_priority_alerts(active_tab):
        if active_tab != "alerts-monitoring":
            return ""
        
        if not current_user.is_authenticated or current_user.role != 'doctor':
            return "Access denied"
        
        doctor = get_doctor_by_user_id(current_user.id)
        if not doctor:
            return "Doctor record not found"
        
        alerts = get_unread_alerts(doctor_id=doctor.id)
        priority_alerts = [a for a in alerts if a.severity in ['high', 'medium']]
        
        if not priority_alerts:
            return dbc.Alert("No priority alerts", color="success")
        
        alert_components = []
        for alert in priority_alerts:
            color_map = {'medium': 'warning', 'high': 'danger'}
            color = color_map.get(alert.severity, 'info')
            
            alert_components.append(
                dbc.Alert([
                    html.H6(f"Patient: {alert.patient.user.username}", className="alert-heading"),
                    html.P(alert.message),
                    html.Small(f"Created: {alert.created_at.strftime('%m/%d/%Y %H:%M')}")
                ], color=color, className="mb-2")
            )
        
        return alert_components

    # Update patient info callback
    @app.callback(
        Output('update-patient-output', 'children'),
        [Input('update-patient-info-btn', 'n_clicks')],
        [State('selected-patient', 'value'),
         State('update-risk-factors', 'value'),
         State('update-medical-history', 'value'),
         State('update-comorbidities', 'value'),
         State('update-doctor-notes', 'value')],
        prevent_initial_call=True
    )
    @db_session
    def update_patient_information(n_clicks, selected_patient_id, risk_factors, medical_history, comorbidities, doctor_notes):
        if not n_clicks or not selected_patient_id:
            return ""
        
        if not current_user.is_authenticated or current_user.role != 'doctor':
            return dbc.Alert("Access denied", color="danger")
        
        # Update patient information
        success = update_patient_info(
            selected_patient_id, 
            risk_factors=risk_factors or "", 
            medical_history=medical_history or "", 
            comorbidities=comorbidities or "",
            notes=doctor_notes or ""
        )
        
        if success:
            patient = Patient[selected_patient_id]
            return dbc.Alert(
                f"Patient information updated successfully for {patient.user.username}!", 
                color="success"
            )
        else:
            return dbc.Alert("Failed to update patient information", color="danger")

    # Populate patient info fields when patient is selected
    @app.callback(
        [Output('update-risk-factors', 'value'),
         Output('update-medical-history', 'value'),
         Output('update-comorbidities', 'value')],
        Input('selected-patient', 'value')
    )
    @db_session
    def populate_patient_info_fields(selected_patient_id):
        if not selected_patient_id:
            return "", "", ""
        
        try:
            patient = Patient[selected_patient_id]
            return (
                patient.risk_factors or "",
                patient.medical_history or "",
                patient.comorbidities or ""
            )
        except:
            return "", "", ""

def get_glucose_status(value, is_before_meal):
    """Helper function to determine glucose status"""
    if is_before_meal:
        if value < 80:
            return "Low"
        elif value > 130:
            return "High"
        else:
            return "Normal"
    else:  # after meal
        if value > 180:
            return "High"
        else:
            return "Normal"

'''
    Questo file (doctor_callbacks.py) contiene i callback per la dashboard del dottore.
    Gestisce visualizzazione pazienti, prescrizione terapie, note mediche e monitoraggio compliance.
'''