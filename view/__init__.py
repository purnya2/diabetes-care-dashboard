# view/__init__.py
from view.layout import get_app_layout, get_home_layout, get_profile_layout
from view.auth import get_login_layout, get_register_layout
from view.patient_dashboard import get_patient_dashboard_layout
from view.doctor_dashboard import get_doctor_dashboard_layout
from view.components import create_user_info_display
from view.navigation import get_navbar

# Re-export all necessary view functions
__all__ = [
    'get_app_layout', 'get_navbar', 'get_login_layout', 'get_register_layout',
    'get_home_layout', 'get_profile_layout',
    'get_patient_dashboard_layout', 'get_doctor_dashboard_layout',
    'create_user_info_display'
]

'''
    Questo file (__init__.py) del modulo view espone tutti i layout e componenti dell'interfaccia utente.
    Centralizza l'accesso alle viste per autenticazione, dashboard pazienti/dottori e navigazione.
'''