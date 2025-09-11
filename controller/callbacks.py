# controller/callbacks.py
import dash

def register_callbacks(app):
    """Register all callbacks for the app"""
    # Import and register callbacks from each module
    from controller.auth import register_auth_callbacks
    from controller.admin import register_admin_callbacks
    from controller.projects import register_project_callbacks
    from controller.project_detail import register_project_detail_callbacks
    from controller.routing import register_routing_callbacks

    # Register navbar callback (kept here since it's simple)
    @app.callback(
        dash.Output('navbar-container', 'children'),
        dash.Input('url', 'pathname')
    )
    def update_navbar(pathname):
        from view import get_navbar
        return get_navbar()

    # Register callbacks from each module
    register_auth_callbacks(app)
    register_admin_callbacks(app)
    register_project_callbacks(app)
    register_project_detail_callbacks(app)
    register_routing_callbacks(app)