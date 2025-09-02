import dash
from dash import html, dcc, callback
from controllers.auth_controller import authenticate_user, validate_credentials, create_session

dash.register_page(__name__, path='/doctor_dashboard')

layout = html.Div([
    dcc.Location(id='url', refresh=True), # For redirection
    html.H1('Doctor Dashboard'),
    html.Div(id='doctor-dashboard-content')
])

