import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('This is our Login page'),
    html.Div([
        html.Label('Username:'),
        dcc.Input(id='username-input', type='text', placeholder='Enter username'),

        html.Label('Password:'),
        dcc.Input(id='password-input', type='password', placeholder='Enter password'),

        html.Button('Login', id='login-button', n_clicks=0)
    ])
])