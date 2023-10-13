from views.views import MainView, SubmenuView
from .permissions import (
    is_authenticated,
    is_sale,
    is_support,
    is_gesture,
)


class MainController:
    """ """

    @classmethod
    def auth_controller(cls, payload):
        username, pwd = MainView.auth()
        # adapt
        log = ["aa"]
        # TODO : Check for user in db
        # user.is_autenticated = True

        # if is_authenticated(user):
        #     if is_gesture(user):
        #         return "ss", payload
        #     if is_sale(user):
        #         return "ss", payload
        #     if is_support(user):
        #         return "ss", payload

        if username + pwd in log:
            return "menu_controller", payload
        else:
            MainView.auth_error()
            return "auth_controller", payload

    @classmethod
    def menu_controller(cls, payload):
        choice = MainView.menu()

        if choice == "1":
            return "customers_controller", payload

        elif choice == "2":
            return "contracts_controller", payload

        elif choice == "3":
            return "events_controller", payload

        elif choice == "4":
            return "auth_controller", payload


class SubmenuController:
    @classmethod
    def customers_controller(cls, payload):
        choice = SubmenuView.customers()

        if choice == "4":
            return "menu_controller", payload

    @classmethod
    def contracts_controller(cls, payload):
        choice = SubmenuView.contracts()

        if choice == "4":
            return "menu_controller", payload

    @classmethod
    def events_controller(cls, payload):
        choice = SubmenuView.events()

        if choice == "4":
            return "menu_controller", payload
