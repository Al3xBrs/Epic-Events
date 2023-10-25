import datetime
from email.policy import default
from genericpath import exists
from pydoc import cli
import string
import uuid
import psycopg2
from decouple import config
from views.views import (
    CRUDView,
    ContractsView,
    EventsView,
    FilterView,
    MainView,
    SubmenuView,
    ErrorView,
    CustomersView,
    CollaboratorsView,
)
from .permissions import (
    is_sale,
    is_support,
    is_gesture,
    is_sign,
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


def decode_jws(token):
    key = config("KEY")
    result = jwt.decode(token, key, algorithms=["HS256"])
    return result


class MainController:
    """ """

    @classmethod
    def auth_controller(cls, payload):
        username, pwd = MainView.auth()
        query = "SELECT username, password, role FROM collaborater WHERE username = %s"
        cur.execute(query, (username,))
        user = cur.fetchone()

        if user:
            stored_pwd = user[1]
            if bcrypt.checkpw(pwd.encode("UTF-8"), stored_pwd.encode("UTF-8")):
                key = config("KEY")
                token = jwt.encode(
                    {"username": user[0], "role": user[2]}, key, algorithm="HS256"
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
            return "all_collaborators_controller", payload

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
        token = decode_jws(payload["token"])
        role = token["role"]
        if choice == "1":
            return "all_customers_controller", payload
        elif choice == "2":
            return "your_customers_controller", payload
        elif choice == "3":
            if is_sale(role):
                payload["table"] = "customer"
                return "create_controller", payload
            else:
                ErrorView.role_error()
                return "customers_controller", payload
        elif choice == "4":
            payload["table"] = "customer"
            payload["all_your"] = "all"
            payload["fields"] = "name, email, company"
            return "filter_controller", payload
        elif choice == "5":
            return "menu_controller", payload
        else:
            ErrorView.choice_error()
            return "customers_controller", payload

    @classmethod
    def contracts_controller(cls, payload):
        choice = SubmenuView.contracts()
        token = decode_jws(payload["token"])
        role = token["role"]

        if choice == "1":
            return "all_contracts_controller", payload
        elif choice == "2":
            return "your_contracts_controller", payload
        elif choice == "3":
            if is_gesture(role):
                payload["table"] = "contract"
                return "create_controller", payload
            else:
                ErrorView.role_error()
                return "contracts_controller", payload
        elif choice == "4":
            payload["table"] = "contract"
            payload["all_your"] = "all"
            payload[
                "fields"
            ] = "customer_name, commercial_username, price, create_date, status"
            return "filter_controller", payload
        elif choice == "5":
            return "menu_controller", payload
        else:
            ErrorView.choice_error()
            return "contracts_controller", payload

    @classmethod
    def events_controller(cls, payload):
        choice = SubmenuView.events()
        token = decode_jws(payload["token"])
        role = token["role"]
        if choice == "1":
            return "all_events_controller", payload
        elif choice == "2":
            return "your_events_controller", payload
        elif choice == "3":
            if is_gesture(role):
                payload["table"] = "event"
                return "create_controller", payload
            else:
                ErrorView.role_error()
                return "events_controller", payload
        elif choice == "4":
            payload["table"] = "event"
            payload["all_your"] = "all"
            payload[
                "fields"
            ] = "customer_name, start_date, end_date, support_username, location, attendees, description"
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

    @classmethod
    def select_one_controller(cls, payload):
        table, information, value = SubmenuView.select_one()
        try:
            if isinstance(value, str):
                query = f"SELECT * FROM {table} WHERE {information} = '{value}'"
                cur.execute(query)
                obj = cur.fetchone()
                if obj:
                    payload["table"] = table
                    payload["obj"] = obj
                    return "find_one_controller", payload
            else:
                query = f"SELECT * FROM {table} WHERE {information} = {value}"
                cur.execute(query)
                obj = cur.fetchone()
                if obj:
                    payload["table"] = table
                    payload["obj"] = obj
                    return "find_one_controller", payload

        except:
            ErrorView.fields()
            return "select_one_controller", payload


class CustomerController:
    @classmethod
    def all_customers_controller(cls, payload):
        if "filter_list" in payload:
            customers_list = payload["filter_list"]
            del payload["filter_list"]
        else:
            query = "SELECT name, email, company FROM customer"
            cur.execute(query)
            customers_list = cur.fetchall()

        token = decode_jws(payload["token"])
        role = token["role"]

        if customers_list:
            choice = CustomersView.all_customers(customers_list)
            if choice == "1":
                return "your_customers_controller", payload
            elif choice == "2":
                if is_sale(role):
                    payload["table"] = "customer"
                    return "create_controller", payload
                else:
                    ErrorView.role_error()
                    return "all_customers_controller", payload
            elif choice == "3":
                payload["table"] = "customer"
                payload["all_your"] = "all"
                payload["fields"] = "name, email, company"
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
        token = decode_jws(payload["token"])
        role = token["role"]
        if "filter_list" in payload:
            customers_list = payload["filter_list"]
            del payload["filter_list"]
        else:
            commercial_username = token["username"]
            query = f"SELECT name, email, company FROM customer WHERE commercial_username = %s"
            cur.execute(query, (commercial_username,))
            customers_list = cur.fetchall()

        if is_sale(role) or is_gesture(role):
            if customers_list:
                choice = CustomersView.your_customers(customers_list)
                if choice == "1":
                    return "all_customers_controller", payload
                elif choice == "2":
                    payload["table"] = "customer"
                    return "create_controller", payload
                elif choice == "3":
                    payload["table"] = "customer"
                    payload["all_your"] = "your"
                    payload["fields"] = "name, email, company"
                    return "filter_controller", payload
                elif choice == "4":
                    return "customers_controller", payload
                else:
                    ErrorView.choice_error()
                    return "your_customers_controller", payload

            else:
                ErrorView.query_not_find()
                return "customers_controller", payload
        else:
            ErrorView.role_error()
            return "customers_controller", payload


class ContractController:
    @classmethod
    def all_contracts_controller(cls, payload):
        if "filter_list" in payload:
            contracts_list = payload["filter_list"]
            del payload["filter_list"]
        else:
            query = "SELECT customer_name, commercial_username, price, create_date, status FROM contract"
            cur.execute(query)
            contracts_list = cur.fetchall()

        token = decode_jws(payload["token"])
        role = token["role"]
        if contracts_list:
            choice = ContractsView.all_contracts(contracts_list)
            if choice == "1":
                return "your_contracts_controller", payload
            if choice == "2":
                if is_gesture(role):
                    payload["table"] = "contract"
                    return "create_controller", payload
                else:
                    ErrorView.role_error()
                    return "all_contracts_controller", payload
            if choice == "3":
                payload["table"] = "contract"
                payload["all_your"] = "all"
                payload[
                    "fields"
                ] = "customer_name, commercial_username, price, create_date, status"
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
        token = decode_jws(payload["token"])
        role = token["role"]
        if is_gesture(role) or is_sale(role):
            commercial_username = token["username"]
            if "filter_list" in payload:
                contracts_list = payload["filter_list"]
                del payload["filter_list"]

            else:
                query = "SELECT customer_name, commercial_username, price, create_date, status FROM contract WHERE commercial_username = %s"
                cur.execute(query, (commercial_username,))
                contracts_list = cur.fetchall()

            if contracts_list:
                choice = ContractsView.your_contracts(contracts_list)
                if choice == "1":
                    return "all_contracts_controller", payload
                elif choice == "2":
                    payload["table"] = "contract"
                    return "create_controller", payload
                elif choice == "3":
                    payload["table"] = "contract"
                    payload["all_your"] = "your"
                    payload[
                        "fields"
                    ] = "customer_name, commercial_username, price, create_date, status"
                    return "filter_controller", payload
                elif choice == "4":
                    return "contracts_controller", payload
                else:
                    ErrorView.choice_error()
                    return "your_contracts_controller", payload

            else:
                ErrorView.query_not_find()
                return "contracts_controller", payload


class EventController:
    @classmethod
    def all_events_controller(cls, payload):
        if "filter_list" in payload:
            events_list = payload["filter_list"]
            del payload["filter_list"]
        else:
            query = "SELECT customer_name, start_date, end_date, support_username, location, attendees, description FROM event"
            cur.execute(query)
            events_list = cur.fetchall()

        choice = EventsView.all_events(events_list)
        if events_list:
            if choice == "1":
                return "your_events_controller", payload
            elif choice == "2":
                payload["table"] = "event"
                return "create_controller", payload
            elif choice == "3":
                payload["table"] = "event"
                payload["all_your"] = "all"
                payload[
                    "fields"
                ] = "customer_name, start_date, end_date, support_username, location, attendees, description"
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
        token = decode_jws(payload["token"])
        role = token["role"]

        if is_support(role):
            commercial_username = token["username"]
            if "filter_list" in payload:
                events_list = payload["filter_list"]
                del payload["filter_list"]
            else:
                query = "SELECT customer_name, start_date, end_date, support_username, location, attendees, description FROM event WHERE support_username = %s"
                cur.execute(query, (commercial_username,))
                events_list = cur.fetchall()

            choice = EventsView.your_events(events_list)
            if events_list:
                if choice == "1":
                    return "all_events_controller", payload
                elif choice == "2":
                    payload["table"] = "event"
                    return "create_controller", payload
                elif choice == "3":
                    payload["table"] = "event"
                    payload["all_your"] = "your"
                    payload[
                        "fields"
                    ] = "customer_name, start_date, end_date, support_username, location, attendees, description"
                    return "filter_controller", payload
                elif choice == "4":
                    return "events_controller", payload
                else:
                    ErrorView.choice_error()
                    return "all_events_controller", payload
            else:
                ErrorView.query_not_find()
                return "events_controller", payload
        else:
            ErrorView.role_error()
            return "events_controller", payload


class CollaboratorController:
    @classmethod
    def all_collaborators(cls, payload):
        token = decode_jws(payload["token"])
        role = token["role"]
        if "filter_list" in payload:
            collaborators_list = payload["filter_list"]
            del payload["filter_list"]
        else:
            query = "SELECT phone, email, username, role FROM collaborater"
            cur.execute(query)
            collaborators_list = cur.fetchall()

        choice = CollaboratorsView.all_collaborators(collaborators_list)

        if choice == "1":
            return "update_controller", payload
        elif choice == "2":
            if is_gesture(role):
                payload["table"] = "collaborater"
                return "create_controller", payload
            else:
                ErrorView.role_error()
                return "all_collaborators_controller", payload
        elif choice == "3":
            payload["table"] = "collaborater"
            payload["all_your"] = "all"
            payload["fields"] = "phone, email, username, role"
            return "filter_controller", payload
        elif choice == "4":
            return "menu_controller", payload
        else:
            ErrorView.choice_error()
            return "all_collaborators_controller", payload


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
            description,
            role,
            password,
        ) = CRUDView.create()
        id = uuid.uuid1()
        now = datetime.datetime.now()
        create_date = now.strftime("%m-%-d-%Y")
        update_date = now.strftime("%m-%d-%Y %H:%M:%S")
        salt = bcrypt.gensalt()
        pwd = bcrypt.hashpw(password.encode("UTF-8"), salt)
        pwd_v = pwd.decode("UTF-8")
        token = decode_jws(token=payload["token"])
        commercial_username = token["username"]
        table = payload["table"]
        status = False
        if table == "collaborater":
            fields = "(id, phone, email, username, password, role)"
            values = f"('{id}', {phone}, '{email}', '{name}', '{pwd_v}', '{role}')"
        elif table == "contract":
            fields = (
                "(id, customer_name, commercial_username, price, create_date, status)"
            )
            values = f"('{id}', '{name}', '{sales_person}', {price}, '{create_date}', {status})"

        elif table == "customer":
            fields = "(id, name, email, phone, company, create_date, update_date, commercial_username)"
            values = f"('{id}', '{name}', '{email}', {phone}, '{company}', '{create_date}', '{update_date}', '{commercial_username}')"
        elif table == "event":
            try:
                query = f"SELECT status FROM contract WHERE id = '{contract_id}' AND status = True"
                cur.execute(query)
                contract_status = cur.fetchone()
            except:
                ErrorView.contract_id()
                return "contracts_controller", payload
            if contract_status:
                fields = "(id, contract_id, customer_name, start_date, end_date, location, attendees, description)"
                values = f"('{id}', '{contract_id}', '{name}', '{start_date}', '{end_date}', '{location}', '{attendees}', '{description}')"
            else:
                ErrorView.status()
                return "contracts_controller", payload
        else:
            ErrorView.table_error()
            return "create_controller", payload

        query = f"INSERT INTO {table} {fields} VALUES {values} RETURNING *"

        cur.execute(query)
        conn.commit()
        obj = cur.fetchone()
        payload["obj"] = obj

        return "find_one_controller", payload

        ErrorView.fields()
        return "menu_controller", payload

    @classmethod
    def delete_controller(cls, payload):
        obj = payload["obj"]
        table = payload["table"]
        choice = CRUDView.delete(obj)

        if choice == "Y" or "y":
            id = obj[0]
            query = f"DELETE FROM {table} WHERE id = '{id}'"
            cur.execute(query)
            conn.commit()
            del payload["obj"]
            del payload["table"]
            return "menu_controller", payload

        elif choice == "N" or "n":
            return "find_one_controller", payload

        else:
            ErrorView.yn()
            return "delete_controller", payload

    @classmethod
    def update_controller(cls, payload):
        table = payload["table"]
        obj = payload["obj"]
        to_update, new_update = CRUDView.update(obj)
        id = obj[0]
        now = datetime.datetime.now()
        update_date = now.strftime("%m-%-d-%Y")
        if obj:
            if isinstance(new_update, str) and table == "customer":
                query = f"UPDATE {table} SET {to_update} = '{new_update}', update_date = '{update_date}' WHERE id = '{id}'"
                cur.execute(query)
                conn.commit()
            elif isinstance(new_update, int) and table == "customer":
                query = f"UPDATE {table} SET {to_update} = {new_update}, update_date = '{update_date}' WHERE id = '{id}'"
                cur.execute(query)
                conn.commit()
            elif isinstance(new_update, str) and table != "customer":
                query = (
                    f"UPDATE {table} SET {to_update} = '{new_update}' WHERE id = '{id}'"
                )
                cur.execute(query)
                conn.commit()

            else:
                query = (
                    f"UPDATE {table} SET {to_update} = {new_update} WHERE id = '{id}'"
                )
                cur.execute(query)
                conn.commit()
            return "menu_controller", payload
        else:
            ErrorView.fields()
            return "update_controller", payload


class FilterController:
    @classmethod
    def filter_controller(cls, payload):
        table = payload["table"]
        all_your = payload["all_your"]
        fields = payload["fields"]
        token = decode_jws(payload["token"])
        collaborator = token["username"]
        order = None
        if table == "customer":
            choice = FilterView.customers_filter()

            if choice == "1":
                order = "name"

            elif choice == "2":
                order = "company"

            elif choice == "3":
                order = "create_date ASC"

            elif choice == "4":
                order = "create_date DESC"

            elif choice == "5":
                order = "update_date ASC"

            elif choice == "6":
                order = "update_date DESC"

            elif choice == "7":
                order = "commercial_username"

            else:
                ErrorView.choice_error()
                return "filter_controller", payload

            if order is not None and all_your == "all":
                query = f"SELECT {fields} FROM {table} ORDER BY {order}"
                cur.execute(query)
                customers_list = cur.fetchall()

                if customers_list:
                    payload["filter_list"] = customers_list
                    return "all_customers_controller", payload

            elif order is not None and all_your == "your":
                query = f"SELECT {fields} FROM {table} WHERE commercial_username = '{collaborator}' ORDER BY {order}"
                cur.execute(query)
                customers_list = cur.fetchall()
                if customers_list:
                    payload["filter_list"] = customers_list
                    return "your_customers_controller", payload

            ErrorView.query_not_find()
            return "customers_controller", payload
        if table == "contract":
            choice = FilterView.contracts_filter()

            if choice == "1":
                order = "customer_name"

            elif choice == "2":
                order = "commercial_username"

            elif choice == "3":
                order = "price DESC"

            elif choice == "4":
                order = "price ASC"

            elif choice == "5":
                order = "create_date DESC"

            elif choice == "6":
                order = "create_date ASC"

            elif choice == "7":
                order = "status DESC"

            elif choice == "8":
                order = "status ASC"

            else:
                ErrorView.choice_error()
                return "contracts_controller", payload

            if order is not None and all_your == "all":
                query = f"SELECT {fields} FROM {table} ORDER BY {order}"
                cur.execute(query)
                contracts_list = cur.fetchall()

                if contracts_list:
                    payload["filter_list"] = contracts_list
                    return "all_contracts_controller", payload

            elif order is not None and all_your == "your":
                query = f"SELECT {fields} FROM {table} WHERE commercial_username = '{collaborator}' ORDER BY {order}"
                cur.execute(query)
                contracts_list = cur.fetchall()
                if contracts_list:
                    payload["filter_list"] = contracts_list
                    return "your_contracts_controller", payload

            ErrorView.query_not_find()
            return "contracts_controller", payload
        if table == "event":
            choice = FilterView.events_filter()

            if choice == "1":
                order = "customer_name"

            elif choice == "2":
                order = "support_username"

            elif choice == "3":
                order = "start_date DESC"

            elif choice == "4":
                order = "start_date ASC"

            elif choice == "5":
                order = "end_date DESC"

            elif choice == "6":
                order = "end_date ASC"

            elif choice == "7":
                order = "attendees DESC"

            elif choice == "8":
                order = "attendees ASC"

            else:
                ErrorView.choice_error()
                return "events_controller", payload

            if order is not None and all_your == "all":
                query = f"SELECT {fields} FROM {table} ORDER BY {order}"
                cur.execute(query)
                events_list = cur.fetchall()

                if events_list:
                    payload["filter_list"] = events_list
                    return "all_events_controller", payload

            elif order is not None and all_your == "your":
                query = f"SELECT {fields} FROM {table} WHERE commercial_username = '{collaborator}' ORDER BY {order}"
                cur.execute(query)
                events_list = cur.fetchall()
                if events_list:
                    payload["filter_list"] = events_list
                    return "your_events_controller", payload

            ErrorView.query_not_find()
            return "events_controller", payload
        if table == "collaborater":
            choice = FilterView.collaborators_filter()

            if choice == "1":
                order = "username"

            elif choice == "2":
                order = "role"

            else:
                ErrorView.choice_error()
                return "collaborators_controller", payload

            if order is not None:
                query = f"SELECT {fields} FROM {table} ORDER BY {order}"
                cur.execute(query)
                collaboraters_list = cur.fetchall()

                if collaboraters_list:
                    payload["filter_list"] = collaboraters_list
                    return "all_collaborators_controller", payload

            ErrorView.query_not_find()
            return "collaborators_controller", payload
