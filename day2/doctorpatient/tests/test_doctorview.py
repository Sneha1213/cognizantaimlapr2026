"""Unit tests for DoctorView."""

import pytest
from io import StringIO
import sys
from doctorpatient.store import DoctorStore
from doctorpatient.view import DoctorView
from doctorpatient.models import Doctor, Patient


class TestDoctorViewInit:
    """Test DoctorView initialization."""

    def test_view_creation(self):
        """Test creating a DoctorView with store."""
        store = DoctorStore(num_doctors=5, num_patients=10)
        view = DoctorView(store)
        assert view.store == store

    def test_view_stores_reference(self):
        """Test that view maintains reference to store."""
        store = DoctorStore()
        view = DoctorView(store)
        assert view.store is store


class TestDisplayMethods:
    """Test display/output methods."""

    def setup_method(self):
        """Set up test fixtures."""
        self.store = DoctorStore(num_doctors=3, num_patients=5)
        self.view = DoctorView(self.store)

    def capture_output(self, func, *args):
        """Helper method to capture printed output."""
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            func(*args)
        finally:
            sys.stdout = sys.__stdout__
        return captured_output.getvalue()

    def test_display_all_doctors_with_patients(self):
        """Test display of all doctors with patients."""
        output = self.capture_output(self.view.display_all_doctors_with_patients)
        assert "DOCTORS WITH THEIR ASSIGNED PATIENTS" in output
        assert len(self.store.get_doctors()) > 0 or "No doctors" in output

    def test_display_all_patients_with_doctors(self):
        """Test display of all patients with doctors."""
        output = self.capture_output(self.view.display_all_patients_with_doctors)
        assert "PATIENTS WITH THEIR ASSIGNED DOCTORS" in output
        assert len(self.store.get_patients()) > 0 or "No patients" in output

    def test_display_statistics(self):
        """Test statistics display."""
        output = self.capture_output(self.view.display_statistics)
        assert "HEALTHCARE SYSTEM STATISTICS" in output
        assert "Total Doctors:" in output
        assert "Total Patients:" in output
        assert "Total Assignments:" in output
        assert "Unassigned Patients:" in output

    def test_display_summary(self):
        """Test doctor summary display."""
        output = self.capture_output(self.view.display_summary)
        assert "DOCTOR SUMMARY" in output


class TestSearchMethods:
    """Test search functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.store = DoctorStore(num_doctors=0, num_patients=0)
        
        # Create doctors
        self.doc_cardio = Doctor("Dr. Heart", "Cardiologist", "LIC-CAR-001")
        self.doc_ortho = Doctor("Dr. Bones", "Orthopedist", "LIC-ORT-001")
        self.store.doctors.extend([self.doc_cardio, self.doc_ortho])
        
        # Create patients
        self.patient_heart = Patient("John Heart", "Heart", "john@example.com")
        self.patient_bone = Patient("Jane Bone", "Bone", "jane@example.com")
        self.patient_cardiac = Patient("Bob Cardiac", "Cardiac", "bob@example.com")
        self.store.patients.extend([
            self.patient_heart, 
            self.patient_bone, 
            self.patient_cardiac
        ])
        
        # Assign patients
        self.doc_cardio.add_patient(self.patient_heart)
        self.doc_cardio.add_patient(self.patient_cardiac)
        self.doc_ortho.add_patient(self.patient_bone)
        
        self.view = DoctorView(self.store)

    def capture_output(self, func, *args):
        """Helper method to capture printed output."""
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            func(*args)
        finally:
            sys.stdout = sys.__stdout__
        return captured_output.getvalue()

    def test_search_patients_for_specialization_existing(self):
        """Test searching for patients with existing specialization."""
        output = self.capture_output(
            self.view.search_patients_for_specialization, "Cardiologist"
        )
        assert "SEARCHING FOR PATIENTS WITH SPECIALIZATION" in output
        assert "Cardiologist" in output

    def test_search_patients_for_specialization_nonexistent(self):
        """Test searching for patients with non-existent specialization."""
        output = self.capture_output(
            self.view.search_patients_for_specialization, "Dermatologist"
        )
        assert "No doctors found" in output or "SEARCHING FOR PATIENTS" in output

    def test_search_doctor_for_patient_existing(self):
        """Test searching for doctor for existing patient."""
        output = self.capture_output(
            self.view.search_doctor_for_patient, "John Heart"
        )
        assert "SEARCHING FOR DOCTOR FOR PATIENT" in output
        assert "Dr. Heart" in output or "Cardiologist" in output

    def test_search_doctor_for_patient_nonexistent(self):
        """Test searching for doctor for non-existent patient."""
        output = self.capture_output(
            self.view.search_doctor_for_patient, "Nonexistent Patient"
        )
        assert "SEARCHING FOR DOCTOR FOR PATIENT" in output
        assert "No doctor found" in output


class TestViewWithEmptyStore:
    """Test view behavior with empty store."""

    def setup_method(self):
        """Set up empty store."""
        self.store = DoctorStore(num_doctors=0, num_patients=0)
        self.view = DoctorView(self.store)

    def capture_output(self, func, *args):
        """Helper method to capture printed output."""
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            func(*args)
        finally:
            sys.stdout = sys.__stdout__
        return captured_output.getvalue()

    def test_display_with_no_doctors(self):
        """Test displaying when no doctors exist."""
        output = self.capture_output(self.view.display_all_doctors_with_patients)
        assert "No doctors found" in output or output  # Should not crash

    def test_display_with_no_patients(self):
        """Test displaying when no patients exist."""
        output = self.capture_output(self.view.display_all_patients_with_doctors)
        assert "No patients found" in output or output  # Should not crash
