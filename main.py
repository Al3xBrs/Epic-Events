from controllers.controllers import (
    MainController,
    SubmenuController,
    CustomerController,
    CRUDController,
    ContractController,
    EventController,
)


routes = {
    "auth_controller": MainController.auth_controller,
    "menu_controller": MainController.menu_controller,
    "customers_controller": SubmenuController.customers_controller,
    "all_customers_controller": CustomerController.all_customers_controller,
    "your_customers_controller": CustomerController.your_customers,
    "contracts_controller": SubmenuController.contracts_controller,
    "all_contracts_controller": ContractController.all_contracts_controller,
    "your_contracts_controller": ContractController.your_contracts_controller,
    "events_controller": SubmenuController.events_controller,
    "all_events_controller": EventController.all_events_controller,
    "your_events_controller": EventController.your_events_controller,
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
