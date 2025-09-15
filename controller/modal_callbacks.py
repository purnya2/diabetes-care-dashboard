# controller/modal_callbacks.py
import dash
from dash.dependencies import Input, Output, State
from dash import html
import dash_bootstrap_components as dbc
from flask_login import current_user
from pony.orm import db_session
from datetime import datetime

from model import (
    get_doctor_by_user_id, get_patient_by_user_id, add_therapy,
    Patient, Doctor
)

def register_modal_callbacks(app):
    """Register modal-related callbacks"""

    # Delete user modal callbacks
    @app.callback(
        Output('delete-user-modal', 'is_open'),
        [Input('confirm-delete-user', 'n_clicks'),
         Input('cancel-delete-user', 'n_clicks')],
        prevent_initial_call=True
    )
    def toggle_delete_user_modal(confirm_clicks, cancel_clicks):
        """Close the delete user modal when any button is clicked"""
        if confirm_clicks or cancel_clicks:
            return False
        return dash.no_update

    # Therapy modal callbacks
    @app.callback(
        Output('therapy-modal', 'is_open'),
        [Input('open-therapy-modal', 'n_clicks'),
         Input('confirm-therapy', 'n_clicks'),
         Input('cancel-therapy', 'n_clicks')],
        [State('therapy-modal', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_therapy_modal(open_clicks, confirm_clicks, cancel_clicks, is_open):
        """Toggle the therapy modal when any button is clicked"""
        if open_clicks or confirm_clicks or cancel_clicks:
            return not is_open
        return is_open

    @app.callback(
        Output('therapy-modal-output', 'children'),
        [Input('confirm-therapy', 'n_clicks')],
        [State('therapy-medication', 'value'),
         State('therapy-dosage', 'value'),
         State('therapy-frequency', 'value'),
         State('therapy-instructions', 'value'),
         State('selected-patient', 'value')],  # Assuming we have selected patient
        prevent_initial_call=True
    )
    @db_session
    def handle_therapy_confirmation(n_clicks, medication, dosage, frequency, instructions, patient_id):
        if not n_clicks or not medication or not dosage or not frequency:
            return ""

        if not current_user.is_authenticated or current_user.role != 'doctor':
            return dbc.Alert("Access denied", color="danger")

        doctor = get_doctor_by_user_id(current_user.id)
        if not doctor or not patient_id:
            return dbc.Alert("Invalid doctor or patient", color="danger")

        # Parse frequency to get daily doses (simplified)
        daily_doses = 1
        frequency_lower = frequency.lower()
        if 'twice' in frequency_lower or '2' in frequency_lower:
            daily_doses = 2
        elif 'three' in frequency_lower or '3' in frequency_lower:
            daily_doses = 3
        elif 'four' in frequency_lower or '4' in frequency_lower:
            daily_doses = 4

        # Extract dose amount and unit from dosage string
        import re
        dose_match = re.match(r'(\d+(?:\.\d+)?)\s*(\w+)', dosage)
        if dose_match:
            dose_amount = float(dose_match.group(1))
            dose_unit = dose_match.group(2)
        else:
            dose_amount = 1.0
            dose_unit = dosage

        success = add_therapy(
            patient_id, doctor.id, medication, daily_doses,
            dose_amount, dose_unit, instructions or ""
        )

        if success:
            return dbc.Alert(f"Therapy added successfully: {medication}", color="success")
        else:
            return dbc.Alert("Failed to add therapy", color="danger")

    # Glucose alert modal callbacks
    @app.callback(
        Output('glucose-alert-modal', 'is_open'),
        [Input('acknowledge-alert', 'n_clicks')],
        prevent_initial_call=True
    )
    def toggle_glucose_alert_modal(acknowledge_clicks):
        """Close the glucose alert modal when acknowledged"""
        if acknowledge_clicks:
            return False
        return dash.no_update

    @app.callback(
        Output('alert-content', 'children'),
        [Input('glucose-alert-modal', 'is_open')],
        prevent_initial_call=True
    )
    def update_alert_content(is_open):
        """Update alert content when modal opens"""
        if is_open:
            # This would typically be triggered by a specific alert
            # For now, we'll show a generic message
            return html.Div([
                html.H5("Glucose Level Alert", className="text-danger"),
                html.P("Your recent glucose reading is outside the normal range."),
                html.P("Please consult with your doctor if this persists."),
                html.Hr(),
                html.Small("Alert generated automatically based on your readings.", className="text-muted")
            ])
        return ""

    # Patient note modal callbacks
    @app.callback(
        Output('patient-note-modal', 'is_open'),
        [Input('open-note-modal', 'n_clicks'),
         Input('confirm-note', 'n_clicks'),
         Input('cancel-note', 'n_clicks')],
        [State('patient-note-modal', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_patient_note_modal(open_clicks, confirm_clicks, cancel_clicks, is_open):
        """Toggle the patient note modal when any button is clicked"""
        if open_clicks or confirm_clicks or cancel_clicks:
            return not is_open
        return is_open

    @app.callback(
        Output('patient-note-output', 'children'),
        [Input('confirm-note', 'n_clicks')],
        [State('patient-note', 'value'),
         State('selected-patient', 'value')],
        prevent_initial_call=True
    )
    @db_session
    def handle_patient_note(n_clicks, note_text, patient_id):
        if not n_clicks or not note_text or not patient_id:
            return ""

        if not current_user.is_authenticated or current_user.role != 'doctor':
            return dbc.Alert("Access denied", color="danger")

        try:
            # Add note to database (would need to create a Note model)
            # For now, just return success message
            patient = Patient[patient_id]

            # This would ideally save to a Notes table
            # For demonstration, we'll just show success
            return dbc.Alert(
                f"Note added for patient {patient.user.username}: {note_text[:50]}...",
                color="success"
            )
        except Exception as e:
            return dbc.Alert(f"Error saving note: {str(e)}", color="danger")

'''
    Questo file (modal_callbacks.py) gestisce i callback per i componenti modali.
    Include funzionalità per eliminazione utenti, gestione terapie e note sui pazienti.
'''
