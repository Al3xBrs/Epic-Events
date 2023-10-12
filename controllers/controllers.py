from views.views import MainView
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
        email, pwd = MainView.auth()
        # adapt
        log = []
        # TODO : Check for user in db
        # user.is_autenticated = True

        # if is_authenticated(user):
        #     if is_gesture(user):
        #         return "ss", payload
        #     if is_sale(user):
        #         return "ss", payload
        #     if is_support(user):
        #         return "ss", payload

        if email + pwd in log:
            return "main_controller", payload
        else:
            MainView.auth_error()
            return "auth_controller", payload
