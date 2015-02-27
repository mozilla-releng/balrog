import json

from flask import render_template, Response, make_response, request, jsonify

from auslib.global_state import dbo
from auslib.admin.views.base import (
    requirelogin, requirepermission, AdminView, HistoryAdminView,
)
from auslib.admin.views.csrf import get_csrf_headers
from auslib.admin.views.forms import EditRuleForm, RuleForm, DbEditableForm
from auslib.log import cef_event, CEF_WARN, CEF_ALERT
from auslib.util import getPagination


class RulesAPIView(AdminView):
    """/api/rules"""
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
        form.mapping.choices = [(item['name'],item['name']) for item in releaseNames]
        form.mapping.choices.insert(0, ('', 'NULL' ) )

        if not form.validate():
            cef_event("Bad input", CEF_WARN, errors=form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        what = dict(backgroundRate=form.backgroundRate.data,
                mapping=form.mapping.data,
                priority=form.priority.data,
                product = form.product.data,
                version = form.version.data,
                buildID = form.build_id.data,
                channel = form.channel.data,
                locale = form.locale.data,
                distribution = form.distribution.data,
                buildTarget = form.build_target.data,
                osVersion = form.os_version.data,
                distVersion = form.dist_version.data,
                comment = form.comment.data,
                update_type = form.update_type.data,
                headerArchitecture = form.header_arch.data)
        rule_id = dbo.rules.addRule(changed_by=changed_by, what=what,
            transaction=transaction)
        return Response(status=200, response=str(rule_id))


class SingleRuleView(AdminView):
    """ /api/rules/:id"""

    def get(self, rule_id):
        rule = dbo.rules.getRuleById(rule_id=rule_id)
        if not rule:
            return Response(status=404, response="Requested rule does not exist")

        releaseNames = dbo.releases.getReleaseNames()

        headers = {'X-Data-Version': rule['data_version']}
        headers.update(get_csrf_headers())

        # TODO: Only return json after old ui is dead
        if "application/json" in request.headers.get("Accept-Encoding", ""):
            return Response(response=json.dumps(rule), mimetype="application/json", headers=headers)
        else:
            form = EditRuleForm(prefix=str(rule_id),
                    backgroundRate = rule['backgroundRate'],
                    mapping = rule['mapping'],
                    priority = rule['priority'],
                    product = rule['product'],
                    version = rule['version'],
                    build_id = rule['buildID'],
                    channel = rule['channel'],
                    locale = rule['locale'],
                    distribution = rule['distribution'],
                    build_target = rule['buildTarget'],
                    os_version = rule['osVersion'],
                    dist_version = rule['distVersion'],
                    comment = rule['comment'],
                    update_type = rule['update_type'],
                    header_arch = rule['headerArchitecture'],
                    data_version=rule['data_version'])
            form.mapping.choices = [(item['name'],item['name']) for item in
                    releaseNames]
            form.mapping.choices.insert(0, ('', 'NULL' ) )
            return Response(response=render_template('fragments/single_rule.html', rule=rule, form=form), mimetype='text/html', headers=headers)

    # changed_by is available via the requirelogin decorator
    @requirelogin
    def _post(self, rule_id, transaction, changed_by):
        # Verify that the rule_id exists.
        rule = dbo.rules.getRuleById(rule_id, transaction=transaction)
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

        form.mapping.choices = [(item['name'],item['name']) for item in releaseNames]
        form.mapping.choices.insert(0, ('', 'NULL' ))

        if not form.validate():
            cef_event("Bad input", CEF_WARN, errors=form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        what = dict()
        if form.backgroundRate.data is not None:
            what['backgroundRate'] = form.backgroundRate.data
        if form.mapping.data:
            what['mapping'] = form.mapping.data
        if form.priority.data is not None:
            what['priority'] = form.priority.data
        if form.product.data:
            what['product'] = form.product.data
        if form.version.data:
            what['version'] = form.version.data
        if form.build_id.data:
            what['buildID'] = form.build_id.data
        if form.channel.data:
            what['channel'] = form.channel.data
        if form.locale.data:
            what['locale'] = form.locale.data
        if form.distribution.data:
            what['distribution'] = form.distribution.data
        if form.build_target.data:
            what['buildTarget'] = form.build_target.data
        if form.os_version.data:
            what['osVersion'] = form.os_version.data
        if form.dist_version.data:
            what['distVersion'] = form.dist_version.data
        if form.comment.data:
            what['comment'] = form.comment.data
        if form.update_type.data:
            what['update_type'] = form.update_type.data
        if form.header_arch.data:
            what['headerArchitecture'] = form.header_arch.data

        dbo.rules.updateRule(changed_by=changed_by, rule_id=rule_id, what=what,
            old_data_version=form.data_version.data, transaction=transaction)
        # find out what the next data version is
        rule = dbo.rules.getRuleById(rule_id, transaction=transaction)
        new_data_version = rule['data_version']
        response = make_response(json.dumps(dict(new_data_version=new_data_version)))
        response.headers['Content-Type'] = 'application/json'
        return response

    _put = _post

    @requirelogin
    def _delete(self, rule_id, transaction, changed_by):
        # Verify that the rule_id exists.
        rule = dbo.rules.getRuleById(rule_id, transaction=transaction)
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

        dbo.rules.deleteRule(changed_by=changed_by, rule_id=rule_id,
            old_data_version=form.data_version.data, transaction=transaction)

        return Response(status=200)


class RuleHistoryAPIView(HistoryAdminView):
    """/api/rules/:id/revisions"""

    def get(self, rule_id):
        rule = dbo.rules.getRuleById(rule_id=rule_id)
        if not rule:
            return Response(status=404,
                            response='Requested rule does not exist')

        table = dbo.rules.history

        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 100))
            assert page >= 1
        except (ValueError, AssertionError), msg:
            cef_event("Bad input", CEF_WARN, errors=msg)
            return Response(status=400, response=str(msg))
        offset = limit * (page - 1)
        total_count, = (table.t.count()
            .where(table.rule_id == rule_id)
            .where(table.data_version != None)
            .execute()
            .fetchone()
        )

        revisions = table.select(
            where=[table.rule_id == rule_id,
                   table.data_version != None],  # sqlalchemy
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
            'product': 'product',
            'version': 'version',
            'background_rate': 'backgroundRate',
            'build_id': 'buildID',
            'channel': 'channel',
            'locale': 'locale',
            'distribution': 'distribution',
            'build_target': 'buildTarget',
            'os_version': 'osVersion',
            'dist_version': 'distVersion',
            'comment': 'comment',
            'update_type': 'update_type',
            'header_arch': 'headerArchitecture',
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
        rule_id = int(rule_id)

        change_id = request.form.get('change_id')
        if not change_id:
            cef_event("Bad input", CEF_WARN, errors="no change_id")
            return Response(status=400, response='no change_id')
        change = dbo.rules.history.getChange(change_id=change_id)
        if change is None:
            return Response(status=404, response='bad change_id')
        if change['rule_id'] != rule_id:
            return Response(status=404, response='bad rule_id')
        rule = dbo.rules.getRuleById(rule_id=rule_id)
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
            product=change['product'],
            version=change['version'],
            buildID=change['buildID'],
            channel=change['channel'],
            locale=change['locale'],
            distribution=change['distribution'],
            buildTarget=change['buildTarget'],
            osVersion=change['osVersion'],
            distVersion=change['distVersion'],
            comment=change['comment'],
            update_type=change['update_type'],
            headerArchitecture=change['headerArchitecture'],
        )

        dbo.rules.updateRule(changed_by=changed_by, rule_id=rule_id, what=what,
            old_data_version=old_data_version, transaction=transaction)

        return Response("Excellent!")


# TODO: Kill me when old admin ui is shut off
class RulesPageView(AdminView):
    """/rules.html"""
    def get(self):
        rules = dbo.rules.getOrderedRules()

        releaseNames = dbo.releases.getReleaseNames()

        new_rule_form = RuleForm(prefix="new_rule");
        new_rule_form.mapping.choices = [(item['name'],item['name']) for item in
                releaseNames]
        new_rule_form.mapping.choices.insert(0, ('', 'NULL' ))
        forms = {}

        for rule in rules:
            _id = rule['rule_id']
            self.log.debug(rule)
            forms[_id] = EditRuleForm(prefix=str(_id),
                                    backgroundRate = rule['backgroundRate'],
                                    mapping = rule['mapping'],
                                    priority = rule['priority'],
                                    product = rule['product'],
                                    version = rule['version'],
                                    build_id = rule['buildID'],
                                    channel = rule['channel'],
                                    locale = rule['locale'],
                                    distribution = rule['distribution'],
                                    build_target = rule['buildTarget'],
                                    os_version = rule['osVersion'],
                                    dist_version = rule['distVersion'],
                                    comment = rule['comment'],
                                    update_type = rule['update_type'],
                                    header_arch = rule['headerArchitecture'],
                                    data_version=rule['data_version'])
            forms[_id].mapping.choices = [(item['name'],item['name']) for item in
                                                releaseNames]
            forms[_id].mapping.choices.insert(0, ('', 'NULL' ) )

        return render_template('rules.html', rules=rules, forms=forms, new_rule_form=new_rule_form)


class RuleHistoryView(HistoryAdminView):
    """ /rules/<rule_id>/revisions """

    def get(self, rule_id):
        rule = dbo.rules.getRuleById(rule_id=rule_id)
        if not rule:
            return Response(status=404,
                            response='Requested rule does not exist')

        table = dbo.rules.history

        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            assert page >= 1
        except (ValueError, AssertionError), msg:
            cef_event("Bad input", CEF_WARN, errors=msg)
            return Response(status=400, response=str(msg))
        offset = limit * (page - 1)
        total_count, = (table.t.count()
            .where(table.rule_id == rule_id)
            .where(table.data_version != None)
            .execute()
            .fetchone()
        )
        if total_count > limit:
            pagination = getPagination(page, total_count, limit)
        else:
            pagination = None

        revisions = table.select(
            where=[table.rule_id == rule_id,
                   table.data_version != None],  # sqlalchemy
            limit=limit,
            offset=offset,
            order_by=[table.timestamp.asc()],
        )
        primary_keys = table.base_primary_key
        all_keys = self.getAllRevisionKeys(revisions, primary_keys)
        self.annotateRevisionDifferences(revisions)

        return render_template(
            'revisions.html',
            revisions=revisions,
            label='rule',
            primary_keys=primary_keys,
            all_keys=all_keys,
            total_count=total_count,
            pagination=pagination,
        )

    @requirelogin
    def _post(self, rule_id, transaction, changed_by):
        rule_id = int(rule_id)

        change_id = request.form.get('change_id')
        if not change_id:
            cef_event("Bad input", CEF_WARN, errors="no change_id")
            return Response(status=400, response='no change_id')
        change = dbo.rules.history.getChange(change_id=change_id)
        if change is None:
            return Response(status=404, response='bad change_id')
        if change['rule_id'] != rule_id:
            return Response(status=404, response='bad rule_id')
        rule = dbo.rules.getRuleById(rule_id=rule_id)
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
            product=change['product'],
            version=change['version'],
            buildID=change['buildID'],
            channel=change['channel'],
            locale=change['locale'],
            distribution=change['distribution'],
            buildTarget=change['buildTarget'],
            osVersion=change['osVersion'],
            distVersion=change['distVersion'],
            comment=change['comment'],
            update_type=change['update_type'],
            headerArchitecture=change['headerArchitecture'],
        )

        dbo.rules.updateRule(changed_by=changed_by, rule_id=rule_id, what=what,
            old_data_version=old_data_version, transaction=transaction)

        return Response("Excellent!")
