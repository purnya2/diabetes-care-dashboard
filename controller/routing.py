# controller/routing.py
import dash
from dash.dependencies import Input, Output
from flask_login import current_user, logout_user

from view import (
    get_home_layout, get_login_layout, get_register_layout, 
    get_profile_layout
)
from view.patient_dashboard import get_patient_dashboard_layout
from view.doctor_dashboard import get_doctor_dashboard_layout

def register_routing_callbacks(app):
    """Register page routing callbacks"""
    
    @app.callback(
        [Output('page-content', 'children'),
         Output('url', 'pathname', allow_duplicate=True)],
        [Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def display_page(pathname):
        # Handle logout
        if pathname == '/logout':
            if current_user.is_authenticated:
                logout_user()
            return get_home_layout(), '/'
        
        # Authentication pages
        if pathname == '/login':
            if current_user.is_authenticated:
                # Redirect based on role
                if current_user.role == 'patient':
                    return get_patient_dashboard_layout(), '/patient-dashboard'
                elif current_user.role == 'doctor':
                    return get_doctor_dashboard_layout(), '/doctor-dashboard'
                else:
                    return get_home_layout(), '/'
            return get_login_layout(), dash.no_update
        
        if pathname == '/register':
            if current_user.is_authenticated:
                # Redirect based on role
                if current_user.role == 'patient':
                    return get_patient_dashboard_layout(), '/patient-dashboard'
                elif current_user.role == 'doctor':
                    return get_doctor_dashboard_layout(), '/doctor-dashboard'
                    return get_admin_layout(), '/admin-dashboard'
                else:
                    return get_home_layout(), '/'
            return get_register_layout(), dash.no_update
        
        # Role-based dashboards
        if pathname == '/patient-dashboard':
            if current_user.is_authenticated and current_user.role == 'patient':
                return get_patient_dashboard_layout(), dash.no_update
            return get_login_layout(), '/login'
        
        if pathname == '/doctor-dashboard':
            if current_user.is_authenticated and current_user.role == 'doctor':
                return get_doctor_dashboard_layout(), dash.no_update
            return get_login_layout(), '/login'
        
        # Legacy dashboard route - redirect based on role
        if pathname == '/dashboard':
            if current_user.is_authenticated:
                if current_user.role == 'patient':
                    return get_patient_dashboard_layout(), '/patient-dashboard'
                elif current_user.role == 'doctor':
                    return get_doctor_dashboard_layout(), '/doctor-dashboard'
                else:
                    return get_home_layout(), '/'
            return get_login_layout(), '/login'
        
        if pathname == '/profile':
            if current_user.is_authenticated:
                return get_profile_layout(), dash.no_update
            return get_login_layout(), '/login'
        
        # Default home page
        return get_home_layout(), dash.no_update