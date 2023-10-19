def is_authenticated(user):
    if user.authenticated:
        return True
    else:
        return False


def is_sale(role):
    if role == "sale":
        return True
    else:
        return False


def is_support(role):
    if role == "support":
        return True
    else:
        return False


def is_gesture(role):
    if role == "gesture":
        return True
    else:
        return False
