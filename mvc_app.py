# mvc_app.py
import dash
import dash_bootstrap_components as dbc
from flask_login import LoginManager
import os
from pony.orm import db_session

# Import from restructured modules
from model import get_user
from view import get_app_layout
from controller import register_callbacks
from scheduler import start_scheduler

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server

# Set a secure secret key for session management
server.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-for-development')

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

@login_manager.user_loader
@db_session
def load_user(user_id):
    return get_user(user_id)

app.layout = get_app_layout()

register_callbacks(app)

start_scheduler()  

if __name__ == '__main__':
    print("Starting Dash MVC Application...")
    print("Access the application at http://127.0.0.1:8050/")
    app.run(debug=True)

'''
    Questo file (mvc_app.py) è il punto di ingresso principale dell'applicazione.
    Configura Dash, il database, l'autenticazione e avvia il server dell'app.
'''