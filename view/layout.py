# view/layout.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from flask_login import current_user

from view.modals import create_delete_user_modal

# Main app layout
def get_app_layout():
    """Returns the main app layout"""
    return html.Div([
        dcc.Location(id='url', refresh=True),
        html.Div(id='navbar-container'),
        html.Div(id='page-content', className='container mt-4'),

        # Hidden containers for storing state
        dcc.Store(id='selected-user-id'),

        # Modals for user management only
        create_delete_user_modal()
    ])

# Home page layout
def get_home_layout():
    """Returns the home page layout"""
    return html.Div([
        html.H1('Diabetes Care Telemedicine System', className='text-center mb-4'),
        html.P('Welcome to the Diabetes Care Management Platform', className='lead text-center mb-5'),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("For Patients"),
                    dbc.CardBody([
                        html.H4("Manage Your Diabetes", className="card-title"),
                        html.Ul([
                            html.Li('Log daily glucose readings (before and after meals)'),
                            html.Li('Track symptoms and medication intake'),
                            html.Li('Receive alerts for abnormal readings'),
                            html.Li('Communicate with your diabetologist')
                        ]),
                        dbc.Button("Patient Login", color="primary", href="/login", className="mt-3")
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("For Doctors"),
                    dbc.CardBody([
                        html.H4("Monitor Your Patients", className="card-title"),
                        html.Ul([
                            html.Li('View patient glucose data and trends'),
                            html.Li('Prescribe and manage therapies'),
                            html.Li('Monitor medication compliance'),
                            html.Li('Receive alerts for critical glucose levels'),
                            html.Li('Update patient medical information')
                        ]),
                        dbc.Button("Doctor Login", color="success", href="/login", className="mt-3")
                    ])
                ])
            ], width=6)
        ], className="mb-5"),
        
        
    ])

# Dashboard page layout (protected)
def get_dashboard_layout():
    """Returns the dashboard page layout"""
    return html.Div([
        html.H1('Dashboard'),
        html.P('This is a protected dashboard page. Only logged-in users can see this.'),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader('My Profile'),
                dbc.CardBody([
                    html.H4('Account Overview', className='card-title'),
                    html.P('View and manage your profile information.'),
                    dbc.Button('Go to Profile', href='/profile', color='primary')
                ])
            ]), width=4),
            dbc.Col(dbc.Card([
                dbc.CardHeader('Health Monitoring'),
                dbc.CardBody([
                    html.H4('Diabetes Management', className='card-title'),
                    html.P('Track glucose, medications, and symptoms.'),
                    dbc.Button('View Dashboard', href='/patient' if hasattr(current_user, 'role') and current_user.role == 'patient' else '/doctor', color='primary')
                ])
            ]), width=4),
            dbc.Col(dbc.Card([
                dbc.CardHeader('Health Alerts'),
                dbc.CardBody([
                    html.H4('Recent Alerts', className='card-title'),
                    html.P('Monitor your glucose level alerts.'),
                ])
            ]), width=4)
        ])
    ])

# Profile page layout (protected)
def get_profile_layout():
    """Returns the profile page layout"""
    return html.Div([
        html.H1('User Profile'),
        html.P('This is your profile page. Here you can view your account details.'),
        html.Div(id='user-info')
    ])