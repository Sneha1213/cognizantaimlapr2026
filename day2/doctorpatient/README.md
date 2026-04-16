# DoctorPatient Healthcare Module - Quick Start Guide

## 🏥 What This Module Does

The DoctorPatient module is a healthcare tracking system that manages the relationships between doctors and patients. It automatically assigns patients to doctors based on disease-specialization matching.

**Example:** A patient with "Heart" disease will be assigned to a "Cardiologist" specialization automatically.

---

## 🚀 Quick Start: Running the Application

### Step 1: Activate Virtual Environment
```bash
cd /workspaces/cognizantaimlapr2026/day2
source day2env/bin/activate
```

### Step 2: Run the Application
```bash
PYTHONPATH=/workspaces/cognizantaimlapr2026/day2 python doctorpatient/app.py
```

### Expected Output
The application will display:
1. System statistics (doctors, patients, assignments)
2. All doctors with their assigned patients
3. All patients with their assigned doctors
4. Doctor summary (ranked by patient count)
5. Sample search demonstrations

---

## 🧪 Running Tests

### Run All Tests
```bash
PYTHONPATH=/workspaces/cognizantaimlapr2026/day2 python -m pytest doctorpatient/tests/ -v
```

### Run Specific Test Module
```bash
# Test only Doctor model
PYTHONPATH=/workspaces/cognizantaimlapr2026/day2 python -m pytest doctorpatient/tests/test_doctor.py -v

# Test only integration (end-to-end)
PYTHONPATH=/workspaces/cognizantaimlapr2026/day2 python -m pytest doctorpatient/tests/test_integration.py -v
```

### Expected Results
All 63 tests should pass ✅

---

## 📚 Code Structure

### Models Layer (`doctorpatient/models/`)
- **`doctor.py`** — Doctor model with patient management
  - Attributes: name, specialization, license_number, patients
  - Methods: add_patient(), remove_patient(), get_patients()
  
- **`patient.py`** — Patient model
  - Attributes: name, disease, email
  - Methods: get_info()

### Store Layer (`doctorpatient/store/`)
- **`doctorstore.py`** — Data access and business logic
  - Generates random doctors and patients (via Faker)
  - **Core Logic:** `assign_patients_by_disease()` — maps patients to doctors
  - Search methods: get_doctor_by_specialization(), get_doctor_for_patient()
  - Statistics: get_stats()

### View Layer (`doctorpatient/view/`)
- **`doctorview.py`** — Presentation and search
  - Display methods: display_all_doctors_with_patients(), display_all_patients_with_doctors()
  - Search methods: search_patients_for_specialization(), search_doctor_for_patient()
  - Statistics: display_statistics(), display_summary()

### Tests (`doctorpatient/tests/`)
- `test_doctor.py` — 11 Doctor model tests
- `test_patient.py` — 6 Patient model tests
- `test_doctorstore.py` — 24 Store layer tests
- `test_doctorview.py` — 10 View layer tests
- `test_integration.py` — 12 End-to-end tests

---

## 🎯 Disease-Specialization Mappings

The system includes 8 medical specializations, each mapped to specific diseases:

| Specialization | Treatable Diseases |
|--|--|
| Cardiologist | Heart, Cardiac, Cardiovascular, Hypertension |
| Orthopedist | Bone, Joint, Spine, Fracture, Arthritis |
| Neurologist | Brain, Nerve, Neurological, Migraine, Epilepsy |
| Dermatologist | Skin, Dermatitis, Psoriasis, Acne, Eczema |
| Gastroenterologist | Stomach, Digestive, Ulcer, IBS, Liver |
| Pulmonologist | Lung, Respiratory, Asthma, COPD, Pneumonia |
| Ophthalmologist | Eye, Vision, Cataract, Glaucoma, Myopia |
| Psychiatrist | Mental, Depression, Anxiety, Bipolar, Schizophrenia |

When a patient is created with a disease, they are automatically assigned to the first doctor whose specialization can treat that disease.

---

## 💻 Using the Module in Code

### Basic Example
```python
from doctorpatient.store import DoctorStore
from doctorpatient.view import DoctorView

# Initialize system (auto-generates 10 doctors and 50 patients)
store = DoctorStore(num_doctors=10, num_patients=50)

# Create view with store
view = DoctorView(store)

# Display all assignments
view.display_all_doctors_with_patients()
view.display_all_patients_with_doctors()

# Search for specific specialization
view.search_patients_for_specialization("Cardiologist")

# Find doctor for a patient
view.search_doctor_for_patient("John Doe")

# Get statistics
view.display_statistics()
```

### Working with Models Directly
```python
from doctorpatient.models import Doctor, Patient

# Create doctor and patient
doctor = Doctor("Dr. Smith", "Cardiologist", "LIC-2024-001")
patient = Patient("John Doe", "Heart", "john@example.com")

# Assign patient to doctor
doctor.add_patient(patient)

# Get patient info
print(patient.get_info())  # "Patient: John Doe | Disease: Heart | Email: john@example.com"
print(doctor)  # "Doctor: Dr. Smith | Specialization: Cardiologist | License: LIC-2024-001 | Patients: 1"
```

---

## 🔍 Key Features

✅ **Automatic Patient Assignment** — Patients assigned to doctors based on disease-specialization matching  
✅ **Random Data Generation** — Uses Faker for realistic names, emails, specializations  
✅ **Search Functionality** — Find patients for a doctor, find doctor for a patient (case-insensitive)  
✅ **Statistics Tracking** — Monitor total doctors, patients, assignments  
✅ **Clean Architecture** — Separation of concerns (Models → Store → View)  
✅ **Comprehensive Tests** — 63 tests covering all functionality  
✅ **Type Safety** — Full type hints throughout codebase  
✅ **Well Documented** — Docstrings on all classes and methods  

---

## 📊 Architecture

```
┌─────────────────────────────────────────────┐
│         DoctorPatient Module                 │
├─────────────────────────────────────────────┤
│                                              │
│  ┌────────────┐  ┌────────────┐            │
│  │  Doctor    │  │  Patient   │            │
│  │  Model     │  │  Model     │            │
│  └────────────┘  └────────────┘            │
│         △                 △                  │
│         └─────────┬───────┘                 │
│                   │                         │
│           ┌───────▼────────┐               │
│           │  DoctorStore   │               │
│           │  (Data Access) │               │
│           │  (Disease Map) │               │
│           └───────┬────────┘               │
│                   │                         │
│           ┌───────▼────────┐               │
│           │  DoctorView    │               │
│           │ (Presentation) │               │
│           └────────────────┘               │
│                                              │
└─────────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'doctorpatient'`
**Solution:** Make sure to set `PYTHONPATH`:
```bash
PYTHONPATH=/workspaces/cognizantaimlapr2026/day2 python ...
```

### Issue: `ModuleNotFoundError: No module named 'faker'`
**Solution:** Install faker in the virtual environment:
```bash
source day2env/bin/activate
pip install faker
```

### Issue: `ModuleNotFoundError: No module named 'pytest'`
**Solution:** Install pytest for tests:
```bash
source day2env/bin/activate
pip install pytest
```

---

## 📋 Default Initialization

When you create a DoctorStore, it automatically:
1. Generates 10 random doctors (default)
2. Generates 50 random patients (default)
3. Assigns each patient to a matching doctor (if specialization exists)
4. Returns empty/unassigned patients if no match found

```python
store = DoctorStore()  # Uses defaults: 10 doctors, 50 patients

# Or customize:
store = DoctorStore(num_doctors=5, num_patients=20)
```

---

## 📝 File Locations

```
/workspaces/cognizantaimlapr2026/day2/
├── doctorpatient/              ← Main module
│   ├── app.py                  ← Run this to see the system in action
│   ├── models/
│   │   ├── doctor.py
│   │   └── patient.py
│   ├── store/
│   │   └── doctorstore.py
│   ├── view/
│   │   └── doctorview.py
│   └── tests/                  ← Run pytest here
│       ├── test_doctor.py
│       ├── test_patient.py
│       ├── test_doctorstore.py
│       └── ...
└── IMPLEMENTATION_SUMMARY.md   ← Full implementation details
```

---

## ✅ Ready to Go!

The DoctorPatient module is fully implemented and tested. Start with:

```bash
cd /workspaces/cognizantaimlapr2026/day2
PYTHONPATH=/workspaces/cognizantaimlapr2026/day2 python doctorpatient/app.py
```

Happy coding! 🎉
