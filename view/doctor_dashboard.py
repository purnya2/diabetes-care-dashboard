# view/doctor_dashboard.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime, timedelta

def get_doctor_dashboard_layout():
    """Returns the doctor dashboard layout"""
    return html.Div([
        html.H1('Doctor Dashboard', className='mb-4'),
        
        # Quick stats for doctor
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Patients", className="card-title"),
                        html.H2(id="total-patients-count", children="--", className="text-primary"),
                        html.P("under care", className="text-muted")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("High Priority Alerts", className="card-title"),
                        html.H2(id="high-priority-alerts", children="--", className="text-danger"),
                        html.P("require attention", className="text-muted")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Active Therapies", className="card-title"),
                        html.H2(id="total-active-therapies", children="--", className="text-success"),
                        html.P("prescribed", className="text-muted")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Compliance Issues", className="card-title"),
                        html.H2(id="compliance-issues-count", children="--", className="text-warning"),
                        html.P("patients", className="text-muted")
                    ])
                ], color="light")
            ], width=3)
        ], className="mb-4"),
        
        # Navigation tabs for doctor
        dbc.Tabs([
            dbc.Tab(label="Patient List", tab_id="patient-list"),
            dbc.Tab(label="Patient Details", tab_id="patient-details"),
            dbc.Tab(label="Prescribe Therapy", tab_id="prescribe-therapy"),
            dbc.Tab(label="Alerts & Monitoring", tab_id="alerts-monitoring")
        ], id="doctor-tabs", active_tab="patient-list"),
        
        html.Div(id="doctor-tab-content", className="mt-4")
    ])

def get_patient_list_tab():
    """Content for the patient list tab"""
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H4("My Patients"),
                html.Div(id="patients-table")
            ], width=8),
            dbc.Col([
                html.H4("Quick Actions"),
                dbc.Card([
                    dbc.CardBody([
                        dbc.Button("Add New Patient", id="add-patient-btn", color="primary", className="mb-2 w-100"),
                        dbc.Button("View All Alerts", id="view-all-alerts-btn", color="warning", className="mb-2 w-100"),
                        dbc.Button("Export Report", id="export-report-btn", color="info", className="w-100")
                    ])
                ])
            ], width=4)
        ])
    ])

def get_patient_details_tab():
    """Content for the patient details tab"""
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Select Patient"),
                    dbc.CardBody([
                        dbc.Select(
                            id="selected-patient",
                            placeholder="Choose a patient to view details"
                        )
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        html.Div(id="patient-detail-content")
    ])

def get_patient_detail_content():
    """Detailed patient information layout"""
    return html.Div([
        dbc.Row([
            # Patient info card
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Patient Information"),
                    dbc.CardBody([
                        html.Div(id="patient-info-display")
                    ])
                ])
            ], width=4),
            
            # Glucose trend
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Glucose Trend (Last 30 Days)"),
                    dbc.CardBody([
                        dcc.Graph(id="doctor-glucose-chart")
                    ])
                ])
            ], width=8)
        ], className="mb-4"),
        
        dbc.Row([
            # Recent readings
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Glucose Readings"),
                    dbc.CardBody([
                        html.Div(id="doctor-recent-readings")
                    ])
                ])
            ], width=6),
            
            # Medication compliance
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Medication Compliance"),
                    dbc.CardBody([
                        html.Div(id="patient-compliance-info")
                    ])
                ])
            ], width=6)
        ], className="mb-4"),
        
        # Patient management actions
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Update Patient Information"),
                    dbc.CardBody([
                        dbc.Form([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Risk Factors"),
                                    dbc.Textarea(
                                        id="update-risk-factors",
                                        placeholder="smoking, alcohol, obesity, etc.",
                                        rows=2
                                    )
                                ], width=6),
                                dbc.Col([
                                    dbc.Label("Medical History"),
                                    dbc.Textarea(
                                        id="update-medical-history",
                                        placeholder="previous pathologies",
                                        rows=2
                                    )
                                ], width=6)
                            ], className="mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Comorbidities"),
                                    dbc.Textarea(
                                        id="update-comorbidities",
                                        placeholder="hypertension, etc.",
                                        rows=2
                                    )
                                ])
                            ], className="mb-3"),
                            dbc.Button("Update Patient Info", id="update-patient-info-btn", color="primary")
                        ])
                    ])
                ])
            ], width=12)
        ])
    ])

def get_prescribe_therapy_tab():
    """Content for the prescribe therapy tab"""
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Prescribe New Therapy"),
                    dbc.CardBody([
                        dbc.Form([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Select Patient"),
                                    dbc.Select(
                                        id="therapy-patient-select",
                                        placeholder="Choose patient"
                                    )
                                ], width=6),
                                dbc.Col([
                                    dbc.Label("Drug Name"),
                                    dbc.Select(
                                        id="drug-name-select",
                                        options=[
                                            {"label": "Metformin", "value": "Metformin"},
                                            {"label": "Insulin (Rapid-acting)", "value": "Insulin (Rapid-acting)"},
                                            {"label": "Insulin (Long-acting)", "value": "Insulin (Long-acting)"},
                                            {"label": "Glipizide", "value": "Glipizide"},
                                            {"label": "Pioglitazone", "value": "Pioglitazone"},
                                            {"label": "Sitagliptin", "value": "Sitagliptin"},
                                            {"label": "Other", "value": "Other"}
                                        ],
                                        placeholder="Select medication"
                                    )
                                ], width=6)
                            ], className="mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Daily Doses"),
                                    dbc.Input(id="daily-doses", type="number", min=1, max=6, value=1, placeholder="Times per day")
                                ], width=4),
                                dbc.Col([
                                    dbc.Label("Dose Amount"),
                                    dbc.Input(id="dose-amount", type="number", min=0, step=0.1, placeholder="Amount per dose")
                                ], width=4),
                                dbc.Col([
                                    dbc.Label("Unit"),
                                    dbc.Select(
                                        id="dose-unit",
                                        options=[
                                            {"label": "mg", "value": "mg"},
                                            {"label": "IU", "value": "IU"},
                                            {"label": "mL", "value": "mL"},
                                            {"label": "tablets", "value": "tablets"}
                                        ],
                                        value="mg"
                                    )
                                ], width=4)
                            ], className="mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Instructions"),
                                    dbc.Textarea(
                                        id="therapy-instructions",
                                        placeholder="e.g., take with meals, before bedtime, etc.",
                                        rows=3
                                    )
                                ])
                            ], className="mb-3"),
                            dbc.Button("Prescribe Therapy", id="prescribe-therapy-btn", color="success", size="lg")
                        ])
                    ])
                ])
            ], width=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Current Therapies"),
                    dbc.CardBody([
                        html.Div(id="current-patient-therapies")
                    ])
                ])
            ], width=4)
        ]),
        
        # Output for prescription
        html.Div(id="prescribe-therapy-output", className="mt-3")
    ])

def get_alerts_monitoring_tab():
    """Content for the alerts and monitoring tab"""
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H4("Priority Alerts"),
                html.Div(id="priority-alerts-list")
            ], width=6),
            dbc.Col([
                html.H4("Compliance Monitoring"),
                html.Div(id="compliance-monitoring-list")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.H4("Glucose Alerts Summary"),
                html.Div(id="glucose-alerts-summary")
            ], width=12)
        ])
    ])