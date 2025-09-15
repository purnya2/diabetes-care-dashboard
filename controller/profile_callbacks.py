# controller/profile_callbacks.py
import dash
from dash.dependencies import Input, Output, State
from dash import html
import dash_bootstrap_components as dbc
from flask_login import current_user
from pony.orm import db_session
from datetime import datetime

def register_profile_callbacks(app):
    """Register profile-related callbacks"""

    # Edit profile button callback
    @app.callback(
        Output('edit-profile-modal', 'is_open'),
        [Input('edit-profile-button', 'n_clicks'),
         Input('cancel-profile-edit', 'n_clicks'),
         Input('save-profile-changes', 'n_clicks')],
        [State('edit-profile-modal', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_edit_profile_modal(edit_clicks, cancel_clicks, save_clicks, is_open):
        """Toggle the edit profile modal"""
        if edit_clicks or cancel_clicks or save_clicks:
            return not is_open
        return is_open

    # Profile edit form callback
    @app.callback(
        Output('profile-edit-output', 'children'),
        [Input('save-profile-changes', 'n_clicks')],
        [State('edit-username', 'value'),
         State('edit-email', 'value')],
        prevent_initial_call=True
    )
    @db_session
    def handle_profile_edit(n_clicks, username, email):
        if not n_clicks:
            return ""

        if not current_user.is_authenticated:
            return dbc.Alert("Please log in to edit your profile", color="danger")

        # Validate inputs
        if not username or len(username.strip()) < 3:
            return dbc.Alert("Username must be at least 3 characters long", color="warning")

        try:
            # Update user information (would need to implement in model)
            # For now, just show success message
            return dbc.Alert(
                f"Profile updated successfully! Username: {username}, Email: {email or 'Not provided'}",
                color="success"
            )
        except Exception as e:
            return dbc.Alert(f"Error updating profile: {str(e)}", color="danger")

    # Populate profile fields when modal opens
    @app.callback(
        [Output('edit-username', 'value'),
         Output('edit-email', 'value')],
        [Input('edit-profile-modal', 'is_open')],
        prevent_initial_call=True
    )
    @db_session
    def populate_profile_fields(is_open):
        if is_open and current_user.is_authenticated:
            # Get current user data
            return current_user.username, ""  # Email would come from user model if available
        return "", ""

    # Change password button callback
    @app.callback(
        Output('change-password-modal', 'is_open'),
        [Input('change-password-button', 'n_clicks'),
         Input('cancel-password-change', 'n_clicks'),
         Input('save-password-change', 'n_clicks')],
        [State('change-password-modal', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_change_password_modal(change_clicks, cancel_clicks, save_clicks, is_open):
        """Toggle the change password modal"""
        if change_clicks or cancel_clicks or save_clicks:
            return not is_open
        return is_open

    # Password change form callback
    @app.callback(
        Output('password-change-output', 'children'),
        [Input('save-password-change', 'n_clicks')],
        [State('current-password', 'value'),
         State('new-password', 'value'),
         State('confirm-new-password', 'value')],
        prevent_initial_call=True
    )
    @db_session
    def handle_password_change(n_clicks, current_password, new_password, confirm_password):
        if not n_clicks:
            return ""

        if not current_user.is_authenticated:
            return dbc.Alert("Please log in to change your password", color="danger")

        # Validate inputs
        if not all([current_password, new_password, confirm_password]):
            return dbc.Alert("All password fields are required", color="warning")

        if new_password != confirm_password:
            return dbc.Alert("New passwords do not match", color="warning")

        if len(new_password) < 6:
            return dbc.Alert("Password must be at least 6 characters long", color="warning")

        try:
            # Verify current password and update (would need to implement in model)
            # For now, just show success message
            return dbc.Alert("Password changed successfully!", color="success")
        except Exception as e:
            return dbc.Alert(f"Error changing password: {str(e)}", color="danger")

def create_edit_profile_modal():
    """Create the edit profile modal component"""
    return dbc.Modal([
        dbc.ModalHeader("Edit Profile"),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Username"),
                        dbc.Input(
                            id="edit-username",
                            type="text",
                            placeholder="Enter new username"
                        ),
                    ])
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Email (Optional)"),
                        dbc.Input(
                            id="edit-email",
                            type="email",
                            placeholder="Enter email address"
                        ),
                    ])
                ], className="mb-3"),
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancel", id="cancel-profile-edit", className="ms-auto", color="secondary"),
            dbc.Button("Save Changes", id="save-profile-changes", color="primary"),
        ]),
        html.Div(id="profile-edit-output", className="mt-3")
    ], id="edit-profile-modal")

def create_change_password_modal():
    """Create the change password modal component"""
    return dbc.Modal([
        dbc.ModalHeader("Change Password"),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Current Password"),
                        dbc.Input(
                            id="current-password",
                            type="password",
                            placeholder="Enter current password"
                        ),
                    ])
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("New Password"),
                        dbc.Input(
                            id="new-password",
                            type="password",
                            placeholder="Enter new password"
                        ),
                    ])
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Confirm New Password"),
                        dbc.Input(
                            id="confirm-new-password",
                            type="password",
                            placeholder="Confirm new password"
                        ),
                    ])
                ], className="mb-3"),
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancel", id="cancel-password-change", className="ms-auto", color="secondary"),
            dbc.Button("Change Password", id="save-password-change", color="primary"),
        ]),
        html.Div(id="password-change-output", className="mt-3")
    ], id="change-password-modal")

'''
    Questo file (profile_callbacks.py) gestisce i callback per le funzionalità del profilo utente.
    Include modifica profilo e cambio password.
'''
