"""
create the doctor CRUD operation
"""

from logging import info
import os
import sys
import sys

from model.doctor import Doctor
from exceptions.doctor_not_found_exception import DoctorNotFoundException
 
#add project root tp python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(project_root)
 
from conf.logger_conf import setup_logger
"""
entry point for the healthcare application
"""
logger = setup_logger()
class DoctorStore:

    def __init__(self):
        self.doctors = []

    def add_doctor(self, doctor: Doctor):
        logger.info(f"Adding doctor: {doctor}")
        self.doctors.append(doctor)

    def get_all_doctors(self):
        logger=info("Retrieving all doctors")   
        return self.doctors

    def get_doctor_by_id(self, doctor_id):
        logger=info(f"Retrieving doctor with id: {doctor_id}")
        for doctor in self.doctors:
            if doctor.id == doctor_id:
                return doctor
        raise DoctorNotFoundException(f"Doctor with id {doctor_id} not found")
    def update_doctor(self, doctor_id, updated_doctor: Doctor):
        

                
        return None