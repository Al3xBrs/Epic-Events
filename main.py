from controllers.controllers import (
    CollaboratorController,
    MainController,
    SubmenuController,
    CustomerController,
    CRUDController,
    ContractController,
    EventController,
    FilterController,
)
import sentry_sdk

from decouple import Config, RepositoryEnv

config = Config(RepositoryEnv(".env"))
sentry_sdk.init(
    dsn=f"{config('DSN')}",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
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
    "all_collaborators_controller": CollaboratorController.all_collaborators,
    "create_controller": CRUDController.create_controller,
    "update_controller": CRUDController.update_controller,
    "delete_controller": CRUDController.delete_controller,
    "select_one_controller": SubmenuController.select_one_controller,
    "find_one_controller": SubmenuController.find_one_controller,
    "filter_controller": FilterController.filter_controller,
}


def main():
    payload = {}
    controller_key, payload = MainController.auth_controller(payload)

    while True:
        controller = routes[controller_key]
        controller_key, payload = controller(payload)


if __name__ == "__main__":
    main()
