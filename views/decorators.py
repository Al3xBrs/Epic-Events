def error_decorator(function):
    def func():
        print("---------- ERROR ----------")
        function()
        print("---------- ERROR ----------")

    return func


def log_decorator(function):
    def func():
        print("---------- LOG IN ----------")
        function()
        print("---------- LOG IN ----------")

    return func
