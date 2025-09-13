# view/auth.py
from dash import html
import dash_bootstrap_components as dbc

# Login page layout
def get_login_layout():
    """Returns the login page layout"""
    return html.Div([
        html.H2('Diabetes Care System - Login', className='mb-4'),
        dbc.Form([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Username'),
                    dbc.Input(id='login-username', type='text', placeholder='Enter username')
                ])
            ], className='mb-3'),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Password'),
                    dbc.Input(id='login-password', type='password', placeholder='Enter password')
                ])
            ], className='mb-3'),
            dbc.Button('Login', id='login-button', color='primary', className='mt-3'),
            html.Div(id='login-output', className='mt-3'),
            html.Hr(),
            html.P([
                "Demo accounts: ",
                html.Br(),
                "Patient: patient1 / patientpass",
                html.Br(),
                "Doctor: dr_smith / doctorpass"
            ], className='text-muted mt-3')
        ])
    ])

# Register page layout with role selection
def get_register_layout():
    """Returns the register page layout"""
    return html.Div([
        html.H2('Register - Diabetes Care System', className='mb-4'),
        dbc.Form([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Username'),
                    dbc.Input(id='register-username', type='text', placeholder='Choose a username')
                ])
            ], className='mb-3'),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Role'),
                    dbc.Select(
                        id='register-role',
                        options=[
                            {'label': 'Patient', 'value': 'patient'},
                            {'label': 'Doctor', 'value': 'doctor'}
                        ],
                        value='patient'
                    )
                ])
            ], className='mb-3'),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Password'),
                    dbc.Input(id='register-password', type='password', placeholder='Choose a password')
                ])
            ], className='mb-3'),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Confirm Password'),
                    dbc.Input(id='register-confirm-password', type='password', placeholder='Confirm your password')
                ])
            ], className='mb-3'),
            dbc.Button('Register', id='register-button', color='primary', className='mt-3'),
            html.Div(id='register-output', className='mt-3')
        ])
    ])

'''
    Questo file (auth.py) gestisce le viste per l'autenticazione degli utenti.
    Contiene i layout per le pagine di login e registrazione del sistema.
'''