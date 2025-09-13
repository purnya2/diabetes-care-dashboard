# view/navigation.py
import dash_bootstrap_components as dbc
from flask_login import current_user

def get_navbar():
    """Returns the appropriate navbar based on user authentication status"""
    if current_user.is_authenticated:
        # Navigation for logged-in users based on role
        nav_items = [
            dbc.NavItem(dbc.NavLink("Home", href="/")),
        ]
        
        # Role-specific navigation
        if current_user.role == 'patient':
            nav_items.extend([
                dbc.NavItem(dbc.NavLink("My Dashboard", href="/patient-dashboard")),
                dbc.NavItem(dbc.NavLink("Profile", href="/profile"))
            ])
        elif current_user.role == 'doctor':
            nav_items.extend([
                dbc.NavItem(dbc.NavLink("Doctor Dashboard", href="/doctor-dashboard")),
                dbc.NavItem(dbc.NavLink("Profile", href="/profile"))
            ])
        
        nav_items.append(dbc.NavItem(dbc.NavLink("Logout", href="/logout")))
        
        # Add user info to navbar
        user_info = f"{current_user.username} ({current_user.role.title()})"
        
        navbar = dbc.NavbarSimple(
            children=nav_items,
            brand="Diabetes Care System",
            brand_href="/",
            color="primary",
            dark=True,
            className="mb-3"
        )
    else:
        # Navigation for guests
        navbar = dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Login", href="/login")),
            ],
            brand="Diabetes Care System",
            brand_href="/",
            color="primary",
            dark=True,
            className="mb-3"
        )
    return navbar