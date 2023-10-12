from views.views import MainView


class MainController:
    """ """

    @classmethod
    def auth_controller(cls, payload):
        email, pwd = MainView.auth_view()

        print(email)

        # PASS
        log = []

        if (email, pwd) in log:
            return "main_controller", payload
        else:
            MainView.auth_error_view()
            return "auth_controller", payload
