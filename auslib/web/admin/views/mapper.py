from auslib.web.admin.views.csrf import CSRFView
from auslib.web.admin.views.rules import RulesAPIView
from auslib.web.admin.views.permissions import UsersView


def csrf_get():
    return CSRFView().get()


def rules_get():
    return RulesAPIView().get()


def rules_post():
    return RulesAPIView().post()


def users_get():
    return UsersView().get()
