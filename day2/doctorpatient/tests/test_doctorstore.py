"""Unit tests for DoctorStore."""

import pytest
from faker import Faker
from doctorpatient.store import DoctorStore
from doctorpatient.models import Doctor, Patient


class TestDoctorStoreInit:
    """Test DoctorStore initialization."""

    def test_store_creation_default(self):
        """Test creating store with default parameters."""
        store = DoctorStore()
        assert len(store.get_doctors()) == 10
        assert len(store.get_patients()) == 50

    def test_store_creation_custom(self):
        """Test creating store with custom parameters."""
        store = DoctorStore(num_doctors=5, num_patients=20)
        assert len(store.get_doctors()) == 5
        assert len(store.get_patients()) == 20

    def test_store_has_faker(self):
        """Test that store has Faker instance."""
        store = DoctorStore()
        assert isinstance(store.fake, Faker)

    def test_store_has_disease_map(self):
        """Test that store has specialization-disease mapping."""
        assert hasattr(DoctorStore, "SPECIALIZATION_DISEASE_MAP")
        assert isinstance(DoctorStore.SPECIALIZATION_DISEASE_MAP, dict)
        assert len(DoctorStore.SPECIALIZATION_DISEASE_MAP) > 0


class TestDoctorGeneration:
    """Test doctor generation."""

    def test_generate_doctors(self):
        """Test generating doctors."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        store.generate_doctors(5)
        assert len(store.get_doctors()) == 5

    def test_generated_doctors_have_valid_specializations(self):
        """Test that generated doctors have valid specializations."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        store.generate_doctors(10)
        valid_specs = list(DoctorStore.SPECIALIZATION_DISEASE_MAP.keys())
        for doctor in store.get_doctors():
            assert doctor.specialization in valid_specs

    def test_generated_doctors_have_required_attributes(self):
        """Test that generated doctors have all required attributes."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        store.generate_doctors(3)
        for doctor in store.get_doctors():
            assert doctor.name
            assert doctor.specialization
            assert doctor.license_number
            assert doctor.patients == []


class TestPatientGeneration:
    """Test patient generation."""

    def test_generate_patients(self):
        """Test generating patients."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        store.generate_patients(10)
        assert len(store.get_patients()) == 10

    def test_generated_patients_have_valid_diseases(self):
        """Test that generated patients have diseases from the map."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        store.generate_patients(10)
        all_valid_diseases = []
        for diseases in DoctorStore.SPECIALIZATION_DISEASE_MAP.values():
            all_valid_diseases.extend(diseases)
        for patient in store.get_patients():
            assert patient.disease in all_valid_diseases

    def test_generated_patients_have_required_attributes(self):
        """Test that generated patients have all required attributes."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        store.generate_patients(5)
        for patient in store.get_patients():
            assert patient.name
            assert patient.disease
            assert patient.email


class TestPatientAssignmentByDisease:
    """Test the core disease-based patient assignment logic."""

    def test_patients_assigned_to_matching_doctors(self):
        """Test that patients are assigned to doctors with matching specialization."""
        store = DoctorStore(num_doctors=5, num_patients=10)
        
        # Verify patients are actually assigned
        total_assignments = sum(
            doc.get_patient_count() for doc in store.get_doctors()
        )
        assert total_assignments > 0
        assert total_assignments <= len(store.get_patients())

    def test_assignment_respects_disease_map(self):
        """Test that assignment respects specialization-disease mapping."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        
        # Create specific doctor and patient for testing
        doc = Doctor("Test Doctor", "Cardiologist", "LIC-001")
        store.doctors.append(doc)
        
        patient = Patient("Test Patient", "Heart", "test@example.com")
        store.patients.append(patient)
        
        # Assign
        store.assign_patients_by_disease()
        
        # Verify patient assigned to cardiologist
        assert patient in doc.get_patients()

    def test_no_assignment_for_non_matching_disease(self):
        """Test that patients aren't assigned to non-matching specializations."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        
        # Create doctor with specialization that doesn't include the patient's disease
        doc = Doctor("Orthopedist", "Orthopedist", "LIC-002")
        store.doctors.append(doc)
        
        patient = Patient("Test Patient", "Heart", "test@example.com")  # Cardiologist disease
        store.patients.append(patient)
        
        # Assign
        store.assign_patients_by_disease()
        
        # Verify patient NOT assigned to orthopedist
        assert patient not in doc.get_patients()

    def test_patient_assigned_to_first_matching_doctor(self):
        """Test that each patient is assigned to first matching doctor only."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        
        # Create two doctors with same specialization
        doc1 = Doctor("Doctor One", "Cardiologist", "LIC-003")
        doc2 = Doctor("Doctor Two", "Cardiologist", "LIC-004")
        store.doctors.extend([doc1, doc2])
        
        patient = Patient("Test Patient", "Heart", "test@example.com")
        store.patients.append(patient)
        
        # Assign
        store.assign_patients_by_disease()
        
        # Patient should be with one doctor, not both
        total_assignments = doc1.get_patient_count() + doc2.get_patient_count()
        assert total_assignments == 1


class TestDoctorStoreSearch:
    """Test search and retrieval methods."""

    def test_get_doctors_returns_all(self):
        """Test getting all doctors."""
        store = DoctorStore(num_doctors=8, num_patients=0)
        doctors = store.get_doctors()
        assert len(doctors) == 8

    def test_get_patients_returns_all(self):
        """Test getting all patients."""
        store = DoctorStore(num_doctors=0, num_patients=15)
        patients = store.get_patients()
        assert len(patients) == 15

    def test_get_doctor_by_specialization(self):
        """Test finding doctors by specialization."""
        store = DoctorStore(num_doctors=10, num_patients=0)
        cardiologists = store.get_doctor_by_specialization("Cardiologist")
        assert all(doc.specialization == "Cardiologist" for doc in cardiologists)

    def test_get_doctor_by_specialization_case_insensitive(self):
        """Test that specialization search is case-insensitive."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        doc = Doctor("Test", "Cardiologist", "LIC-005")
        store.doctors.append(doc)
        
        result1 = store.get_doctor_by_specialization("Cardiologist")
        result2 = store.get_doctor_by_specialization("CARDIOLOGIST")
        result3 = store.get_doctor_by_specialization("cardiologist")
        
        assert len(result1) == 1
        assert len(result2) == 1
        assert len(result3) == 1

    def test_get_patients_for_specialization(self):
        """Test getting patients for a specific specialization."""
        store = DoctorStore(num_doctors=5, num_patients=15)
        cardio_patients = store.get_patients_for_specialization("Cardiologist")
        assert isinstance(cardio_patients, list)

    def test_get_doctor_for_patient(self):
        """Test finding doctor for a specific patient."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        
        doc = Doctor("Test Doctor", "Cardiologist", "LIC-006")
        patient = Patient("John Doe", "Heart", "john@example.com")
        doc.add_patient(patient)
        store.doctors.append(doc)
        store.patients.append(patient)
        
        found_doc = store.get_doctor_for_patient("John Doe")
        assert found_doc == doc

    def test_get_doctor_for_nonexistent_patient(self):
        """Test finding doctor for non-existent patient."""
        store = DoctorStore(num_doctors=5, num_patients=0)
        found_doc = store.get_doctor_for_patient("Nonexistent Patient")
        assert found_doc is None

    def test_get_doctor_for_patient_case_insensitive(self):
        """Test that patient search is case-insensitive."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        
        doc = Doctor("Test", "Cardiologist", "LIC-007")
        patient = Patient("Mary Smith", "Heart", "mary@example.com")
        doc.add_patient(patient)
        store.doctors.append(doc)
        store.patients.append(patient)
        
        found1 = store.get_doctor_for_patient("Mary Smith")
        found2 = store.get_doctor_for_patient("MARY SMITH")
        found3 = store.get_doctor_for_patient("mary smith")
        
        assert found1 == doc
        assert found2 == doc
        assert found3 == doc


class TestDoctorStoreStats:
    """Test statistics functionality."""

    def test_get_stats_structure(self):
        """Test that stats dictionary has required keys."""
        store = DoctorStore(num_doctors=5, num_patients=10)
        stats = store.get_stats()
        
        assert "total_doctors" in stats
        assert "total_patients" in stats
        assert "total_assignments" in stats
        assert "unassigned_patients" in stats

    def test_get_stats_values(self):
        """Test that stats values are correct."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        
        doc = Doctor("Test", "Cardiologist", "LIC-008")
        patient1 = Patient("Patient 1", "Heart", "p1@example.com")
        patient2 = Patient("Patient 2", "Joint", "p2@example.com")
        
        doc.add_patient(patient1)
        store.doctors.append(doc)
        store.patients.extend([patient1, patient2])
        
        stats = store.get_stats()
        assert stats["total_doctors"] == 1
        assert stats["total_patients"] == 2
        assert stats["total_assignments"] == 1
        assert stats["unassigned_patients"] == 1
