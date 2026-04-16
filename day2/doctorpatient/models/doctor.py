"""Doctor domain model for healthcare system."""

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .patient import Patient


class Doctor:
    """Represents a healthcare provider with specialization.
    
    A doctor has a specialization (e.g., Cardiologist, Orthopedist) and
    maintains a list of assigned patients.
    
    Attributes:
        name: Doctor's full name
        specialization: Medical specialization (e.g., "Cardiologist")
        license_number: Medical license identifier
        patients: List of Patient objects assigned to this doctor
    """

    def __init__(
        self, name: str, specialization: str, license_number: str
    ) -> None:
        """Initialize a Doctor instance.
        
        Args:
            name: Doctor's full name
            specialization: Medical specialization
            license_number: Medical license number
        """
        self.name: str = name
        self.specialization: str = specialization
        self.license_number: str = license_number
        self.patients: List["Patient"] = []

    def add_patient(self, patient: "Patient") -> None:
        """Add a patient to this doctor's roster.
        
        Args:
            patient: Patient object to assign to this doctor
        """
        if patient not in self.patients:
            self.patients.append(patient)

    def remove_patient(self, patient_id: int) -> bool:
        """Remove a patient from this doctor's roster.
        
        Args:
            patient_id: Index/ID of patient to remove
            
        Returns:
            True if patient was removed, False if patient not found
        """
        if 0 <= patient_id < len(self.patients):
            self.patients.pop(patient_id)
            return True
        return False

    def get_patients(self) -> List["Patient"]:
        """Get all patients assigned to this doctor.
        
        Returns:
            List of Patient objects
        """
        return self.patients

    def get_patient_count(self) -> int:
        """Get the number of patients assigned to this doctor.
        
        Returns:
            Number of patients
        """
        return len(self.patients)

    def __str__(self) -> str:
        """Return string representation of doctor.
        
        Returns:
            Formatted string with doctor details
        """
        return (
            f"Doctor: {self.name} | "
            f"Specialization: {self.specialization} | "
            f"License: {self.license_number} | "
            f"Patients: {self.get_patient_count()}"
        )
