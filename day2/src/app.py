# creating entry point for application
import faker
from store.customerstore import customerstore
from view.customerview import customerview


"""displaying a random name.
call the customer store and view """


def check():
    """this function creates an instance of the Faker class and prints a random name."""
    customer_store = customerstore(num_customers=100)
    customer_view = customerview(customer_store)
    customer_view.display_customers()


if __name__ == "__main__":
    check()
