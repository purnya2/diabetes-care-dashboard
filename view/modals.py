# view/modals.py
from dash import html
import dash_bootstrap_components as dbc
from datetime import date

def create_delete_user_modal():
    """Creates a confirmation modal for deleting users"""
    return dbc.Modal([
        dbc.ModalHeader("Confirm Deletion"),
        dbc.ModalBody("Are you sure you want to delete this user? All their medical data will also be deleted."),
        dbc.ModalFooter([
            dbc.Button("Cancel", id="cancel-delete-user", className="ms-auto", color="secondary"),
            dbc.Button("Delete", id="confirm-delete-user", color="danger"),
        ]),
    ], id="delete-user-modal")

def create_therapy_modal():
    """Creates a modal for creating/editing therapy prescriptions"""
    return dbc.Modal([
        dbc.ModalHeader("Manage Therapy"),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Medication Name"),
                        dbc.Input(id="therapy-medication", type="text", placeholder="Enter medication name"),
                    ])
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Dosage"),
                        dbc.Input(id="therapy-dosage", type="text", placeholder="e.g., 10mg"),
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Frequency"),
                        dbc.Input(id="therapy-frequency", type="text", placeholder="e.g., Twice daily"),
                    ], width=6),
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Instructions"),
                        dbc.Textarea(id="therapy-instructions", placeholder="Special instructions for the patient"),
                    ])
                ]),
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancel", id="cancel-therapy", className="ms-auto", color="secondary"),
            dbc.Button("Save", id="confirm-therapy", color="success"),
        ]),
    ], id="therapy-modal")

def create_glucose_alert_modal():
    """Creates a modal for glucose level alerts"""
    return dbc.Modal([
        dbc.ModalHeader("Glucose Level Alert"),
        dbc.ModalBody([
            html.Div(id="alert-content"),
        ]),
        dbc.ModalFooter([
            dbc.Button("Acknowledge", id="acknowledge-alert", color="primary"),
        ]),
    ], id="glucose-alert-modal")

def create_patient_note_modal():
    """Creates a modal for adding doctor notes about patients"""
    return dbc.Modal([
        dbc.ModalHeader("Add Patient Note"),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Note"),
                        dbc.Textarea(id="patient-note", placeholder="Enter observations or recommendations", rows=5),
                    ])
                ]),
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancel", id="cancel-note", className="ms-auto", color="secondary"),
            dbc.Button("Save Note", id="confirm-note", color="success"),
        ]),
    ], id="patient-note-modal")