"""
create patient 
"""
class patient :
    def __init__(self, id, name ,dob, alinment):
        self.id = id
        self.name = name
        self.dob = dob
        self.alinment = alinment
        
    def __str__(self):
        return f"Patient(id='{self.id}', name='{self.name}', dob: '{self.dob}', alinment: '{self.alinment}')"