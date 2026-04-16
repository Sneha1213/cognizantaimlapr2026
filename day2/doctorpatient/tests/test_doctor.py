"""Unit tests for Doctor model."""

import pytest
from doctorpatient.models import Doctor, Patient


class TestDoctorInit:
    """Test Doctor initialization."""

    def test_doctor_creation(self):
        """Test creating a doctor with valid attributes."""
        doc = Doctor("John Smith", "Cardiologist", "LIC-2024-001")
        assert doc.name == "John Smith"
        assert doc.specialization == "Cardiologist"
        assert doc.license_number == "LIC-2024-001"
        assert doc.patients == []

    def test_doctor_with_empty_patients(self):
        """Test that new doctor has no patients initially."""
        doc = Doctor("Jane Doe", "Orthopedist", "LIC-2024-002")
        assert doc.get_patient_count() == 0


class TestDoctorPatientManagement:
    """Test doctor's patient management functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.doctor = Doctor("Alice Johnson", "Neurologist", "LIC-2024-003")
        self.patient1 = Patient("Bob Williams", "Migraine", "bob@example.com")
        self.patient2 = Patient("Carol White", "Epilepsy", "carol@example.com")

    def test_add_single_patient(self):
        """Test adding a single patient to doctor."""
        self.doctor.add_patient(self.patient1)
        assert self.doctor.get_patient_count() == 1
        assert self.patient1 in self.doctor.get_patients()

    def test_add_multiple_patients(self):
        """Test adding multiple patients to doctor."""
        self.doctor.add_patient(self.patient1)
        self.doctor.add_patient(self.patient2)
        assert self.doctor.get_patient_count() == 2
        assert self.patient1 in self.doctor.get_patients()
        assert self.patient2 in self.doctor.get_patients()

    def test_prevent_duplicate_patients(self):
        """Test that same patient cannot be added twice."""
        self.doctor.add_patient(self.patient1)
        self.doctor.add_patient(self.patient1)  # Try to add again
        assert self.doctor.get_patient_count() == 1

    def test_get_patients_returns_copy(self):
        """Test that get_patients returns list with patients."""
        self.doctor.add_patient(self.patient1)
        patients_list = self.doctor.get_patients()
        assert len(patients_list) == 1
        assert patients_list[0] == self.patient1

    def test_remove_patient_by_id(self):
        """Test removing a patient by ID."""
        self.doctor.add_patient(self.patient1)
        self.doctor.add_patient(self.patient2)
        assert self.doctor.get_patient_count() == 2

        # Remove first patient
        result = self.doctor.remove_patient(0)
        assert result is True
        assert self.doctor.get_patient_count() == 1
        assert self.patient1 not in self.doctor.get_patients()
        assert self.patient2 in self.doctor.get_patients()

    def test_remove_patient_invalid_id(self):
        """Test removing patient with invalid ID."""
        self.doctor.add_patient(self.patient1)
        result = self.doctor.remove_patient(5)  # Invalid index
        assert result is False
        assert self.doctor.get_patient_count() == 1

    def test_remove_negative_id(self):
        """Test removing patient with negative ID."""
        self.doctor.add_patient(self.patient1)
        result = self.doctor.remove_patient(-1)
        assert result is False
        assert self.doctor.get_patient_count() == 1


class TestDoctorStringRepresentation:
    """Test doctor string representation."""

    def test_str_empty_patients(self):
        """Test string representation with no patients."""
        doc = Doctor("Test Doctor", "Cardiologist", "LIC-2024-004")
        result = str(doc)
        assert "Test Doctor" in result
        assert "Cardiologist" in result
        assert "LIC-2024-004" in result
        assert "Patients: 0" in result

    def test_str_with_patients(self):
        """Test string representation with patients."""
        doc = Doctor("Test Doctor", "Cardiologist", "LIC-2024-005")
        patient = Patient("Patient One", "Heart", "patient@example.com")
        doc.add_patient(patient)
        result = str(doc)
        assert "Patients: 1" in result
