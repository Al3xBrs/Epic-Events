import datetime
import uuid
import psycopg2
from decouple import config
from views.views import CRUDView, MainView, SubmenuView, ErrorView, CustomersView
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

        elif choice == "4":
            return "collaborators_controller", payload

        elif choice == "5":
            return "select_one_controller", payload

        elif choice == "6":
            return "auth_controller", payload
        else:
            ErrorView.choice_error()
            return "menu_controller", payload


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
        else:
            ErrorView.choice_error()
            return "customers_controller", payload

    @classmethod
    def contracts_controller(cls, payload):
        choice = SubmenuView.contracts()

        if choice == "5":
            return "menu_controller", payload
        else:
            ErrorView.choice_error()
            return "contracts_controller", payload

    @classmethod
    def events_controller(cls, payload):
        choice = SubmenuView.events()

        if choice == "5":
            return "menu_controller", payload
        else:
            ErrorView.choice_error()
            return "events_controller", payload

    @classmethod
    def find_one_controller(cls, payload):
        obj = payload["obj"]
        choice = SubmenuView.find_one(obj)
        if choice == "1":
            return "update_controller", payload
        elif choice == "2":
            return "delete_controller", payload
        elif choice == "3":
            return "menu_controller", payload


class CustomerController:
    @classmethod
    def all_customers_controller(cls, payload):
        query = "SELECT name, email, company FROM customer"
        cur.execute(query)
        customers_list = cur.fetchall()
        payload["customers_list"] = customers_list

        if customers_list:
            choice = CustomersView.all_customers(customers_list)
            if choice == "1":
                return "your_customers_controller", payload
            elif choice == "2":
                return "create_controller", payload
            elif choice == "3":
                return "filter_controller", payload
            elif choice == "4":
                return "customers_controller", payload
            else:
                ErrorView.choice_error()
                return "all_customers_controller", payload
        else:
            ErrorView.query_not_find()
            return "customers_controller", payload

    @classmethod
    def your_customers(cls, payload):
        commercial_username = "TESTCOLL"
        query = f"SELECT name, email, company FROM customer WHERE commercial_username = '{commercial_username}'"
        cur.execute(query)
        customers_list = cur.fetchall()
        payload["your_customers"] = customers_list

        if customers_list:
            choice = CustomersView.your_customers(customers_list)
            if choice == "1":
                return "all_customers_controller", payload
            elif choice == "2":
                return "create_controller", payload
            elif choice == "3":
                return "filter_controller", payload
            elif choice == "4":
                return "customers_controller", payload
            else:
                ErrorView.choice_error()
                return "your_customers_controller", payload

        else:
            ErrorView.query_not_find()
            return "your_customers_controller", payload


class CRUDController:
    @classmethod
    def create_controller(cls, payload):
        (
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
        ) = CRUDView.create()
        id = uuid.uuid1()
        now = datetime.datetime.now()
        create_date = now.strftime("%m-%-d-%Y")
        update_date = now.strftime("%m-%d-%Y %H:%M:%S")
        commercial_username = "TESTCOLL"
        query = f"INSERT INTO customer (id, name, email, phone, company, create_date, update_date, commercial_username) VALUES ('{id}', '{name}', '{email}', {phone}, '{company}', '{create_date}', '{update_date}', '{commercial_username}') RETURNING *"
        cur.execute(query)
        conn.commit()
        obj = cur.fetchone()
        payload["obj"] = obj
        return "find_one_controller", payload

    # TODO
    @classmethod
    def delete_controller(cls, payload):
        pass

    # TODO
    @classmethod
    def update_controller(cls, payload):
        pass
