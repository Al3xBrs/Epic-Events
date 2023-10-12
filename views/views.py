from .decorators import log_decorator, error_decorator


class MainView:
    @log_decorator
    @staticmethod
    def auth_view():
        print(
            """
        Please, enter your mail and your password.
        """
        )
        email = input("Your mail : ")
        password = input("Your pwd : ")

        print(email, password)
        print(type(email), type(password))

        return email, password

    @error_decorator
    @staticmethod
    def auth_error_view():
        print(
            """
        Error, can't find an user with this ... 
        """
        )
        return MainView.auth_view()
