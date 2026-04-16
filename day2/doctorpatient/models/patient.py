"""Patient domain model for healthcare system."""

from typing import Optional


class Patient:
    """Represents a healthcare patient with medical condition.
    
    A patient has a disease/condition and is assigned to a doctor
    whose specialization matches the patient's disease.
    
    Attributes:
        name: Patient's full name
        disease: Medical condition/disease name
        email: Patient's email address
    """

    def __init__(self, name: str, disease: str, email: str) -> None:
        """Initialize a Patient instance.
        
        Args:
            name: Patient's full name
            disease: Medical condition/disease name
            email: Patient's contact email
        """
        self.name: str = name
        self.disease: str = disease
        self.email: str = email

    def get_info(self) -> str:
        """Get detailed information about the patient.
        
        Returns:
            Formatted patient information string
        """
        return (
            f"Patient: {self.name} | "
            f"Disease: {self.disease} | "
            f"Email: {self.email}"
        )

    def __str__(self) -> str:
        """Return string representation of patient.
        
        Returns:
            Formatted string with patient details
        """
        return self.get_info()
