import dash
from dash import html, dcc, callback

dash.register_page(__name__, path='/patient_dashboard')

layout = html.Div([
    dcc.Location(id='url', refresh=True), # For redirection
    html.H1('Patient Dashboard'),
    html.Div(id='patient-dashboard-content')
])

