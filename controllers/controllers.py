import datetime
from email.policy import default
from pydoc import cli
import uuid
import psycopg2
from decouple import config
from views.views import (
    CRUDView,
    ContractsView,
    EventsView,
    MainView,
    SubmenuView,
    ErrorView,
    CustomersView,
)
from .permissions import (
    is_authenticated,
    is_sale,
    is_support,
    is_gesture,
)
import bcrypt
import jwt

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
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd.encode("utf-8"), salt)

        query = "SELECT username, password, role FROM collaborater WHERE username = %s"
        cur.execute(query, (username,))
        user = cur.fetchone()

        if user:
            stored_pwd = user[1]
            if bcrypt.checkpw(hashed, stored_pwd.encode("utf-8")):
                key = config("KEY")
                token = jwt.encode(
                    {"username": username, "role": user[2]}, key, algorithm="H256"
                )
                payload["token"] = token
                return "menu_controller", payload

            else:
                ErrorView.auth_error()
                return "auth_controller", payload
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

        if choice == "1":
            return "all_contracts_controller", payload
        elif choice == "2":
            return "your_contracts_controller", payload
        elif choice == "3":
            return "create_controller", payload
        elif choice == "4":
            return "filter_controller", payload
        elif choice == "5":
            return "menu_controller", payload
        else:
            ErrorView.choice_error()
            return "contracts_controller", payload

    @classmethod
    def events_controller(cls, payload):
        choice = SubmenuView.events()

        if choice == "1":
            return "all_events_controller", payload
        elif choice == "2":
            return "your_events_controller", payload
        elif choice == "3":
            return "create_controller", payload
        elif choice == "4":
            return "filter_controller", payload
        elif choice == "5":
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
        query = (
            f"SELECT name, email, company FROM customer WHERE commercial_username = %s"
        )
        cur.execute(query, (commercial_username,))
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


class ContractController:
    @classmethod
    def all_contracts_controller(cls, payload):
        query = "SELECT customer_name, commercial_username, price, create_date, status FROM contract"
        cur.execute(query)
        contracts_list = cur.fetchall()
        payload["contracts_list"] = contracts_list

        if contracts_list:
            choice = ContractsView.all_contracts(contracts_list)
            if choice == "1":
                return "your_contracts_controller", payload
            if choice == "2":
                return "create_controller", payload
            if choice == "3":
                return "filter_controller", payload
            if choice == "4":
                return "contracts_controller", payload
            else:
                ErrorView.choice_error()
                return "all_contracts_controller", payload
        else:
            ErrorView.query_not_find()
            return "contracts_controller", payload

    @classmethod
    def your_contracts_controller(cls, payload):
        commercial_username = "TESTCOLL"
        query = "SELECT customer_name, commercial_username, price, create_date, status FROM contract WHERE commercial_username = %s"
        cur.execute(query, (commercial_username,))
        contracts_list = cur.fetchall()
        payload["your_contracts"] = contracts_list

        if contracts_list:
            choice = ContractsView.your_contracts(contracts_list)
            if choice == "1":
                return "all_contracts_controller", payload
            elif choice == "2":
                return "create_controller", payload
            elif choice == "3":
                return "filter_controller", payload
            elif choice == "4":
                return "contracts_controller", payload
            else:
                ErrorView.choice_error()
                return "your_contracts_controller", payload

        else:
            ErrorView.query_not_find()
            return "your_contracts_controller", payload


class EventController:
    @classmethod
    def all_events_controller(cls, payload):
        query = "SELECT customer_name, start_date, end_date, support_username, location, attendees, description FROM event"
        cur.execute(query)
        events_list = cur.fetchall()
        payload["events_list"] = events_list

        choice = EventsView.all_events(events_list)
        if events_list:
            if choice == "1":
                return "your_events_controller", payload
            elif choice == "2":
                return "create_controller", payload
            elif choice == "3":
                return "filter_controller", payload
            elif choice == "4":
                return "events_controller", payload
            else:
                ErrorView.choice_error()
                return "all_events_controller", payload
        else:
            ErrorView.query_not_find()
            return "events_controller", payload

    @classmethod
    def your_events_controller(cls, payload):
        commercial_username = "TESTCOLL"
        query = "SELECT customer_name, start_date, end_date, support_username, location, attendees, description FROM event WHERE support_username = %s"
        cur.execute(query, (commercial_username,))
        events_list = cur.fetchall()
        payload["events_list"] = events_list

        choice = EventsView.your_events(events_list)
        if events_list:
            if choice == "1":
                return "all_events_controller", payload
            elif choice == "2":
                return "create_controller", payload
            elif choice == "3":
                return "filter_controller", payload
            elif choice == "4":
                return "events_controller", payload
            else:
                ErrorView.choice_error()
                return "all_events_controller", payload
        else:
            ErrorView.query_not_find()
            return "events_controller", payload


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
