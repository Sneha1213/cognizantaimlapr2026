"""Unit tests for Patient model."""

import pytest
from doctorpatient.models import Patient


class TestPatientInit:
    """Test Patient initialization."""

    def test_patient_creation(self):
        """Test creating a patient with valid attributes."""
        patient = Patient("John Doe", "Heart Disease", "john@example.com")
        assert patient.name == "John Doe"
        assert patient.disease == "Heart Disease"
        assert patient.email == "john@example.com"

    def test_patient_with_different_diseases(self):
        """Test creating patients with various diseases."""
        diseases = ["Heart", "Cardiac", "Arthritis", "Asthma"]
        for disease in diseases:
            patient = Patient("Test Patient", disease, "test@example.com")
            assert patient.disease == disease


class TestPatientGetInfo:
    """Test patient information retrieval."""

    def test_get_info_format(self):
        """Test get_info returns properly formatted string."""
        patient = Patient("Alice Smith", "Migraine", "alice@example.com")
        info = patient.get_info()
        assert "Alice Smith" in info
        assert "Migraine" in info
        assert "alice@example.com" in info
        assert "Patient:" in info
        assert "Disease:" in info
        assert "Email:" in info

    def test_get_info_consistency(self):
        """Test that get_info is consistent with str()."""
        patient = Patient("Bob Johnson", "Epilepsy", "bob@example.com")
        assert patient.get_info() == str(patient)


class TestPatientStringRepresentation:
    """Test patient string representation."""

    def test_str_representation(self):
        """Test string representation of patient."""
        patient = Patient("Carol Wilson", "Bone Fracture", "carol@example.com")
        result = str(patient)
        assert "Carol Wilson" in result
        assert "Bone Fracture" in result
        assert "carol@example.com" in result

    def test_str_with_special_characters(self):
        """Test string representation with special characters in name."""
        patient = Patient("Dr. José García", "Joint Pain", "jose@example.com")
        result = str(patient)
        assert "José García" in result
        assert "Joint Pain" in result
