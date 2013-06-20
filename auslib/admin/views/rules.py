import json
from flask import render_template, Response, make_response, request

from auslib.util import getPagination
from auslib.admin.base import db
from auslib.admin.views.base import (
    requirelogin, requirepermission, AdminView, HistoryAdminView
)
from auslib.admin.views.forms import EditRuleForm, RuleForm

class RulesPageView(AdminView):
    """/rules.html"""
    def get(self):
        rules = db.rules.getOrderedRules()

        releaseNames = db.releases.getReleaseNames()

        new_rule_form = RuleForm(prefix="new_rule");
        new_rule_form.mapping.choices = [(item['name'],item['name']) for item in
                releaseNames]
        new_rule_form.mapping.choices.insert(0, ('', 'NULL' ))
        forms = {}

        for rule in rules:
            _id = rule['rule_id']
            self.log.debug(rule)
            forms[_id] = EditRuleForm(prefix=str(_id),
                                    throttle = rule['throttle'],
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


class RulesAPIView(AdminView):
    """/rules"""
    # changed_by is available via the requirelogin decorator
    @requirelogin
    @requirepermission('/rules', options=[])
    def _post(self, transaction, changed_by):
        # a Post here creates a new rule
        form = RuleForm()
        releaseNames = db.releases.getReleaseNames()
        form.mapping.choices = [(item['name'],item['name']) for item in releaseNames]
        form.mapping.choices.insert(0, ('', 'NULL' ) )
        if not form.validate():
            self.log.debug(form.errors)
            return Response(status=400, response=form.errors)

        what = dict(throttle=form.throttle.data,
                mapping=form.mapping.data,
                priority=form.priority.data,
                product = form.product.data,
                version = form.version.data,
                build_id = form.build_id.data,
                channel = form.channel.data,
                locale = form.locale.data,
                distribution = form.distribution.data,
                build_target = form.build_target.data,
                os_version = form.os_version.data,
                dist_version = form.dist_version.data,
                comment = form.comment.data,
                update_type = form.update_type.data,
                header_arch = form.header_arch.data)
        rule_id = db.rules.addRule(changed_by=changed_by, what=what,
            transaction=transaction)
        return Response(status=200, response=rule_id)


class SingleRuleView(AdminView):
    """ /rules/<rule_id> """

    def get(self, rule_id):
        rule = db.rules.getRuleById(rule_id=rule_id)
        if not rule:
            return Response(status=404, response="Requested rule does not exist")

        releaseNames = db.releases.getReleaseNames()

        form = EditRuleForm(prefix=str(rule_id),
                throttle = rule['throttle'],
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

        return render_template('fragments/single_rule.html', rule=rule, form=form)

    # changed_by is available via the requirelogin decorator
    @requirelogin
    @requirepermission('/rules/:id', options=[])
    def _post(self, rule_id, transaction, changed_by):
        # Verify that the rule_id exists.
        if not db.rules.getRuleById(rule_id, transaction=transaction):
            return Response(status=404)
        form = EditRuleForm()

        releaseNames = db.releases.getReleaseNames()

        form.mapping.choices = [(item['name'],item['name']) for item in releaseNames]
        form.mapping.choices.insert(0, ('', 'NULL' ))

        if not form.validate():
            return Response(status=400, response=form.errors)
        what = dict(throttle=form.throttle.data,
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
        self.log.debug("old_data_version: %s", form.data_version.data)
        db.rules.updateRule(changed_by=changed_by, rule_id=rule_id, what=what,
            old_data_version=form.data_version.data, transaction=transaction)
        # find out what the next data version is
        rule = db.rules.getRuleById(rule_id, transaction=transaction)
        new_data_version = rule['data_version']
        response = make_response(json.dumps(dict(new_data_version=new_data_version)))
        response.headers['Content-Type'] = 'application/json'
        return response


class RuleHistoryView(HistoryAdminView):
    """ /rules/<rule_id>/revisions """

    def get(self, rule_id):
        rule = db.rules.getRuleById(rule_id=rule_id)
        if not rule:
            return Response(status=404,
                            response='Requested rule does not exist')

        table = db.rules.history

        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            assert page >= 1
        except (ValueError, AssertionError), msg:
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
    @requirepermission('/rules', options=[])
    def _post(self, rule_id, transaction, changed_by):
        rule_id = int(rule_id)

        change_id = request.form.get('change_id')
        if not change_id:
            return Response(status=400, response='no change_id')
        change = db.rules.history.getChange(change_id=change_id)
        if change is None:
            return Response(status=404, response='bad change_id')
        if change['rule_id'] != rule_id:
            return Response(status=404, response='bad rule_id')
        rule = db.rules.getRuleById(rule_id=rule_id)
        if rule is None:
            return Response(status=404, response='bad rule_id')
        old_data_version = rule['data_version']

        # now we're going to make a new insert based on this
        what = dict(
            throttle=change['throttle'],
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

        db.rules.updateRule(changed_by=changed_by, rule_id=rule_id, what=what,
            old_data_version=old_data_version, transaction=transaction)

        return Response("Excellent!")
