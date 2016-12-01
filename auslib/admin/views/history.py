import difflib
import json

from sqlalchemy.sql.expression import null

from flask import Response

from auslib.global_state import dbo
from auslib.admin.views.base import AdminView


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
        revision = table.history.getChange(change_id=change_id)
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

    def get(self, type_, change_id, field):
        try:
            value = self.get_value(type_, change_id, field)
        except KeyError as msg:
            self.log.warning("Bad input: %s", field)
            return Response(status=400, response=str(msg))
        except ValueError as msg:
            return Response(status=404, response=str(msg))
        value = self.format_value(value)
        return Response(value, content_type='text/plain')


class DiffView(FieldView):
    """/diff/:type/:id/:field"""

    def get_prev_id(self, value, change_id):

        release_name = value['name']

        table = dbo.releases.history
        old_revision = table.select(
            where=[
                table.name == release_name,
                table.change_id < change_id,
                table.data_version != null()
            ],
            limit=1,
            order_by=[table.timestamp.desc()],
        )

        return old_revision[0]['change_id']

    def get(self, type_, change_id, field):
        value = self.get_value(type_, change_id, field)
        data_version = self.get_value(type_, change_id, "data_version")

        prev_id = self.get_prev_id(value, change_id)
        previous = self.get_value(type_, prev_id, field)
        prev_data_version = self.get_value(type_, prev_id, "data_version")

        value = self.format_value(value)
        previous = self.format_value(previous)

        result = difflib.unified_diff(
            previous.splitlines(),
            value.splitlines(),
            fromfile="Data Version {}".format(prev_data_version),
            tofile="Data Version {}".format(data_version),
            lineterm=""
        )

        return Response('\n'.join(result), content_type='text/plain')
