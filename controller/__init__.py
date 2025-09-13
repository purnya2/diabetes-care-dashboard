# controller/__init__.py
from .callbacks import register_callbacks

# Re-export the main functions to maintain compatibility
__all__ = ['register_callbacks']

'''
    Questo file (__init__.py) del modulo controller espone la funzione principale per registrare i callback.
    Centralizza l'accesso a tutti i callback per autenticazione, routing e funzionalità delle dashboard.
'''