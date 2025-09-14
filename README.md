# Diabetes Care Telemedicine System

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate

# Install all required packages from requirements.txt
pip install -r requirements.txt

# Start the diabetes care dashboard
python mvc_app.py
```

## Testing Strategy

### Backend Testing Implementation

For comprehensive backend testing, here's the recommended testing structure:

#### 1. Test Setup Structure

```bash
# Create tests directory structure
mkdir -p tests/{unit,integration,fixtures}
touch tests/__init__.py
touch tests/conftest.py
```

#### 2. Required Test Dependencies

Add to `requirements-dev.txt`:
```txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
freezegun>=1.2.0
factory-boy>=3.2.0
```

#### 3. Struttura Test Completa

Il progetto ora include una **strategia di testing completa** implementata:

```
tests/
├── conftest.py              # Configurazione test database
├── requirements-dev.txt     # Dipendenze di sviluppo  
├── run_all_tests.py        # Script per esecuzione test
├── unit/                   # Test unitari
│   ├── test_models.py      # Test entità database
│   └── test_operations.py  # Test business logic
├── integration/            # Test di integrazione
│   └── test_workflows.py   # Test workflow completi
├── performance/            # Test performance
│   └── test_database_performance.py
└── fixtures/               # Utilità per test
    └── test_data_factory.py # Factory per dati di test
```

**A. Test Unitari (`tests/unit/`)**
- ✅ **Modelli database:** Creazione, validazione, relazioni utenti/pazienti/dottori
- ✅ **Operazioni business:** CRUD completo, autenticazione, compliance, alert
- ✅ **Validazione dati:** Controlli range glicemia, date, formati
- ✅ **Gestione errori:** Eccezioni e casi edge

**B. Test Integrazione (`tests/integration/`)**
- ✅ **Workflow pazienti:** Login → glicemia → alert → monitoraggio
- ✅ **Workflow dottori:** Gestione → prescrizioni → compliance → alert
- ✅ **Scenari completi:** 30 giorni simulati con dati realistici
- ✅ **Alert management:** Generazione → gestione → risoluzione

**C. Test Performance (`tests/performance/`)**
- ✅ **Database operations:** 1000+ record, query complesse, batch operations
- ✅ **Large datasets:** Simulazione 6 mesi dati reali per 50+ pazienti
- ✅ **Concurrent access:** Operazioni simultanee e carichi realistici
- ✅ **Memory efficiency:** Gestione ottimale grandi result set

#### 4. Esecuzione Test

**Setup veloce:**
```bash
# Installa dipendenze test
pip install -r requirements-dev.txt

# Menu interattivo
python tests/run_all_tests.py

# Tutti i test con coverage
python tests/run_all_tests.py all

# Solo test unitari/integrazione
python tests/run_all_tests.py unit
python tests/run_all_tests.py integration
```

**Test Coverage:**
- 🎯 **Target:** 80%+ coverage backend
- 📊 **Reports:** HTML + terminal output
- ⚡ **Performance:** < 1s per operazioni critiche
- 🔒 **Isolation:** Database in-memory per ogni test
- Patient info updates by doctors

**Edge Cases:**
- Glucose readings outside normal ranges
- Missing medication intakes over time
- Multiple therapies per patient
- Concurrent user operations
- Database transaction rollbacks

#### 5. Test Data Realistici

**Factory Pattern (`tests/fixtures/test_data_factory.py`):**
Il sistema include factory avanzati per generare dati di test realistici:

```python
# Scenari predefiniti
well_controlled_patient = ScenarioFactory.create_well_controlled_patient_scenario(test_db, doctor)
problematic_patient = ScenarioFactory.create_problematic_patient_scenario(test_db, doctor)
new_patient = ScenarioFactory.create_newly_diagnosed_patient_scenario(test_db, doctor)

# Dati randomizzati ma realistici
TestDataFactory.create_glucose_reading(test_db, patient)  # 70-400 mg/dL
TestDataFactory.create_therapy(test_db, patient, doctor)  # Farmaci reali
TestDataFactory.create_alert(test_db, patient, doctor)    # Alert tipici
```

**Scenari Clinici Reali:**
- 🟢 **Paziente controllato:** Glicemia 90-130, aderenza 95%
- 🟡 **Paziente problematico:** Glicemia 180-320, aderenza 60%, alert multipli
- 🔵 **Neodiagnosticato:** Pattern miglioramento graduale post-diagnosi

#### 6. Performance Validation

**Benchmark Realistici:**
```python
# Test con dataset grandi (6 mesi dati, 50 pazienti)
test_large_dataset_queries()           # < 2s
test_concurrent_access_simulation()    # < 1s per operazione
test_bulk_glucose_insertion()          # < 2s per 1000 record
test_compliance_checking_performance() # < 1s per 20 pazienti
```

#### 7. CI/CD Integration

**Automazione Completa:**
```yaml
name: Diabetes Care Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: python tests/run_all_tests.py all
      - run: coverage report --fail-under=80
```

#### 8. Test Reporting Avanzato

**Coverage Reports:**
- 📊 **HTML Report:** Visualizzazione interattiva coverage
- 📋 **Terminal Output:** Riepilogo immediato
- ⚡ **Performance Metrics:** Tempi operazioni critiche
- 🎯 **Missing Coverage:** Identificazione lacune

Questa strategia garantisce:
- ✅ **Coverage completo backend (80%+)**
- ✅ **Test isolation con database in-memory**
- ✅ **Scenari clinici realistici**
- ✅ **Performance validation automatica**
- ✅ **CI/CD integration ready**
- ✅ **Data integrity verification**
- ✅ **Regression prevention**

