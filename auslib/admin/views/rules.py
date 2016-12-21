import json

from sqlalchemy.sql.expression import null

from flask import Response, request, jsonify

from auslib.global_state import dbo
from auslib.admin.views.base import (
    requirelogin, AdminView, HistoryAdminView,
)
from auslib.admin.views.csrf import get_csrf_headers
from auslib.admin.views.forms import EditRuleForm, RuleForm, DbEditableForm, \
    ScheduledChangeNewRuleForm, ScheduledChangeExistingRuleForm, \
    ScheduledChangeDeleteRuleForm, EditScheduledChangeNewRuleForm, \
    EditScheduledChangeExistingRuleForm, EditScheduledChangeDeleteRuleForm
from auslib.admin.views.scheduled_changes import ScheduledChangesView, \
    ScheduledChangeView, EnactScheduledChangeView, ScheduledChangeHistoryView, \
    SignoffsView


class RulesAPIView(AdminView):
    """/rules"""

    def get(self, **kwargs):
        # We can't use a form here because it will enforce "csrf_token" needing
        # to exist, which doesn't make sense for GET requests.
        where = {}
        for field in ("product",):
            if request.args.get(field):
                where[field] = request.args[field]

        rules = dbo.rules.getOrderedRules(where=where)
        count = 0
        _rules = []
        for rule in rules:
            _rules.append(dict(
                (key, value)
                for key, value in rule.items()
            ))
            count += 1
        return jsonify(count=count, rules=_rules)

    # changed_by is available via the requirelogin decorator
    @requirelogin
    def _post(self, transaction, changed_by):
        # a Post here creates a new rule
        form = RuleForm()
        releaseNames = dbo.releases.getReleaseNames()
        form.mapping.choices = [(item['name'], item['name']) for item in releaseNames]
        form.mapping.choices.insert(0, ('', 'NULL'))

        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        what = dict(backgroundRate=form.backgroundRate.data,
                    mapping=form.mapping.data,
                    fallbackMapping=form.fallbackMapping.data,
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
                    systemCapabilities=form.systemCapabilities.data,
                    distVersion=form.distVersion.data,
                    whitelist=form.whitelist.data,
                    comment=form.comment.data,
                    update_type=form.update_type.data,
                    headerArchitecture=form.headerArchitecture.data)
        rule_id = dbo.rules.insert(changed_by=changed_by, transaction=transaction, **what)
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

        releaseNames = dbo.releases.getReleaseNames()

        form.mapping.choices = [(item['name'], item['name']) for item in releaseNames]
        form.mapping.choices.insert(0, ('', 'NULL'))

        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
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

        dbo.rules.update(changed_by=changed_by, where={"rule_id": id_or_alias}, what=what,
                         old_data_version=form.data_version.data, transaction=transaction)

        # find out what the next data version is
        rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
        return jsonify(new_data_version=rule["data_version"])

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

        dbo.rules.delete(where={"rule_id": id_or_alias}, changed_by=changed_by, old_data_version=form.data_version.data,
                         transaction=transaction)

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
            self.log.warning("Bad input: %s", msg)
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
            order_by=[table.timestamp.desc()],
        )
        _rules = []
        _mapping = {
            # return : db name
            'rule_id': 'rule_id',
            'mapping': 'mapping',
            'fallbackMapping': 'fallbackMapping',
            'priority': 'priority',
            'alias': 'alias',
            'product': 'product',
            'version': 'version',
            'backgroundRate': 'backgroundRate',
            'buildID': 'buildID',
            'channel': 'channel',
            'locale': 'locale',
            'distribution': 'distribution',
            'buildTarget': 'buildTarget',
            'osVersion': 'osVersion',
            'systemCapabilities': 'systemCapabilities',
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

        return jsonify(count=total_count, rules=_rules)

    @requirelogin
    def _post(self, rule_id, transaction, changed_by):
        rule = dbo.rules.getRule(rule_id)
        if rule is None:
            return Response(status=404, response='bad rule_id')
        change_id = None
        if request.json:
            change_id = request.json.get('change_id')
        if not change_id:
            self.log.warning("Bad input: %s", "no change_id")
            return Response(status=400, response='no change_id')
        change = dbo.rules.history.getChange(change_id=change_id)
        if change is None:
            return Response(status=400, response='bad change_id')
        if change['rule_id'] != rule_id:
            return Response(status=400, response='bad rule_id')
        old_data_version = rule['data_version']

        # now we're going to make a new insert based on this
        what = dict(
            backgroundRate=change['backgroundRate'],
            mapping=change['mapping'],
            fallbackMapping=change['fallbackMapping'],
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
            systemCapabilities=change['systemCapabilities'],
            distVersion=change['distVersion'],
            whitelist=change['whitelist'],
            comment=change['comment'],
            update_type=change['update_type'],
            headerArchitecture=change['headerArchitecture'],
        )

        dbo.rules.update(changed_by=changed_by, where={"rule_id": rule_id}, what=what,
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


class RuleScheduledChangesView(ScheduledChangesView):
    def __init__(self):
        super(RuleScheduledChangesView, self).__init__("rules", dbo.rules)

    @requirelogin
    def _post(self, transaction, changed_by):

        change_type = request.json.get("change_type")

        if change_type == "update":
            form = ScheduledChangeExistingRuleForm()

            releaseNames = dbo.releases.getReleaseNames(transaction=transaction)

            self.log.debug("releaseNames: %s" % (releaseNames))
            self.log.debug("transaction: %s" % (transaction))

            form.mapping.choices = [(item['name'], item['name']) for item in releaseNames]
            form.mapping.choices.insert(0, ('', 'NULL'))

        elif change_type == "insert":
            form = ScheduledChangeNewRuleForm()

            releaseNames = dbo.releases.getReleaseNames(transaction=transaction)

            self.log.debug("releaseNames: %s" % (releaseNames))
            self.log.debug("transaction: %s" % (transaction))

            form.mapping.choices = [(item['name'], item['name']) for item in releaseNames]
            form.mapping.choices.insert(0, ('', 'NULL'))

        elif change_type == "delete":
            form = ScheduledChangeDeleteRuleForm()

        else:
            return Response(status=400, response="Change Type invalid or not entered")

        return super(RuleScheduledChangesView, self)._post(form, transaction, changed_by)


class RuleScheduledChangeView(ScheduledChangeView):
    def __init__(self):
        super(RuleScheduledChangeView, self).__init__("rules", dbo.rules)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        if request.json and request.json.get("data_version"):
            if request.json.get("change_type") == "delete":
                form = EditScheduledChangeDeleteRuleForm()
            else:
                form = EditScheduledChangeExistingRuleForm()
        else:
            form = EditScheduledChangeNewRuleForm()

        if request.json.get("change_type") != "delete":
            releaseNames = dbo.releases.getReleaseNames(transaction=transaction)

            form.mapping.choices = [(item['name'], item['name']) for item in releaseNames]
            form.mapping.choices.insert(0, ('', 'NULL'))

        return super(RuleScheduledChangeView, self)._post(sc_id, form, transaction, changed_by)

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(RuleScheduledChangeView, self)._delete(sc_id, transaction, changed_by)


class EnactRuleScheduledChangeView(EnactScheduledChangeView):
    def __init__(self):
        super(EnactRuleScheduledChangeView, self).__init__("rules", dbo.rules)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(EnactRuleScheduledChangeView, self)._post(sc_id, transaction, changed_by)


class RuleScheduledChangeSignoffsView(SignoffsView):
    def __init__(self):
        super(RuleScheduledChangeSignoffsView, self).__init__("rules", dbo.rules)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(RuleScheduledChangeSignoffsView, self)._post(sc_id, transaction, changed_by)

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(RuleScheduledChangeSignoffsView, self)._delete(sc_id, transaction, changed_by)


class RuleScheduledChangeHistoryView(ScheduledChangeHistoryView):
    def __init__(self):
        super(RuleScheduledChangeHistoryView, self).__init__("rules", dbo.rules)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(RuleScheduledChangeHistoryView, self)._post(sc_id, transaction, changed_by)
