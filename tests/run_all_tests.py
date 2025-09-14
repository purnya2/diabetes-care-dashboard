# tests/run_all_tests.py
"""
Script per eseguire tutti i test del sistema diabetes care dashboard.
Fornisce reporting dettagliato e configurazione dei test.
"""
import sys
import os
import pytest
from pathlib import Path

# Aggiungi il path root del progetto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_unit_tests():
    """Esegue solo i test unitari"""
    print("🧪 Esecuzione test unitari...")
    return pytest.main([
        "tests/unit/",
        "-v",
        "--tb=short",
        "--capture=no"
    ])


def main():
    return run_unit_tests()


if __name__ == "__main__":

    exit_code = main()
    sys.exit(exit_code)