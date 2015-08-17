import difflib
import json

from flask import Response

from auslib.global_state import dbo
from auslib.admin.views.base import AdminView
from auslib.log import cef_event, CEF_WARN


class FieldView(AdminView):
    """/view/:type/:id/:field"""

    def get_value(self, type_, change_id, field):
        tables = {
            'rule': dbo.rules,
            'permission': dbo.permissions,
            'release': dbo.releases,
        }
        if type_ not in tables:
            raise KeyError('Bad table')
        table = tables[type_]
        revision = table.history.getChange(change_id)
        if not revision:
            raise ValueError('Bad change_id')
        if field not in revision:
            raise KeyError('Bad field')
        return revision[field]

    def format_value(self, value):
        if isinstance(value, basestring):
            try:
                value = json.loads(value)
                value = json.dumps(value, indent=2, sort_keys=True)
            except ValueError:
                pass
        elif value is None:
            value = 'NULL'
        else:
            value = unicode(value, 'utf8')
        return value

    def get(self, type_, change_id, field):
        try:
            value = self.get_value(type_, change_id, field)
        except KeyError as msg:
            cef_event("Bad input", CEF_WARN, errors=str(msg), field=field)
            return Response(status=400, response=str(msg))
        except ValueError as msg:
            return Response(status=404, response=str(msg))
        value = self.format_value(value)
        return Response(value, content_type='text/plain')


class DiffView(FieldView):
    """/diff/:type/:id/:field"""

    def get(self, type_, change_id, field):
        value = self.get_value(type_, change_id, field)
        previous = self.get_value(type_, int(change_id) - 1, field)

        value = self.format_value(value)
        previous = self.format_value(previous)

        differ = difflib.Differ()
        result = differ.compare(
            previous.splitlines(),
            value.splitlines()
        )

        return Response('\n'.join(result), content_type='text/plain')
