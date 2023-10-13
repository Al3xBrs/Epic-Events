from .decorators import (
    log_decorator,
    error_decorator,
    menu_decorator,
    customers_decorator,
    contracts_decorator,
    events_decorator,
)


class MainView:
    @log_decorator
    @staticmethod
    def auth():
        print(
            """
        Please, enter your mail and your password.
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
        4 - Quit
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
        4 - Return Menu
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
        4 - Return Menu
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
        4 - Return Menu
        """
        )
        return input("CHOICE : ")
