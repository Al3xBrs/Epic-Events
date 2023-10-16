from .decorators import (
    log_decorator,
    error_decorator,
    menu_decorator,
    customers_decorator,
    contracts_decorator,
    events_decorator,
    filter_decorator,
    create_decorator,
    update_decorator,
    delete_decorator,
    select_one_decorator,
)


class MainView:
    @log_decorator
    @staticmethod
    def auth():
        print(
            """
        Please, enter your username and your password.
        """
        )
        username = input("Your username : ")
        password = input("Your pwd : ")

        return username, password

    @error_decorator
    @staticmethod
    def auth_error():
        print(
            """
        Error, can't find any user with this ... 
        """
        )

    @menu_decorator
    @staticmethod
    def menu():
        print(
            """
        1 - Customers 
        2 - Contracts 
        3 - Events
        4 - Collaborators

        5 - Select One

        6 - Quit
        """
        )
        return input("CHOICE : ")


class SubmenuView:
    @customers_decorator
    @staticmethod
    def customers():
        print(
            """ 
        1 - All Customers
        2 - Your Customers

        3 - Create 
        4 - Filter

        5 - Return Menu
        """
        )
        return input("CHOICE : ")

    @customers_decorator
    @staticmethod
    def all_customers(customers_list):
        print(
            f""" 
        {customers_list}
        1 - Your Customers

        2 - Create 
        3 - Filter

        4 - Return Menu
        """
        )
        return input("CHOICE : ")

    @customers_decorator
    @staticmethod
    def your_customers(customers_list):
        print(
            f""" 
        {customers_list}
        1 - Select One
        2 - All Customers
        3 - Create
        4 - Filter
        5 - Return Menu
        """
        )
        return input("CHOICE : ")

    @contracts_decorator
    @staticmethod
    def contracts():
        print(
            """ 
        1 - All Contracts
        2 - Your Contracts

        3 - Create
        4 - Filter

        5 - Return Menu
        """
        )
        return input("CHOICE : ")

    @events_decorator
    @staticmethod
    def events():
        print(
            """ 
        1 - All Events
        2 - Your Events

        3 - Create
        4 - Filter

        5 - Return Menu
        """
        )
        return input("CHOICE : ")

    @select_one_decorator
    @staticmethod
    def select_one():
        print(
            """ 
        Choose the object to find, THEN, the information, THEN, the value
        """
        )
        obj = input("SELECT THE OBJECT (customer, contract or event) : ")
        information = input("SELECT THE INFORMATION (ex : name) : ")
        value = input("TYPE THE VALUE (ex : Alex) : ")

        return obj, information, value

    @customers_decorator
    @staticmethod
    def find_one(obj):
        print(
            f""" 
        {obj}
        1 - Update
        2 - Delete

        3 - Return
        """
        )
        return input("CHOICE : ")


class FilterView:
    @filter_decorator
    @staticmethod
    def customers_filter():
        print(
            """ 
        1 - Name (Alphabetical)
        2 - Company (Alphabetical)

        3 - Create Date (Most Recent)
        4 - Create Date (Less Recent)

        5 - Update Date (Most Recent)
        6 - Update Date (Less Recent)

        7 - Sales Person (Alphabetical)
        """
        )
        return input("CHOICE : ")

    @filter_decorator
    @staticmethod
    def contracts_filter():
        print(
            """ 
        1 - Customers (Alphabetical)
        2 - Sales Person (Alphabetical)

        3 - Price (Most Expensive)
        4 - Price (Less Expensive)

        5 - Create Date (Most Recent)
        6 - Create Date (Less Recent)

        7 - Status (Sign)
        8 - Status (Not Sign)
        """
        )
        return input("CHOICE : ")

    @filter_decorator
    @staticmethod
    def events_filter():
        print(
            """ 
        1 - Customers (Alphabetical)
        2 - Support Person (Alphabetical)

        3 - Start Date (Most Recent)
        4 - Stat Date (Less Recent)

        5 - End Date (Most Recent)
        6 - End Date (Less Recent)

        7 - Attendees (Most)
        8 - Attendees (Less)
        """
        )
        return input("CHOICE : ")

    @filter_decorator
    @staticmethod
    def collaborators_filter():
        print(
            """ 
        1 - Username (Alphabetical)
        2 - Role (Alphabetical)
        """
        )
        return input("CHOICE : ")


class CRUDView:
    @create_decorator
    @staticmethod
    def create():
        print(
            """ 
        Leave blank if don't need
        (m) : mandatory

        Customer (m): name, email, phone, company, sales_person
        Contract (m): name, sales_person, price
        Event (m): contract_id, name, start_date, end_date, location, attendees
        """
        )
        name = input("NAME : ")
        email = input("EMAIL : ")
        phone = input("PHONE : ")
        company = input("COMPANY : ")
        sales_person = input("SALES PERSON : ")
        price = input("PRICE : ")
        contract_id = input("CONTRACT ID : ")
        start_date = input("START DATE : ")
        end_date = input("END DATE : ")
        location = input("LOCATION : ")
        attendees = input("ATTENDEES : ")

        return (
            name,
            email,
            phone,
            company,
            sales_person,
            price,
            contract_id,
            start_date,
            end_date,
            location,
            attendees,
        )

    @update_decorator
    @staticmethod
    def update(informations):
        print(
            f"""
        {informations} 
        Choose the information to update, THEN, write the update.

        Ex : 
            INFORMATION TO UPDATE : name
            NEW UPDATE : Alex
        """
        )
        to_update = input("INFORMATION TO UPDATE : ")
        new_update = input("NEW UPDATE : ")

        return to_update, new_update

    @delete_decorator
    @staticmethod
    def delete(obj):
        print(
            f"""
        {obj} 
        Are you sure to delete ? (Y/N)
        """
        )

        return input("CHOISE : ")
