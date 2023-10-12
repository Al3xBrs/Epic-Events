from controllers.controllers import MainController

routes = {
    "auth_controller": MainController.auth_controller,
}


def main():
    payload = {}
    controller_key, payload = MainController.auth_controller(payload)

    while True:
        controller = routes[controller_key]
        controller_key, payload = controller(payload)


if __name__ == "__main__":
    main()
