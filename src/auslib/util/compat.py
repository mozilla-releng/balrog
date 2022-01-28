from copy import copy

import sqlalchemy

if sqlalchemy.__version__.startswith("1.3."):

    def whereclause(q):
        return q._whereclause

    def query_param(query, param):
        return query.parameters[param]

    def query_params(query):
        return copy(query.parameters)

else:

    def whereclause(q):
        return q.whereclause

    def query_param(query, param):
        return query._values[param].value

    def query_params(query):
        return {k: p.value for k, p in query._values.items()}
