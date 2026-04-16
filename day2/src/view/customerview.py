#show customer details 
from store.customerstore import customerstore
class customerview:
    def __init__(self, store: customerstore):
        self.store = store

    def display_customers(self):
        customers = self.store.get_customers()
        for customer in customers:
            print(customer)