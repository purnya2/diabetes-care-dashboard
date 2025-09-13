# controller/patient_callbacks.py
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table
from flask_login import current_user
from pony.orm import db_session
from datetime import datetime, timedelta

from model import (
    get_patient_by_user_id, add_glucose_reading, get_patient_glucose_readings,
    add_symptom, record_medication_intake, get_patient_active_therapies,
    get_unread_alerts, check_glucose_alerts
)
from view.patient_dashboard import (
    get_log_data_tab, get_therapies_tab, get_alerts_tab
)

def register_patient_callbacks(app):
    """Register patient dashboard callbacks"""
    
    # Tab content callback
    @app.callback(
        Output('patient-tab-content', 'children'),
        Input('patient-tabs', 'active_tab')
    )
    def update_patient_tab_content(active_tab):
        if active_tab == "log-data":
            return get_log_data_tab()
        elif active_tab == "therapies":
            return get_therapies_tab()
        elif active_tab == "alerts":
            return get_alerts_tab()
        return html.Div("Select a tab")
    
    # Update dashboard stats
    @app.callback(
        [Output('latest-glucose-value', 'children'),
         Output('active-therapies-count', 'children'),
         Output('week-avg-glucose', 'children'),
         Output('unread-alerts-count', 'children')],
        Input('url', 'pathname')
    )
    @db_session
    def update_patient_stats(pathname):
        if not current_user.is_authenticated or current_user.role != 'patient':
            return "--", "--", "--", "--"
        
        patient = get_patient_by_user_id(current_user.id)
        if not patient:
            return "--", "--", "--", "--"
        
        # Latest glucose reading
        recent_readings = get_patient_glucose_readings(patient.id, days=1)
        latest_glucose = recent_readings[-1].value if recent_readings else "--"
        
        # Active therapies count
        active_therapies = get_patient_active_therapies(patient.id)
        therapies_count = len(active_therapies)
        
        # Week average glucose
        week_readings = get_patient_glucose_readings(patient.id, days=7)
        if week_readings:
            week_avg = round(sum(r.value for r in week_readings) / len(week_readings), 1)
        else:
            week_avg = "--"
        
        # Unread alerts
        unread_alerts = get_unread_alerts(patient_id=patient.id)
        alerts_count = len(unread_alerts)
        
        return str(latest_glucose), str(therapies_count), str(week_avg), str(alerts_count)
    
    # Populate therapy dropdown
    @app.callback(
        Output('therapy-select', 'options'),
        Input('patient-tabs', 'active_tab')
    )
    @db_session
    def update_therapy_options(active_tab):
        if not current_user.is_authenticated or current_user.role != 'patient':
            return []
        
        patient = get_patient_by_user_id(current_user.id)
        if not patient:
            return []
        
        active_therapies = get_patient_active_therapies(patient.id)
        return [
            {
                'label': f"{therapy.drug_name} - {therapy.dose_amount}{therapy.dose_unit} x{therapy.daily_doses}/day",
                'value': therapy.id
            }
            for therapy in active_therapies
        ]
    
    # Log glucose reading callback
    @app.callback(
        Output('patient-form-output', 'children', allow_duplicate=True),
        [Input('log-glucose-btn', 'n_clicks')],
        [State('glucose-value', 'value'),
         State('glucose-timing', 'value'),
         State('glucose-notes', 'value')],
        prevent_initial_call=True
    )
    @db_session
    def log_glucose_reading(n_clicks, glucose_value, is_before_meal, notes):
        if not n_clicks or not glucose_value:
            return ""
        
        if not current_user.is_authenticated or current_user.role != 'patient':
            return dbc.Alert("Access denied", color="danger")
        
        patient = get_patient_by_user_id(current_user.id)
        if not patient:
            return dbc.Alert("Patient record not found", color="danger")
        
        # Validate glucose value
        if glucose_value < 30 or glucose_value > 600:
            return dbc.Alert("Please enter a valid glucose value (30-600 mg/dL)", color="warning")
        
        # Add glucose reading
        success = add_glucose_reading(patient.id, glucose_value, is_before_meal, notes)
        
        if success:
            # Check for alerts after adding reading
            check_glucose_alerts(patient.id)
            
            # Determine if reading is concerning
            alert_type = ""
            if is_before_meal and (glucose_value < 80 or glucose_value > 130):
                alert_type = " - Outside normal range for before meals (80-130 mg/dL)"
            elif not is_before_meal and glucose_value > 180:
                alert_type = " - Above recommended level for after meals (<180 mg/dL)"
            
            return dbc.Alert(
                f"Glucose reading logged successfully: {glucose_value} mg/dL{alert_type}",
                color="success" if not alert_type else "warning"
            )
        else:
            return dbc.Alert("Failed to log glucose reading", color="danger")
    
    # Record medication intake callback
    @app.callback(
        Output('patient-form-output', 'children', allow_duplicate=True),
        [Input('record-medication-btn', 'n_clicks')],
        [State('therapy-select', 'value'),
         State('dose-taken', 'value'),
         State('medication-time', 'value'),
         State('medication-notes', 'value')],
        prevent_initial_call=True
    )
    @db_session
    def record_medication(n_clicks, therapy_id, dose_taken, med_time, notes):
        if not n_clicks or not therapy_id or dose_taken is None:
            return ""
        
        if not current_user.is_authenticated or current_user.role != 'patient':
            return dbc.Alert("Access denied", color="danger")
        
        patient = get_patient_by_user_id(current_user.id)
        if not patient:
            return dbc.Alert("Patient record not found", color="danger")
        
        # Record medication intake
        success = record_medication_intake(patient.id, therapy_id, dose_taken, notes)
        
        if success:
            return dbc.Alert("Medication intake recorded successfully", color="success")
        else:
            return dbc.Alert("Failed to record medication intake", color="danger")
    
    # Log symptom callback
    @app.callback(
        Output('patient-form-output', 'children', allow_duplicate=True),
        [Input('log-symptom-btn', 'n_clicks')],
        [State('symptom-name', 'value'),
         State('symptom-severity', 'value'),
         State('symptom-description', 'value')],
        prevent_initial_call=True
    )
    @db_session
    def log_symptom(n_clicks, symptom_name, severity, description):
        if not n_clicks or not symptom_name:
            return ""
        
        if not current_user.is_authenticated or current_user.role != 'patient':
            return dbc.Alert("Access denied", color="danger")
        
        patient = get_patient_by_user_id(current_user.id)
        if not patient:
            return dbc.Alert("Patient record not found", color="danger")
        
        # Add symptom
        success = add_symptom(patient.id, symptom_name, description, severity)
        
        if success:
            return dbc.Alert(f"Symptom '{symptom_name}' logged successfully", color="success")
        else:
            return dbc.Alert("Failed to log symptom", color="danger")
    
    # Active therapies table
    @app.callback(
        Output('active-therapies-table', 'children'),
        Input('patient-tabs', 'active_tab')
    )
    @db_session
    def update_active_therapies(active_tab):
        if active_tab != "therapies":
            return ""
        
        if not current_user.is_authenticated or current_user.role != 'patient':
            return "Access denied"
        
        patient = get_patient_by_user_id(current_user.id)
        if not patient:
            return "Patient record not found"
        
        therapies = get_patient_active_therapies(patient.id)
        
        if not therapies:
            return dbc.Alert("No active therapies prescribed", color="info")
        
        # Create table data
        table_data = []
        for therapy in therapies:
            table_data.append({
                'Medication': therapy.drug_name,
                'Dose': f"{therapy.dose_amount} {therapy.dose_unit}",
                'Frequency': f"{therapy.daily_doses} times/day",
                'Instructions': therapy.instructions or "No special instructions",
                'Start Date': therapy.start_date.strftime('%m/%d/%Y')
            })
        
        return dash_table.DataTable(
            data=table_data,
            columns=[
                {'name': 'Medication', 'id': 'Medication'},
                {'name': 'Dose', 'id': 'Dose'},
                {'name': 'Frequency', 'id': 'Frequency'},
                {'name': 'Instructions', 'id': 'Instructions'},
                {'name': 'Start Date', 'id': 'Start Date'}
            ],
            style_cell={'textAlign': 'left', 'fontSize': '14px'},
            style_header={'backgroundColor': 'lightblue'}
        )
    
    # Patient alerts
    @app.callback(
        Output('patient-alerts-list', 'children'),
        Input('patient-tabs', 'active_tab')
    )
    @db_session
    def update_patient_alerts(active_tab):
        if active_tab != "alerts":
            return ""
        
        if not current_user.is_authenticated or current_user.role != 'patient':
            return "Access denied"
        
        patient = get_patient_by_user_id(current_user.id)
        if not patient:
            return "Patient record not found"
        
        alerts = get_unread_alerts(patient_id=patient.id)
        
        if not alerts:
            return dbc.Alert("No new alerts", color="success")
        
        alert_components = []
        for alert in alerts:
            color_map = {'low': 'info', 'medium': 'warning', 'high': 'danger'}
            color = color_map.get(alert.severity, 'info')
            
            alert_components.append(
                dbc.Alert([
                    html.H6(f"{alert.alert_type.replace('_', ' ').title()}", className="alert-heading"),
                    html.P(alert.message),
                    html.Small(f"Created: {alert.created_at.strftime('%m/%d/%Y %H:%M')}")
                ], color=color, className="mb-2")
            )
        
        return alert_components

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