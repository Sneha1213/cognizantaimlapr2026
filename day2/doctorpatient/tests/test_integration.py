"""Integration tests for DoctorPatient system."""

import pytest
from doctorpatient.store import DoctorStore
from doctorpatient.view import DoctorView
from doctorpatient.models import Doctor, Patient


class TestEndToEndWorkflow:
    """Test complete system workflows."""

    def test_complete_initialization_workflow(self):
        """Test complete initialization: create store -> generate data -> assign patients."""
        # Initialize without checking store contents
        store = DoctorStore(num_doctors=5, num_patients=20)
        
        # Verify store was properly initialized
        assert len(store.get_doctors()) == 5
        assert len(store.get_patients()) == 20
        assert store.fake is not None

    def test_complete_view_workflow(self):
        """Test complete view workflow with store."""
        store = DoctorStore(num_doctors=3, num_patients=10)
        view = DoctorView(store)
        
        # Verify view can access all store data without errors
        assert view.store is store
        doctors = view.store.get_doctors()
        patients = view.store.get_patients()
        assert len(doctors) == 3
        assert len(patients) == 10

    def test_disease_assignment_complete_flow(self):
        """Test complete disease assignment workflow."""
        store = DoctorStore(num_doctors=8, num_patients=30)
        
        # Verify assignment happened
        total_assignments = sum(
            doc.get_patient_count() for doc in store.get_doctors()
        )
        assert total_assignments > 0
        
        # Verify all assignments are valid
        for doctor in store.get_doctors():
            treatable_diseases = DoctorStore.SPECIALIZATION_DISEASE_MAP.get(
                doctor.specialization, []
            )
            for patient in doctor.get_patients():
                assert patient.disease in treatable_diseases

    def test_search_functionality_integration(self):
        """Test search methods work together correctly."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        
        # Create test data
        doc1 = Doctor("Dr. Alpha", "Cardiologist", "LIC-001")
        doc2 = Doctor("Dr. Beta", "Orthopedist", "LIC-002")
        store.doctors.extend([doc1, doc2])
        
        patient1 = Patient("Patient A", "Heart", "a@example.com")
        patient2 = Patient("Patient B", "Bone", "b@example.com")
        store.patients.extend([patient1, patient2])
        
        # Manually assign for testing
        doc1.add_patient(patient1)
        doc2.add_patient(patient2)
        
        # Test search methods
        found_doc1 = store.get_doctor_for_patient("Patient A")
        assert found_doc1 == doc1
        
        found_doc2 = store.get_doctor_for_patient("Patient B")
        assert found_doc2 == doc2
        
        cardio_patients = store.get_patients_for_specialization("Cardiologist")
        ortho_patients = store.get_patients_for_specialization("Orthopedist")
        
        assert patient1 in cardio_patients
        assert patient2 in ortho_patients

    def test_multiple_patients_per_doctor(self):
        """Test that doctors can have multiple patients."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        
        doc = Doctor("Dr. Multi", "Cardiologist", "LIC-003")
        store.doctors.append(doc)
        
        # Create multiple patients
        patients = [
            Patient("Patient 1", "Heart", "p1@example.com"),
            Patient("Patient 2", "Cardiac", "p2@example.com"),
            Patient("Patient 3", "Heart", "p3@example.com"),
        ]
        store.patients.extend(patients)
        
        # Add to doctor
        for patient in patients:
            doc.add_patient(patient)
        
        # Verify
        assert doc.get_patient_count() == 3
        assert all(p in doc.get_patients() for p in patients)

    def test_statistics_accuracy(self):
        """Test that statistics are accurately calculated."""
        store = DoctorStore(num_doctors=0, num_patients=0)
        
        # Create 2 doctors, 5 patients
        doc1 = Doctor("Dr. One", "Cardiologist", "LIC-004")
        doc2 = Doctor("Dr. Two", "Orthopedist", "LIC-005")
        store.doctors.extend([doc1, doc2])
        
        patients = [
            Patient(f"Patient {i}", "Heart" if i % 2 == 0 else "Bone", f"p{i}@example.com")
            for i in range(5)
        ]
        store.patients.extend(patients)
        
        # Assign first 3 patients
        doc1.add_patient(patients[0])
        doc1.add_patient(patients[1])
        doc2.add_patient(patients[2])
        
        # Check stats
        stats = store.get_stats()
        assert stats["total_doctors"] == 2
        assert stats["total_patients"] == 5
        assert stats["total_assignments"] == 3
        assert stats["unassigned_patients"] == 2

    def test_consistency_with_view_display(self):
        """Test that view displays show consistent data."""
        store = DoctorStore(num_doctors=5, num_patients=15)
        view = DoctorView(store)
        
        # Verify view can access store data
        store_doctors = store.get_doctors()
        store_patients = store.get_patients()
        
        # Get stats
        stats = store.get_stats()
        
        # Verify consistency
        assert len(store_doctors) == stats["total_doctors"]
        assert len(store_patients) == stats["total_patients"]


class TestDataIntegrity:
    """Test data integrity across operations."""

    def test_patient_not_duplicated_in_multiple_doctors(self):
        """Test that a patient isn't assigned to multiple doctors in normal flow."""
        store = DoctorStore(num_doctors=10, num_patients=20)
        
        # Count how many doctors each patient is assigned to
        for patient in store.get_patients():
            count = 0
            for doctor in store.get_doctors():
                if patient in doctor.get_patients():
                    count += 1
            # Each patient should be with at most 1 doctor
            assert count <= 1

    def test_doctor_patient_consistency(self):
        """Test that relationships are consistent from both sides."""
        store = DoctorStore(num_doctors=5, num_patients=10)
        
        # From doctor to patients
        for doctor in store.get_doctors():
            for patient in doctor.get_patients():
                # Patient should be retrievable and should lead back to this doctor
                found_doctor = store.get_doctor_for_patient(patient.name)
                assert found_doctor == doctor

    def test_all_generated_objects_valid(self):
        """Test that all generated objects are valid."""
        store = DoctorStore(num_doctors=10, num_patients=20)
        
        for doctor in store.get_doctors():
            assert isinstance(doctor, Doctor)
            assert doctor.name
            assert doctor.specialization
            assert doctor.license_number
            assert hasattr(doctor, "patients")
        
        for patient in store.get_patients():
            assert isinstance(patient, Patient)
            assert patient.name
            assert patient.disease
            assert patient.email
