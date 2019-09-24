from flask import jsonify

from auslib.web.public.base import with_transaction


@with_transaction
def get_update(transaction, **parameters):
    return jsonify({"foo": "bar"})
