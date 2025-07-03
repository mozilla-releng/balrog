import logging

import connexion
from flask import current_app as app

from auslib.global_state import dbo
from auslib.util.auth import verified_userinfo
from auslib.web.admin.views.problem import problem

log = logging.getLogger(__name__)


def requirelogin(f):
    def decorated(*args, **kwargs):
        username = verified_userinfo(connexion.request, app.config["AUTH_DOMAIN"], app.config["AUTH_AUDIENCE"])["email"]
        if not username:
            log.warning("Login Required")
            return problem(401, "Unauthenticated", "Login Required")
        # Machine to machine accounts are identified by uninformative clientIds
        # In order to keep Balrog permissions more readable, we map them to
        # more useful usernames, which are stored in the app config.
        if "@" not in username:
            username = app.config["M2M_ACCOUNT_MAPPING"].get(username, username)
        # Even if the user has provided a valid access token, we don't want to assume
        # that person should be able to access Balrog (in case auth0 is not configured
        # to be restrictive enough.
        elif not dbo.isKnownUser(username):
            log.warning("Authorization Required")
            return problem(403, "Forbidden", "Authorization Required")
        return f(*args, changed_by=username, **kwargs)

    return decorated


def transactionHandler(request_handler):
    def decorated(*args, **kwargs):
        trans = dbo.begin()
        # Transactions are automatically rolled back by the context manager if
        # _post raises an Exception, but we need to make sure they are also
        # rolled back if the View returns any sort of error.
        try:
            ret = request_handler(*args, transaction=trans, **kwargs)
            if ret.status_code >= 400:
                trans.rollback()
            else:
                trans.commit()
            return ret
        except Exception:
            trans.rollback()
            raise
        finally:
            trans.close()

    return decorated
