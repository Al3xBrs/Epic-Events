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
