# view/components.py
from dash import html
import dash_bootstrap_components as dbc

def create_user_info_display(username):
    """Creates the user info display component"""
    
    return html.Div([
        html.H4(f'Username: {username}'),
        dbc.Button('Edit Profile', id='edit-profile-button', color='primary', className='mr-2 me-2'),
        dbc.Button('Change Password', id='change-password-button', color='secondary')
    ])