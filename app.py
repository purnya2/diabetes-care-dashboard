import dash
from dash import dcc, html
# from views import overview, glucose_tracker, medications  # Import your views when ready

# Initialize the Dash app
app = dash.Dash(__name__, use_pages=True)
app.title = "Diabetes Care Dashboard"

# Basic layout
app.layout = html.Div([
    html.H1('Diabetes Care Dashboard'),

    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)