from controllers.controllers import (
    MainController,
    SubmenuController,
    CustomerController,
    CRUDController,
)

routes = {
    "auth_controller": MainController.auth_controller,
    "menu_controller": MainController.menu_controller,
    "customers_controller": SubmenuController.customers_controller,
    "contracts_controller": SubmenuController.contracts_controller,
    "events_controller": SubmenuController.events_controller,
    "all_customers_controller": CustomerController.all_customers_controller,
    "your_customers_controller": CustomerController.your_customers,
    "create_controller": CRUDController.create_controller,
    "find_one_controller": SubmenuController.find_one_controller,
}


def main():
    payload = {}
    controller_key, payload = MainController.auth_controller(payload)

    while True:
        controller = routes[controller_key]
        controller_key, payload = controller(payload)


if __name__ == "__main__":
    main()
