#generate 100 customers 
import faker 
import typing
from models.customer import Customer
class customerstore:
    def __init__(self,num_customers:int=100):
        self.customers = []
        self.fake = faker.Faker()

    def generate_customers(self, n=100):
        for _ in range(n):
            name = self.fake.name()
            email = self.fake.email()
            dob = self.fake.date_of_birth()
            customer = Customer(name, email, dob)
            self.customers.append(customer)

    def get_customers(self) -> typing.List[Customer]:
        return self.customers