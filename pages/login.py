import dash
from dash import html, dcc, callback
from controllers.auth_controller import authenticate_user

dash.register_page(__name__, path='/')

layout = html.Div([
    dcc.Location(id='url', refresh=True), # For redirection
    html.H1('This is our Login page'),
    html.Div([
        html.Label('Username:'),
        dcc.Input(id='username-input', type='text', placeholder='Enter username'),

        html.Label('Password:'),
        dcc.Input(id='password-input', type='password', placeholder='Enter password'),

        html.Button('Login', id='login-button', n_clicks=0),
        dcc.Checklist(
            options=[
                {'label': 'Log in as doctor', 'value': 'doctor'}
            ],
            id='login-as-doctor',
            inline=True
        ),
        html.Div(id='login-output')
    ])
])

@callback(
    [dash.Output('url', 'pathname'),
    dash.Output('login-output', 'children')],
    dash.Input('login-button', 'n_clicks'),
    dash.State('username-input', 'value'),
    dash.State('password-input', 'value'),
    dash.State('login-as-doctor', 'value')
)
def update_login_button(n_clicks, username, password, login_as_doctor):
    if n_clicks > 0:
        if authenticate_user(username, password, login_as_doctor=bool(login_as_doctor)):
            if login_as_doctor:
                # Redirect to doctor dashboard
                return "/doctor_dashboard", ""
            # Redirect to user dashboard
            return "/patient_dashboard", ""
        else:
            return "/", "Login Failed"
    return "/", ""