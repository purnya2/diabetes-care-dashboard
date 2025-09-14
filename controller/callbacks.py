# controller/callbacks.py
import dash

def register_callbacks(app):
    """Register all callbacks for the app"""
    # Import and register callbacks from each module
    from controller.auth import register_auth_callbacks
    from controller.patient_callbacks import register_patient_callbacks
    from controller.doctor_callbacks import register_doctor_callbacks
    from controller.routing import register_routing_callbacks

    @app.callback(
        dash.Output('navbar-container', 'children'),
        dash.Input('url', 'pathname')
    )
    def update_navbar(pathname):
        from view import get_navbar
        try:
            return get_navbar()
        except Exception :
            from flask_login import logout_user
            logout_user()
            return get_navbar()

    # Register callbacks from each module
    register_auth_callbacks(app)
    register_patient_callbacks(app)
    register_doctor_callbacks(app)
    register_routing_callbacks(app)

'''
    Questo file (callbacks.py) serve per collegare tutte le funzionalità interattive 
    dell'applicazione Dash. In pratica, registra tutte le "callback" (funzioni che aggiornano 
    l'interfaccia utente in base alle azioni dell'utente o alla navigazione).
'''