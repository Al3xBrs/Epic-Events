def error_decorator(function):
    def func(*args, **kwargs):
        print("---------- ERROR ----------")
        result = function(*args, **kwargs)
        return result

    return func


def log_decorator(function):
    def func(*args, **kwargs):
        print("---------- LOG IN ----------")
        result = function(*args, **kwargs)
        return result

    return func


def menu_decorator(function):
    def func(*args, **kwargs):
        print("---------- MENU ----------")
        result = function(*args, **kwargs)
        return result

    return func


def customers_decorator(function):
    def func(*args, **kwargs):
        print("---------- CUSTOMERS ----------")
        result = function(*args, **kwargs)
        return result

    return func


def contracts_decorator(function):
    def func(*args, **kwargs):
        print("---------- CONTRACTS ----------")
        result = function(*args, **kwargs)
        return result

    return func


def events_decorator(function):
    def func(*args, **kwargs):
        print("---------- EVENTS ----------")
        result = function(*args, **kwargs)
        return result

    return func
