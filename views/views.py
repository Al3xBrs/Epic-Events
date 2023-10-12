from .decorators import (
    log_decorator,
    error_decorator,
    menu_decorator,
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
        email = input("Your mail : ")
        password = input("Your pwd : ")

        return email, password

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
    def menu_sale():
        print(
            """
        1 - 
        """
        )

    @menu_decorator
    @staticmethod
    def menu_support():
        print(
            """
        1 - 
        """
        )

    @menu_decorator
    @staticmethod
    def menu_gesture():
        print(
            """
        1 - 
        """
        )
