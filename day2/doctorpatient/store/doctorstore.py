"""DoctorStore for data access and business logic layer."""

from typing import List, Dict, Optional
from faker import Faker
from ..models import Doctor, Patient


class DoctorStore:
    """Manages doctors, patients, and disease-to-specialization mapping.
    
    Handles:
    - Generation of random doctors and patients using Faker
    - Disease-to-specialization matching logic
    - Patient assignment to doctors based on disease
    - Data access and search functionality
    
    Attributes:
        doctors: List of all doctors in the system
        patients: List of all patients in the system
        fake: Faker instance for generating random data
        specialization_disease_map: Mapping of medical specializations to treatable diseases
    """

    # Disease-to-specialization mapping
    SPECIALIZATION_DISEASE_MAP = {
        "Cardiologist": ["Heart", "Cardiac", "Cardiovascular", "Hypertension"],
        "Orthopedist": ["Bone", "Joint", "Spine", "Fracture", "Arthritis"],
        "Neurologist": ["Brain", "Nerve", "Neurological", "Migraine", "Epilepsy"],
        "Dermatologist": ["Skin", "Dermatitis", "Psoriasis", "Acne", "Eczema"],
        "Gastroenterologist": ["Stomach", "Digestive", "Ulcer", "IBS", "Liver"],
        "Pulmonologist": ["Lung", "Respiratory", "Asthma", "COPD", "Pneumonia"],
        "Ophthalmologist": ["Eye", "Vision", "Cataract", "Glaucoma", "Myopia"],
        "Psychiatrist": ["Mental", "Depression", "Anxiety", "Bipolar", "Schizophrenia"],
    }

    def __init__(self, num_doctors: int = 10, num_patients: int = 50) -> None:
        """Initialize DoctorStore with empty collections.
        
        Args:
            num_doctors: Number of doctors to generate (default: 10)
            num_patients: Number of patients to generate (default: 50)
        """
        self.doctors: List[Doctor] = []
        self.patients: List[Patient] = []
        self.fake: Faker = Faker()

        # Auto-generate doctors and patients on initialization
        self.generate_doctors(num_doctors)
        self.generate_patients(num_patients)
        # Auto-assign patients to doctors based on disease matching
        self.assign_patients_by_disease()

    def generate_doctors(self, n: int = 10) -> None:
        """Generate random doctors with specializations.
        
        Args:
            n: Number of doctors to generate
        """
        specializations = list(self.SPECIALIZATION_DISEASE_MAP.keys())
        for _ in range(n):
            name = self.fake.name()
            specialization = self.fake.random_element(specializations)
            license_number = self.fake.bothify(text="LIC-????-####").upper()
            doctor = Doctor(name, specialization, license_number)
            self.doctors.append(doctor)

    def generate_patients(self, n: int = 50) -> None:
        """Generate random patients with diseases.
        
        Args:
            n: Number of patients to generate
        """
        all_diseases = []
        for diseases in self.SPECIALIZATION_DISEASE_MAP.values():
            all_diseases.extend(diseases)

        for _ in range(n):
            name = self.fake.name()
            disease = self.fake.random_element(all_diseases)
            email = self.fake.email()
            patient = Patient(name, disease, email)
            self.patients.append(patient)

    def assign_patients_by_disease(self) -> None:
        """Assign patients to doctors based on disease-specialization matching.
        
        This is the core business logic: each patient is assigned to one or more
        doctors whose specialization covers the patient's disease.
        """
        for patient in self.patients:
            for doctor in self.doctors:
                # Get list of diseases this doctor specializes in
                treatable_diseases = self.SPECIALIZATION_DISEASE_MAP.get(
                    doctor.specialization, []
                )
                # Assign patient if their disease matches doctor's specialization
                if patient.disease in treatable_diseases:
                    doctor.add_patient(patient)
                    break  # Assign to first matching doctor only

    def get_doctors(self) -> List[Doctor]:
        """Get all doctors in the system.
        
        Returns:
            List of all Doctor objects
        """
        return self.doctors

    def get_patients(self) -> List[Patient]:
        """Get all patients in the system.
        
        Returns:
            List of all Patient objects
        """
        return self.patients

    def get_doctor_by_specialization(
        self, specialization: str
    ) -> List[Doctor]:
        """Get all doctors with a specific specialization.
        
        Args:
            specialization: Medical specialization to search for
            
        Returns:
            List of doctors with matching specialization
        """
        return [
            doc for doc in self.doctors
            if doc.specialization.lower() == specialization.lower()
        ]

    def get_patients_for_specialization(self, specialization: str) -> List[Patient]:
        """Get all patients assigned to doctors with a specific specialization.
        
        Args:
            specialization: Medical specialization to search for
            
        Returns:
            List of patients assigned to doctors with this specialization
        """
        patients = []
        doctors = self.get_doctor_by_specialization(specialization)
        for doctor in doctors:
            patients.extend(doctor.get_patients())
        return patients

    def get_doctor_for_patient(self, patient_name: str) -> Optional[Doctor]:
        """Find the doctor assigned to a specific patient.
        
        Args:
            patient_name: Name of the patient to search for
            
        Returns:
            Doctor object if found, None otherwise
        """
        for doctor in self.doctors:
            for patient in doctor.get_patients():
                if patient.name.lower() == patient_name.lower():
                    return doctor
        return None

    def get_stats(self) -> Dict[str, int]:
        """Get statistics about the store.
        
        Returns:
            Dictionary with counts of doctors, patients, and total assignments
        """
        total_assignments = sum(
            doctor.get_patient_count() for doctor in self.doctors
        )
        return {
            "total_doctors": len(self.doctors),
            "total_patients": len(self.patients),
            "total_assignments": total_assignments,
            "unassigned_patients": len(self.patients) - total_assignments,
        }
