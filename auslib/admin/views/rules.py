import json

from sqlalchemy.sql.expression import null

from flask import Response, make_response, request, jsonify

from auslib.global_state import dbo
from auslib.admin.views.base import (
    requirelogin, requirepermission, AdminView, HistoryAdminView,
)
from auslib.admin.views.csrf import get_csrf_headers
from auslib.admin.views.forms import EditRuleForm, RuleForm, DbEditableForm
from auslib.log import cef_event, CEF_WARN, CEF_ALERT


class RulesAPIView(AdminView):
    """/rules"""

    def get(self, **kwargs):
        rules = dbo.rules.getOrderedRules()
        count = 0
        _rules = []
        for rule in rules:
            _rules.append(dict(
                (key, value)
                for key, value in rule.items()
            ))
            count += 1
        ret = {
            "count": count,
            "rules": _rules,
        }
        return jsonify(ret)

    # changed_by is available via the requirelogin decorator
    @requirelogin
    @requirepermission('/rules')
    def _post(self, transaction, changed_by):
        # a Post here creates a new rule
        form = RuleForm()
        releaseNames = dbo.releases.getReleaseNames()
        form.mapping.choices = [(item['name'], item['name']) for item in releaseNames]
        form.mapping.choices.insert(0, ('', 'NULL'))

        if not form.validate():
            cef_event("Bad input", CEF_WARN, errors=form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        what = dict(backgroundRate=form.backgroundRate.data,
                    mapping=form.mapping.data,
                    priority=form.priority.data,
                    alias=form.alias.data,
                    product=form.product.data,
                    version=form.version.data,
                    buildID=form.buildID.data,
                    channel=form.channel.data,
                    locale=form.locale.data,
                    distribution=form.distribution.data,
                    buildTarget=form.buildTarget.data,
                    osVersion=form.osVersion.data,
                    distVersion=form.distVersion.data,
                    whitelist=form.whitelist.data,
                    comment=form.comment.data,
                    update_type=form.update_type.data,
                    headerArchitecture=form.headerArchitecture.data)
        rule_id = dbo.rules.addRule(changed_by=changed_by, what=what,
                                    transaction=transaction)
        return Response(status=200, response=str(rule_id))


class SingleRuleView(AdminView):
    """ /rules/:id"""

    def get(self, id_or_alias):
        rule = dbo.rules.getRule(id_or_alias)
        if not rule:
            return Response(status=404, response="Requested rule does not exist")

        headers = {'X-Data-Version': rule['data_version']}
        headers.update(get_csrf_headers())

        return Response(response=json.dumps(rule), mimetype="application/json", headers=headers)

    # changed_by is available via the requirelogin decorator
    @requirelogin
    def _post(self, id_or_alias, transaction, changed_by):
        # Verify that the rule_id or alias exists.
        rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
        if not rule:
            return Response(status=404)
        form = EditRuleForm()

        # Verify that the user has permission for the existing rule _and_ what the rule would become.
        toCheck = [rule['product']]
        # Rules can be partially updated - if product is null/None, we won't update that field, so
        # we shouldn't check its permission.
        if form.product.data:
            toCheck.append(form.product.data)
        for product in toCheck:
            if not dbo.permissions.hasUrlPermission(changed_by, '/rules/:id', 'POST', urlOptions={'product': product}):
                msg = "%s is not allowed to alter rules that affect %s" % (changed_by, product)
                cef_event('Unauthorized access attempt', CEF_ALERT, msg=msg)
                return Response(status=401, response=msg)
        releaseNames = dbo.releases.getReleaseNames()

        form.mapping.choices = [(item['name'], item['name']) for item in releaseNames]
        form.mapping.choices.insert(0, ('', 'NULL'))

        if not form.validate():
            cef_event("Bad input", CEF_WARN, errors=form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        what = dict()
        # We need to be able to support changing AND removing parts of a rule,
        # and because of how Flask's request object and WTForm's defaults work
        # this gets a little hary.
        for k, v in form.data.iteritems():
            # data_version is a "special" column, in that it's not part of the
            # primary data, and shouldn't be updatable by the user.
            if k == "data_version":
                continue
            # We need to check for each column in both the JSON style post
            # and the regular multipart form data. If the key is not present in
            # either of these data structures. We treat this cases as no-op
            # and shouldn't modify the data for that key.
            # If the key is present we should modify the data as requested.
            # If a value is an empty string, we should remove that restriction
            # from the rule (aka, set as NULL in the db). The underlying Form
            # will have already converted it to None, so we can treat it the
            # same as a modification here.
            if (request.json and k in request.json) or k in request.form:
                what[k] = v

        dbo.rules.updateRule(changed_by=changed_by, id_or_alias=id_or_alias, what=what,
                             old_data_version=form.data_version.data, transaction=transaction)

        # find out what the next data version is
        rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
        new_data_version = rule['data_version']
        response = make_response(json.dumps(dict(new_data_version=new_data_version)))
        response.headers['Content-Type'] = 'application/json'
        return response

    _put = _post

    @requirelogin
    def _delete(self, id_or_alias, transaction, changed_by):
        # Verify that the rule_id or alias exists.
        rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
        if not rule:
            return Response(status=404)

        # Bodies are ignored for DELETE requests, so we need to force WTForms
        # to look at the arguments instead.
        # Even though we aren't going to use most of the form fields (just
        # rule_id and data_version), we still want to create and validate the
        # form to make sure that the CSRF token is checked.
        form = DbEditableForm(request.args)

        if not dbo.permissions.hasUrlPermission(changed_by, '/rules/:id', 'DELETE', urlOptions={'product': rule['product']}):
            msg = "%s is not allowed to alter rules that affect %s" % (changed_by, rule['product'])
            cef_event('Unauthorized access attempt', CEF_ALERT, msg=msg)
            return Response(status=401, response=msg)

        dbo.rules.deleteRule(changed_by=changed_by, id_or_alias=id_or_alias,
                             old_data_version=form.data_version.data, transaction=transaction)

        return Response(status=200)


class RuleHistoryAPIView(HistoryAdminView):
    """/rules/:id/revisions"""

    def get(self, rule_id):
        rule = dbo.rules.getRule(rule_id)
        if not rule:
            return Response(status=404,
                            response='Requested rule does not exist')

        table = dbo.rules.history

        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 100))
            assert page >= 1
        except (ValueError, AssertionError) as msg:
            cef_event("Bad input", CEF_WARN, errors=msg)
            return Response(status=400, response=str(msg))
        offset = limit * (page - 1)
        total_count = table.t.count()\
            .where(table.rule_id == rule_id)\
            .where(table.data_version != null())\
            .execute()\
            .fetchone()[0]

        revisions = table.select(
            where=[table.rule_id == rule_id,
                   table.data_version != null()],
            limit=limit,
            offset=offset,
            order_by=[table.timestamp.asc()],
        )
        _rules = []
        _mapping = {
            # return : db name
            'id': 'rule_id',
            'mapping': 'mapping',
            'priority': 'priority',
            'alias': 'alias',
            'product': 'product',
            'version': 'version',
            'background_rate': 'backgroundRate',
            'buildID': 'buildID',
            'channel': 'channel',
            'locale': 'locale',
            'distribution': 'distribution',
            'buildTarget': 'buildTarget',
            'osVersion': 'osVersion',
            'distVersion': 'distVersion',
            'whitelist': 'whitelist',
            'comment': 'comment',
            'update_type': 'update_type',
            'headerArchitecture': 'headerArchitecture',
            'data_version': 'data_version',
            # specific to revisions
            'change_id': 'change_id',
            'timestamp': 'timestamp',
            'changed_by': 'changed_by',
        }
        for rule in revisions:
            _rules.append(dict(
                (key, rule[db_key])
                for key, db_key in _mapping.items()
            ))

        ret = {
            'count': total_count,
            'rules': _rules,
        }
        return Response(response=json.dumps(ret), mimetype="application/json")

    @requirelogin
    def _post(self, rule_id, transaction, changed_by):
        change_id = None
        if request.json:
            change_id = request.json.get('change_id')
        if not change_id:
            cef_event("Bad input", CEF_WARN, errors="no change_id")
            return Response(status=400, response='no change_id')
        change = dbo.rules.history.getChange(change_id=change_id)
        if change is None:
            return Response(status=404, response='bad change_id')
        if change['rule_id'] != rule_id:
            return Response(status=404, response='bad rule_id')
        rule = dbo.rules.getRule(rule_id)
        if rule is None:
            return Response(status=404, response='bad rule_id')
        # Verify that the user has permission for the existing rule _and_ what the rule would become.
        for product in (rule['product'], change['product']):
            if not dbo.permissions.hasUrlPermission(changed_by, '/rules/:id', 'POST', urlOptions={'product': product}):
                msg = "%s is not allowed to alter rules that affect %s" % (changed_by, product)
                cef_event('Unauthorized access attempt', CEF_ALERT, msg=msg)
                return Response(status=401, response=msg)
        old_data_version = rule['data_version']

        # now we're going to make a new insert based on this
        what = dict(
            backgroundRate=change['backgroundRate'],
            mapping=change['mapping'],
            priority=change['priority'],
            alias=change['alias'],
            product=change['product'],
            version=change['version'],
            buildID=change['buildID'],
            channel=change['channel'],
            locale=change['locale'],
            distribution=change['distribution'],
            buildTarget=change['buildTarget'],
            osVersion=change['osVersion'],
            distVersion=change['distVersion'],
            whitelist=change['whitelist'],
            comment=change['comment'],
            update_type=change['update_type'],
            headerArchitecture=change['headerArchitecture'],
        )

        dbo.rules.updateRule(changed_by=changed_by, id_or_alias=rule_id, what=what,
                             old_data_version=old_data_version, transaction=transaction)

        return Response("Excellent!")


class SingleRuleColumnView(AdminView):
    """ /rules/columns/:column"""

    def get(self, column):
        rules = dbo.rules.getOrderedRules()
        column_values = []
        if column not in rules[0].keys():
            return Response(status=404, response="Requested column does not exist")

        for rule in rules:
            for key, value in rule.items():
                if key == column and value is not None:
                    column_values.append(value)
        column_values = list(set(column_values))
        ret = {
            "count": len(column_values),
            column: column_values,
        }
        return jsonify(ret)
