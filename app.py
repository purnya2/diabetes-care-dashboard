import dash
from dash import dcc, html
import os
from flask_login import LoginManager

from model import get_user
from view import get_app_layout
from controller import register_callbacks


# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title = "Diabetes Care Dashboard"

server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'verysecretkey123')

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# Basic layout
'''app.layout = html.Div([
    html.H1('Diabetes Care Dashboard'),
    dash.page_container
])'''

@login_manager.user_loader
@db_session
def load_user(user_id):
    return get_user(user_id)

app.layout = get_app_layout()
register_callbacks(app)

if __name__ == '__main__':
    print("Starting Dash MVC Application...")
    print("Access the application at http://127.0.0.1:8050/")
    app.run(debug=True, port=8050)