# scheduler.py
import time
import threading
import os
from model import check_all_patients_compliance
from datetime import datetime

# Global variable per controllare se lo scheduler è attivo
_scheduler_running = False
_scheduler_thread = None
_scheduler_id = None

def run_compliance_check():
    """Esegue il controllo di compliance per tutti i pazienti"""
    global _scheduler_id
    scheduler_info = f"[Scheduler-{_scheduler_id}]" if _scheduler_id else ""
    print(f"{scheduler_info}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running compliance check for all patients...")
    try:
        check_all_patients_compliance()
        print(f"{scheduler_info}Compliance check completed successfully")
    except Exception as e:
        print(f"{scheduler_info}Error during compliance check: {e}")

def _background_scheduler():
    """Funzione per eseguire i controlli di compliance in background"""
    global _scheduler_running
    while _scheduler_running:
        run_compliance_check()
        time.sleep(20)  # Check compliance every hour (3600 seconds)
        
def start_scheduler():
    """Avvia lo scheduler in background per controlli automatici di compliance"""
    global _scheduler_running, _scheduler_thread
    
    if _scheduler_running:
        print("Scheduler already running")
        return
        
    _scheduler_running = True
    _scheduler_thread = threading.Thread(target=_background_scheduler, daemon=True)
    _scheduler_thread.start()
    print("Compliance scheduler started - automatic checks every hour")

def stop_scheduler():
    """Ferma lo scheduler di background"""
    global _scheduler_running
    _scheduler_running = False
    print("Compliance scheduler stopped")

def run_immediate_compliance_check():
    """Esegue immediatamente un controllo di compliance (per testing)"""
    run_compliance_check()

'''
    Questo file (scheduler.py) gestisce la pianificazione automatica dei controlli di compliance.
    Esegue verifiche periodiche per tutti i pazienti e genera alert appropriati.
    
    Funzionalità principali:
    - Controlli automatici ogni 24 ore in background
    - Possibilità di eseguire controlli manuali per testing
    - Sistema di alert per pazienti non aderenti alla terapia
    - Integrazione con sistema di pulizia automatica degli alert
'''

'''
    Questo file (scheduler.py) gestisce la pianificazione automatica dei controlli di compliance.
    Esegue verifiche periodiche per tutti i pazienti e genera alert appropriati.
'''