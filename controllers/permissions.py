def is_authenticated(user):
    if user.authenticated:
        return True
    else:
        return False


def is_sale(user):
    if user.role == "sale":
        return True
    else:
        return False


def is_support(user):
    if user.role == "support":
        return True
    else:
        return False


def is_gesture(user):
    if user.role == "gesture":
        return True
    else:
        return False
