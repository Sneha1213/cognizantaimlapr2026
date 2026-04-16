"""
defining doctor class with id name and specializantion as attributes and __str__ method to return doctor details in string format
"""
class Doctor:
    def __init__(self, id,name, specialization):
        self.id = id
        self.name=name
        self.specialization = specialization

    def __str__(self):
        return f"Doctor(id='{self.id}', name='{self.name}', Specialization: '{self.specialization}')"