#define customer model 
import typing
import datetime
class Customer:
    def __init__(self, name: str, email: str, dob: datetime.date):
        self.name = name
        self.email = email
        self.dob = dob


    def __str__(self):
        return f"Customer(name={self.name}, email={self.email}, dob={self.dob})"