"""DoctorView for presentation and display layer."""

from typing import List
from ..store import DoctorStore
from ..models import Doctor, Patient


class DoctorView:
    """Handles presentation and search functionality for healthcare data.
    
    Provides multiple views and search capabilities:
    - Display all doctors with their assigned patients
    - Display all patients with their assigned doctors
    - Search patients by doctor specialization
    - Search doctor for a specific patient
    
    Attributes:
        store: DoctorStore instance providing data access
    """

    def __init__(self, store: DoctorStore) -> None:
        """Initialize DoctorView with dependency-injected store.
        
        Args:
            store: DoctorStore instance for data access
        """
        self.store = store

    def display_all_doctors_with_patients(self) -> None:
        """Display all doctors and their assigned patients.
        
        Shows each doctor's details and a list of their patients.
        """
        doctors = self.store.get_doctors()
        print("\n" + "=" * 80)
        print("ALL DOCTORS WITH THEIR ASSIGNED PATIENTS")
        print("=" * 80)

        if not doctors:
            print("No doctors found.")
            return

        for idx, doctor in enumerate(doctors, 1):
            print(f"\n[{idx}] {doctor}")
            patients = doctor.get_patients()
            if patients:
                print(f"    Patients ({len(patients)}):")
                for p_idx, patient in enumerate(patients, 1):
                    print(f"      {p_idx}. {patient}")
            else:
                print("    Patients: None assigned")

        print("\n" + "=" * 80 + "\n")

    def display_all_patients_with_doctors(self) -> None:
        """Display all patients and their assigned doctors.
        
        Shows each patient's details and their assigned doctor's information.
        """
        patients = self.store.get_patients()
        print("\n" + "=" * 80)
        print("ALL PATIENTS WITH THEIR ASSIGNED DOCTORS")
        print("=" * 80)

        if not patients:
            print("No patients found.")
            return

        for idx, patient in enumerate(patients, 1):
            doctor = self.store.get_doctor_for_patient(patient.name)
            print(f"\n[{idx}] {patient}")
            if doctor:
                print(f"    Assigned Doctor: {doctor.name}")
                print(f"    Specialization: {doctor.specialization}")
                print(f"    License: {doctor.license_number}")
            else:
                print("    Assigned Doctor: UNASSIGNED")

        print("\n" + "=" * 80 + "\n")

    def search_patients_for_specialization(self, specialization: str) -> None:
        """Find and display all patients for doctors with a specific specialization.
        
        Args:
            specialization: Medical specialization to search for (e.g., "Cardiologist")
        """
        print("\n" + "-" * 80)
        print(
            f"SEARCHING FOR PATIENTS WITH SPECIALIZATION: {specialization.upper()}"
        )
        print("-" * 80)

        doctors = self.store.get_doctor_by_specialization(specialization)
        if not doctors:
            print(f"No doctors found with specialization: {specialization}")
            print("-" * 80 + "\n")
            return

        print(f"Found {len(doctors)} doctor(s) with specialization: {specialization}")
        print()

        for doctor_idx, doctor in enumerate(doctors, 1):
            print(f"{doctor_idx}. {doctor}")
            patients = doctor.get_patients()
            if patients:
                print(f"   Patients ({len(patients)}):")
                for p_idx, patient in enumerate(patients, 1):
                    print(f"     {p_idx}. {patient.name} - Disease: {patient.disease}")
            else:
                print("   Patients: None")
            print()

        print("-" * 80 + "\n")

    def search_doctor_for_patient(self, patient_name: str) -> None:
        """Find and display doctor assigned to a specific patient.
        
        Args:
            patient_name: Name of the patient to search for
        """
        print("\n" + "-" * 80)
        print(f"SEARCHING FOR DOCTOR FOR PATIENT: {patient_name.upper()}")
        print("-" * 80)

        doctor = self.store.get_doctor_for_patient(patient_name)
        if doctor:
            print(f"Patient: {patient_name}")
            print(f"Assigned Doctor: {doctor.name}")
            print(f"Specialization: {doctor.specialization}")
            print(f"License: {doctor.license_number}")
            print(f"Contact: {patient_name}'s record on file")
        else:
            print(f"No doctor found for patient: {patient_name}")
            print("Patient may be unassigned or name may not exist in system.")

        print("-" * 80 + "\n")

    def display_statistics(self) -> None:
        """Display system statistics and summary information."""
        stats = self.store.get_stats()
        print("\n" + "=" * 80)
        print("HEALTHCARE SYSTEM STATISTICS")
        print("=" * 80)
        print(f"Total Doctors:         {stats['total_doctors']}")
        print(f"Total Patients:        {stats['total_patients']}")
        print(f"Total Assignments:     {stats['total_assignments']}")
        print(f"Unassigned Patients:   {stats['unassigned_patients']}")
        print("=" * 80 + "\n")

    def display_summary(self) -> None:
        """Display a summary of doctors ordered by patient count."""
        doctors = self.store.get_doctors()
        print("\n" + "=" * 80)
        print("DOCTOR SUMMARY (ORDERED BY PATIENT COUNT)")
        print("=" * 80)

        # Sort doctors by patient count in descending order
        sorted_doctors = sorted(
            doctors, key=lambda d: d.get_patient_count(), reverse=True
        )

        for idx, doctor in enumerate(sorted_doctors, 1):
            patient_count = doctor.get_patient_count()
            print(
                f"{idx}. {doctor.name} ({doctor.specialization}) - "
                f"Patients: {patient_count}"
            )

        print("=" * 80 + "\n")
