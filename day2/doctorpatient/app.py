"""Main application entry point for DoctorPatient healthcare system."""

from doctorpatient.store import DoctorStore
from doctorpatient.view import DoctorView


def check() -> None:
    """Main orchestration function.
    
    Executes the complete healthcare system workflow:
    1. Create DoctorStore and auto-generate doctors and patients
    2. Auto-assign patients to doctors based on disease-specialization matching
    3. Create DoctorView for presentation
    4. Display various views and search results
    """
    print("\n" + "=" * 80)
    print("DOCTOR-PATIENT HEALTHCARE SYSTEM")
    print("=" * 80)

    # Step 1: Initialize store (this auto-generates doctors, patients, and assigns)
    print("\nInitializing healthcare system...")
    print("Generating 10 doctors and 50 patients...")
    store = DoctorStore(num_doctors=10, num_patients=50)

    # Step 2: Create view with dependency injection
    view = DoctorView(store)

    # Step 3: Display statistics
    view.display_statistics()

    # Step 4: Display all doctors with their patients
    view.display_all_doctors_with_patients()

    # Step 5: Display all patients with their doctors
    view.display_all_patients_with_doctors()

    # Step 6: Display doctor summary
    view.display_summary()

    # Step 7: Search demonstrations
    print("\n" + "=" * 80)
    print("SEARCH DEMONSTRATIONS")
    print("=" * 80)

    # Search for cardiologists and their patients
    view.search_patients_for_specialization("Cardiologist")

    # Search for orthopedists and their patients
    view.search_patients_for_specialization("Orthopedist")

    # Search for a specific patient's doctor (using first patient)
    if store.get_patients():
        first_patient = store.get_patients()[0]
        view.search_doctor_for_patient(first_patient.name)

    print("=" * 80)
    print("Healthcare system demonstration complete!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    check()
