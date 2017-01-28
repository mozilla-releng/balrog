import json

from flask import Response

from auslib.admin.views.base import AdminView


class FieldView(AdminView):
    """/view/:id/:field"""
    def __init__(self, table, *args, **kwargs):
        self.table = table

    def get_value(self, change_id, field):
        revision = self.table.history.getChange(change_id=change_id)
        if not revision:
            raise ValueError('Bad change_id')
        if field not in revision:
            raise KeyError('Bad field')
        return revision[field]

    def format_value(self, value):
        if isinstance(value, dict):
            try:
                value = json.dumps(value, indent=2, sort_keys=True)
            except ValueError:
                pass
        elif value is None:
            value = 'NULL'
        elif isinstance(value, int):
            value = unicode(str(value), 'utf8')
        else:
            value = unicode(value, 'utf8')
        return value

    def get(self, change_id, field):
        try:
            value = self.get_value(change_id, field)
        except KeyError as msg:
            self.log.warning("Bad input: %s", field)
            return Response(status=400, response=str(msg))
        except ValueError as msg:
            return Response(status=404, response=str(msg))
        value = self.format_value(value)
        return Response(value, content_type='text/plain')
