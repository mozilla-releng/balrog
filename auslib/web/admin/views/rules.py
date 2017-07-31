import json
import connexion

from sqlalchemy.sql.expression import null
from jsonschema.compat import str_types
from flask import Response, jsonify
from auslib.web.admin.views.problem import problem
from auslib.global_state import dbo
from auslib.web.admin.views.base import (
    requirelogin, AdminView
)
from auslib.web.admin.views.csrf import get_csrf_headers
from auslib.web.admin.views.forms import EditScheduledChangeNewRuleForm, \
    EditScheduledChangeExistingRuleForm, EditScheduledChangeDeleteRuleForm
from auslib.web.admin.views.scheduled_changes import ScheduledChangesView, \
    ScheduledChangeView, EnactScheduledChangeView, ScheduledChangeHistoryView,\
    SignoffsView
from auslib.web.admin.views.history import HistoryView


def process_rule_form(form_data):
    """
    Method to process either new/existing Rule form's data without wtfForm validations
    :param form_data: input json form data in dict
    :return: dictionary of processed form field values and list of valid mapping key's value.
    """
    release_names = dbo.releases.getReleaseNames()

    mapping_choices = [(item['name'], item['name']) for item in release_names]
    mapping_choices.insert(0, ('', 'NULL'))

    # Replaces wtfForms validations
    rule_form_dict = dict()
    for key in form_data:
        if isinstance(form_data[key], str_types):
            rule_form_dict[key] = None if form_data[key].strip() == '' else form_data[key].strip()
        else:
            rule_form_dict[key] = form_data[key]

    for i in ["priority", "backgroundRate", "data_version"]:
        if rule_form_dict.get(i, None):
            rule_form_dict[i] = int(rule_form_dict[i])

    mapping_values = [y for x, y in mapping_choices if x == rule_form_dict.get("mapping")]
    fallback_mapping_values = [y for x, y in mapping_choices if x == rule_form_dict.get("fallbackMapping")]

    return rule_form_dict, mapping_values, fallback_mapping_values


class RulesAPIView(AdminView):
    """/rules"""

    def get(self, **kwargs):
        # We can't use a form here because it will enforce "csrf_token" needing
        # to exist, which doesn't make sense for GET requests.
        where = {}
        for field in ("product",):
            if connexion.request.args.get(field):
                where[field] = connexion.request.args[field]

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
        what, mapping_values, fallback_mapping_values = process_rule_form(connexion.request.json)

        if what.get('mapping', None) is not None and len(mapping_values) != 1:
            return problem(400, 'Bad Request', 'Invalid mapping value. No release name found in DB')

        if what.get('fallbackMapping', None) is not None and len(fallback_mapping_values) != 1:
            return problem(400, 'Bad Request', 'Invalid fallbackMapping value. No release name found in DB')

        # Solves Bug https://bugzilla.mozilla.org/show_bug.cgi?id=1361158
        what.pop("csrf_token", None)

        alias = what.get('alias', None)
        if alias is not None and dbo.rules.getRule(alias):
            return problem(400, 'Bad Request', 'Rule with alias exists.')

        rule_id = dbo.rules.insert(changed_by=changed_by, transaction=transaction, **what)
        return Response(status=200, response=str(rule_id))


class SingleRuleView(AdminView):
    """ /rules/:id"""

    def get(self, id_or_alias):
        rule = dbo.rules.getRule(id_or_alias)
        if not rule:
            return problem(status=404, title="Not Found", detail="Requested rule wasn't found",
                           ext={"exception": "Requested rule does not exist"})

        headers = {'X-Data-Version': rule['data_version']}
        headers.update(get_csrf_headers())

        return Response(response=json.dumps(rule), mimetype="application/json", headers=headers)

    # changed_by is available via the requirelogin decorator
    @requirelogin
    def _post(self, id_or_alias, transaction, changed_by):
        # Verify that the rule_id or alias exists.
        rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
        if not rule:
            return problem(status=404, title="Not Found", detail="Requested rule wasn't found",
                           ext={"exception": "Requested rule does not exist"})

        what, mapping_values, fallback_mapping_values = process_rule_form(connexion.request.json)

        if what.get('mapping', None) is not None and len(mapping_values) != 1:
            return problem(400, 'Bad Request', 'Invalid mapping value. No release name found in DB')

        if what.get('fallbackMapping', None) is not None and len(fallback_mapping_values) != 1:
            return problem(400, 'Bad Request', 'Invalid fallbackMapping value. No release name found in DB')

        # Solves https://bugzilla.mozilla.org/show_bug.cgi?id=1361158
        what.pop("csrf_token", None)
        data_version = what.pop("data_version", None)

        dbo.rules.update(changed_by=changed_by, where={"rule_id": id_or_alias}, what=what,
                         old_data_version=data_version, transaction=transaction)

        # find out what the next data version is
        rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
        return jsonify(new_data_version=rule["data_version"])

    _put = _post

    @requirelogin
    def _delete(self, id_or_alias, transaction, changed_by):
        # Verify that the rule_id or alias exists.
        rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
        if not rule:
            return problem(status=404, title="Not Found", detail="Requested rule wasn't found",
                           ext={"exception": "Requested rule does not exist"})

        # Bodies are ignored for DELETE requests, so we need to look at the request arguments instead.
        # Even though we aren't going to use most of the form fields (just
        # rule_id and data_version), we still want to create and validate the
        # form to make sure that the CSRF token is checked.

        old_data_version = int(connexion.request.args.get("data_version"))
        dbo.rules.delete(where={"rule_id": id_or_alias}, changed_by=changed_by,
                         old_data_version=old_data_version,
                         transaction=transaction)

        return Response(status=200)


class RuleHistoryAPIView(HistoryView):
    """/rules/:id/revisions"""

    def __init__(self):
        super(RuleHistoryAPIView, self).__init__(dbo.rules)

    def _process_revisions(self, revisions):
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
            'instructionSet': 'instructionSet',
            'memory': 'memory',
            'distVersion': 'distVersion',
            'comment': 'comment',
            'update_type': 'update_type',
            'headerArchitecture': 'headerArchitecture',
            'data_version': 'data_version',
            # specific to revisions
            'change_id': 'change_id',
            'timestamp': 'timestamp',
            'changed_by': 'changed_by',
        }

        _rules = []

        for rule in revisions:
            _rules.append(dict(
                (key, rule[db_key])
                for key, db_key in _mapping.items()
            ))

        return _rules

    def _get_filters(self, rule):
        return [self.history_table.rule_id == rule['rule_id'],
                self.history_table.data_version != null()]

    def _get_what(self, change):
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
            instructionSet=change['instructionSet'],
            memory=change['memory'],
            distVersion=change['distVersion'],
            comment=change['comment'],
            update_type=change['update_type'],
            headerArchitecture=change['headerArchitecture'],
        )
        return what

    def get(self, rule_id):
        try:
            return self.get_revisions(
                get_object_callback=lambda: self.table.getRule(rule_id),
                history_filters_callback=self._get_filters,
                process_revisions_callback=self._process_revisions,
                revisions_order_by=[self.history_table.timestamp.desc()],
                obj_not_found_msg='Requested rule does not exist',
                response_key='rules')
        # Adding AttributeError to accommodate exception thrown when no rule
        # is found when db.getRule method is invoked
        except (ValueError, AttributeError) as msg:
            self.log.warning("Bad input: %s", msg)
            return problem(400, "Bad Request", "Error occurred when trying to fetch"
                                               " Rule's revisions having rule_id {0}".format(rule_id),
                           ext={"exception": str(msg)})

    @requirelogin
    def _post(self, rule_id, transaction, changed_by):
        return self.revert_to_revision(
            get_object_callback=lambda: self.table.getRule(rule_id),
            change_field='rule_id',
            get_what_callback=self._get_what,
            changed_by=changed_by,
            response_message='Excellent!',
            transaction=transaction,
            obj_not_found_msg='bad rule_id')


class SingleRuleColumnView(AdminView):
    """/rules/columns/:column"""

    def get(self, column):
        rules = dbo.rules.getOrderedRules()
        column_values = []
        if column not in rules[0].keys():
            return problem(status=404, title="Not Found", detail="Rule column was not found",
                           ext={"exception": "Requested column does not exist"})

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
    """/scheduled_changes/rules"""

    def __init__(self):
        super(RuleScheduledChangesView, self).__init__("rules", dbo.rules)

    @requirelogin
    def _post(self, transaction, changed_by):
        if connexion.request.json:
            change_type = connexion.request.json.get("change_type")
        else:
            change_type = connexion.request.values.get("change_type")

        what = {}
        delete_change_type_allowed_fields = ["telemetry_product", "telemetry_channel", "telemetry_uptake", "when",
                                             "rule_id", "data_version", "change_type"]
        for field in connexion.request.json:
            # TODO: currently UI passes extra rule model fields in change_type == 'delete' request body. Fix it and
            # TODO: change the below operation from filter/pop to throw Error when extra fields are passed.
            if (field == "csrf_token" or (change_type == "insert" and field in ["rule_id", "data_version"]) or
                    (change_type == "delete" and field not in delete_change_type_allowed_fields)):
                continue

            if field in ["rule_id", "data_version"]:
                what[field] = int(connexion.request.json[field])
            else:
                what[field] = connexion.request.json[field]

        # Explicit checks for each change_type
        if change_type in ["update", "delete"]:
            for field in ["rule_id", "data_version"]:
                if not what.get(field, None):
                    return problem(400, "Bad Request", "Missing field", ext={"exception": "%s is missing" % field})

        elif change_type == "insert":
            for field in ["update_type", "backgroundRate", "priority"]:
                if not what.get(field, None):
                    return problem(400, "Bad Request", "Missing field", ext={"exception": "%s is missing" % field})
        else:
            return problem(400, "Bad Request", "Invalid or missing change_type")

        if change_type in ["update", "insert"]:
            rule_dict, mapping_values, fallback_mapping_values = process_rule_form(what)
            what = rule_dict
            if what.get('mapping') is not None and len(mapping_values) != 1:
                return problem(400, 'Bad Request', 'Invalid mapping value. No release name found in DB')

            if what.get('fallbackMapping') is not None and len(fallback_mapping_values) != 1:
                return problem(400, 'Bad Request', 'Invalid fallbackMapping value. No release name found in DB')

        return super(RuleScheduledChangesView, self)._post(what, transaction, changed_by, change_type)


class RuleScheduledChangeView(ScheduledChangeView):
    def __init__(self):
        super(RuleScheduledChangeView, self).__init__("rules", dbo.rules)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        if connexion.request.json and connexion.request.json.get("data_version"):
            if connexion.request.json.get("change_type") == "delete":
                form = EditScheduledChangeDeleteRuleForm()
            else:
                form = EditScheduledChangeExistingRuleForm()
        else:
            form = EditScheduledChangeNewRuleForm()

        if connexion.request.json.get("change_type") != "delete":
            release_names = dbo.releases.getReleaseNames(transaction=transaction)

            form.mapping.choices = [(item['name'], item['name']) for item in release_names]
            form.mapping.choices.insert(0, ('', 'NULL'))

        return super(RuleScheduledChangeView, self)._post(sc_id, form, transaction, changed_by)

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(RuleScheduledChangeView, self)._delete(sc_id, transaction, changed_by)


class EnactRuleScheduledChangeView(EnactScheduledChangeView):
    """/scheduled_changes/rules/<int:sc_id>/enact"""

    def __init__(self):
        super(EnactRuleScheduledChangeView, self).__init__("rules", dbo.rules)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(EnactRuleScheduledChangeView, self)._post(sc_id, transaction, changed_by)


class RuleScheduledChangeSignoffsView(SignoffsView):
    """/scheduled_changes/rules/<int:sc_id>/signoffs"""

    def __init__(self):
        super(RuleScheduledChangeSignoffsView, self).__init__("rules", dbo.rules)


class RuleScheduledChangeHistoryView(ScheduledChangeHistoryView):
    def __init__(self):
        super(RuleScheduledChangeHistoryView, self).__init__("rules", dbo.rules)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(RuleScheduledChangeHistoryView, self)._post(sc_id, transaction, changed_by)
