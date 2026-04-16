from datetime import datetime
from doctor import Doctor
from patient import patient
class Appointment:
    def __init__(self, id, doctor: Doctor, patient: patient, date_time: datetime):
        self.appointment_id = id
        self.date_time = date_time
        self.doctor = doctor
        self.patient = patient

    def __str__(self):
        return f"Appointment(id='{self.id}', doctor='{self.doctor.name}', patient='{self.patient.name}', date_time='{self.date_time}')"