# view/patient_dashboard.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime, timedelta

def get_patient_dashboard_layout():
    """Returns the patient dashboard layout"""
    return html.Div([
        html.H1('Patient Dashboard', className='mb-4'),
        
        # Quick stats cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Latest Glucose", className="card-title"),
                        html.H2(id="latest-glucose-value", children="--", className="text-primary"),
                        html.P("mg/dL", className="text-muted")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Active Therapies", className="card-title"),
                        html.H2(id="active-therapies-count", children="--", className="text-success"),
                        html.P("prescriptions", className="text-muted")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("This Week Avg", className="card-title"),
                        html.H2(id="week-avg-glucose", children="--", className="text-info"),
                        html.P("mg/dL", className="text-muted")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Alerts", className="card-title"),
                        html.H2(id="unread-alerts-count", children="--", className="text-warning"),
                        html.P("unread", className="text-muted")
                    ])
                ], color="light")
            ], width=3)
        ], className="mb-4"),
        
        # Navigation tabs
        dbc.Tabs([
            dbc.Tab(label="Log Data", tab_id="log-data"),
            dbc.Tab(label="My Therapies", tab_id="therapies"),
            dbc.Tab(label="Alerts", tab_id="alerts")
        ], id="patient-tabs", active_tab="log-data"),
        
        html.Div(id="patient-tab-content", className="mt-4")
    ])

def get_log_data_tab():
    """Content for the log data tab"""
    return html.Div([
        dbc.Row([
            # Glucose reading form
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Log Glucose Reading"),
                    dbc.CardBody([
                        dbc.Form([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Glucose Level (mg/dL)"),
                                    dbc.Input(id="glucose-value", type="number", min=30, max=600, step=0.1, placeholder="Enter glucose level")
                                ], width=6),
                                dbc.Col([
                                    dbc.Label("Measurement Type"),
                                    dbc.Select(
                                        id="glucose-timing",
                                        options=[
                                            {"label": "Before Meal", "value": True},
                                            {"label": "After Meal", "value": False}
                                        ],
                                        value=True
                                    )
                                ], width=6)
                            ], className="mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Notes (optional)"),
                                    dbc.Textarea(id="glucose-notes", placeholder="Any additional notes...", rows=2)
                                ])
                            ], className="mb-3"),
                            dbc.Button("Log Glucose Reading", id="log-glucose-btn", color="primary")
                        ])
                    ])
                ])
            ], width=6),
            
            # Medication intake form
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Record Medication Intake"),
                    dbc.CardBody([
                        dbc.Form([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Select Therapy"),
                                    dbc.Select(
                                        id="therapy-select",
                                        placeholder="Select a prescribed therapy"
                                    )
                                ])
                            ], className="mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Dose Taken"),
                                    dbc.Input(id="dose-taken", type="number", min=0, step=0.1, placeholder="Amount taken")
                                ], width=6),
                                dbc.Col([
                                    dbc.Label("Time"),
                                    dbc.Input(id="medication-time", type="time", value=datetime.now().strftime("%H:%M"))
                                ], width=6)
                            ], className="mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Notes (optional)"),
                                    dbc.Textarea(id="medication-notes", placeholder="Any notes about this intake...", rows=2)
                                ])
                            ], className="mb-3"),
                            dbc.Button("Record Intake", id="record-medication-btn", color="success")
                        ])
                    ])
                ])
            ], width=6)
        ], className="mb-4"),
        
        # Symptom logging
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Log Symptoms"),
                    dbc.CardBody([
                        dbc.Form([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Symptom"),
                                    dbc.Select(
                                        id="symptom-name",
                                        options=[
                                            {"label": "Fatigue", "value": "fatigue"},
                                            {"label": "Nausea", "value": "nausea"},
                                            {"label": "Headache", "value": "headache"},
                                            {"label": "Dizziness", "value": "dizziness"},
                                            {"label": "Blurred Vision", "value": "blurred_vision"},
                                            {"label": "Excessive Thirst", "value": "excessive_thirst"},
                                            {"label": "Frequent Urination", "value": "frequent_urination"},
                                            {"label": "Other", "value": "other"}
                                        ],
                                        placeholder="Select symptom"
                                    )
                                ], width=4),
                                dbc.Col([
                                    dbc.Label("Severity"),
                                    dbc.Select(
                                        id="symptom-severity",
                                        options=[
                                            {"label": "Mild", "value": "mild"},
                                            {"label": "Moderate", "value": "moderate"},
                                            {"label": "Severe", "value": "severe"}
                                        ],
                                        value="mild"
                                    )
                                ], width=4),
                                dbc.Col([
                                    dbc.Label("Duration (if ongoing)"),
                                    dbc.Input(id="symptom-duration", placeholder="e.g., '2 hours', 'since morning'")
                                ], width=4)
                            ], className="mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Description"),
                                    dbc.Textarea(id="symptom-description", placeholder="Describe the symptom...", rows=2)
                                ])
                            ], className="mb-3"),
                            dbc.Button("Log Symptom", id="log-symptom-btn", color="warning")
                        ])
                    ])
                ])
            ], width=12)
        ]),
        
        # Output for form submissions
        html.Div(id="patient-form-output", className="mt-3")
    ])

def get_therapies_tab():
    """Content for the therapies tab"""
    return html.Div([
        html.H4("My Active Therapies"),
        html.Div(id="active-therapies-table"),
        html.Hr(),
        html.H4("Medication Schedule"),
        html.Div(id="medication-schedule")
    ])

def get_alerts_tab():
    """Content for the alerts tab"""
    return html.Div([
        html.H4("My Alerts & Notifications"),
        html.Div(id="patient-alerts-list")
    ])