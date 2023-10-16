import psycopg2
from decouple import config
from views.views import MainView, SubmenuView, ErrorView
from .permissions import (
    is_authenticated,
    is_sale,
    is_support,
    is_gesture,
)

conn = psycopg2.connect(
    user=config("DB_USER"),
    password=config("DB_PASSWORD"),
    host=config("DB_HOST"),
    database=config("DB_NAME"),
    port="5432",
)
cur = conn.cursor()


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
            ErrorView.auth_error()
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

        elif choice == "6":
            return "auth_controller", payload


class SubmenuController:
    @classmethod
    def customers_controller(cls, payload):
        choice = SubmenuView.customers()

        if choice == "1":
            return "all_customers_controller", payload
        elif choice == "2":
            return "your_customers_controller", payload
        elif choice == "3":
            return "create_controller", payload
        elif choice == "4":
            return "filter_controller", payload
        elif choice == "5":
            return "menu_controller", payload

    @classmethod
    def all_customers_controller(cls, payload):
        query = "SELECT name, email, company FROM customer"
        cur.execute(query)
        customers_list = cur.fetchall()
        payload["customers_list"] = customers_list

        if customers_list:
            choice = SubmenuView.all_customers(customers_list)
            if choice == "1":
                return "your_customers_controller", payload
            elif choice == "2":
                return "create_controller", payload
            elif choice == "3":
                return "filter_controller", payload
            elif choice == "4":
                return "customers_controller", payload
            else:
                print("Please, select 1/2/3/4")
                return "all_customers_controller", payload
        else:
            ErrorView.query_not_find()
            return "customers_controller", payload

    @classmethod
    def contracts_controller(cls, payload):
        choice = SubmenuView.contracts()

        if choice == "5":
            return "menu_controller", payload

    @classmethod
    def events_controller(cls, payload):
        choice = SubmenuView.events()

        if choice == "5":
            return "menu_controller", payload
