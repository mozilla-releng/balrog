import connexion
from flask import Response, jsonify

from auslib.global_state import dbo
from auslib.web.admin.views.base import AdminView, requirelogin
from auslib.web.admin.views.history import HistoryView
from auslib.web.admin.views.problem import problem
from auslib.web.admin.views.scheduled_changes import (
    EnactScheduledChangeView,
    ScheduledChangeHistoryView,
    ScheduledChangesView,
    ScheduledChangeView,
    SignoffsView,
)


def process_rule_form(form_data):
    """
    Method to process either new/existing Rule form's data without wtfForm validations
    :param form_data: input json form data in dict
    :return: dictionary of processed form field values and list of valid mapping key's value.
    """
    release_names = [
        *dbo.releases.getReleaseNames(),
        *dbo.releases_json.select(columns=[dbo.releases_json.name]),
    ]

    mapping_choices = [(item["name"], item["name"]) for item in release_names]

    csv_columns = ["locale", "distribution"]
    for column in csv_columns:
        column_data = form_data.get(column)
        if column_data:
            form_data[column] = "".join(column_data.split())

    # Replaces wtfForms validations
    rule_form_dict = dict()
    for key in form_data:
        if isinstance(form_data[key], str):
            rule_form_dict[key] = None if form_data[key].strip() == "" else form_data[key].strip()
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

    # changed_by is available via the requirelogin decorator
    @requirelogin
    def _post(self, transaction, changed_by):
        # a Post here creates a new rule
        what, mapping_values, fallback_mapping_values = process_rule_form(connexion.request.get_json())

        if what.get("mapping", None) is None:
            return problem(400, "Bad Request", "mapping value cannot be set to null/empty")

        if what.get("mapping", None) is not None and len(mapping_values) != 1:
            return problem(400, "Bad Request", "Invalid mapping value. No release name found in DB")

        if what.get("fallbackMapping") is not None and len(fallback_mapping_values) != 1:
            return problem(400, "Bad Request", "Invalid fallbackMapping value. No release name found in DB")

        alias = what.get("alias", None)
        if alias is not None and dbo.rules.getRule(alias):
            return problem(400, "Bad Request", "Rule with alias exists.")

        rule_id = dbo.rules.insert(changed_by=changed_by, transaction=transaction, **what)
        return Response(status=200, response=str(rule_id))


class SingleRuleView(AdminView):
    """/rules/:id"""

    # changed_by is available via the requirelogin decorator
    @requirelogin
    def _post(self, id_or_alias, transaction, changed_by):
        # Verify that the rule_id or alias exists.
        rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
        if not rule:
            return problem(status=404, title="Not Found", detail="Requested rule wasn't found", ext={"exception": "Requested rule does not exist"})

        what, mapping_values, fallback_mapping_values = process_rule_form(connexion.request.get_json())

        # If 'mapping' key is present in request body but is either blank/null
        if "mapping" in what and what.get("mapping", None) is None:
            return problem(400, "Bad Request", "mapping value cannot be set to null/empty")

        if what.get("mapping", None) is not None and len(mapping_values) != 1:
            return problem(400, "Bad Request", "Invalid mapping value. No release name found in DB")

        if what.get("fallbackMapping") is not None and len(fallback_mapping_values) != 1:
            return problem(400, "Bad Request", "Invalid fallbackMapping value. No release name found in DB")

        data_version = what.pop("data_version", None)

        dbo.rules.update(changed_by=changed_by, where={"rule_id": id_or_alias}, what=what, old_data_version=data_version, transaction=transaction)

        # find out what the next data version is
        rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
        return jsonify(new_data_version=rule["data_version"])

    _put = _post

    @requirelogin
    def _delete(self, id_or_alias, transaction, changed_by):
        # Verify that the rule_id or alias exists.
        rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
        if not rule:
            return problem(status=404, title="Not Found", detail="Requested rule wasn't found", ext={"exception": "Requested rule does not exist"})

        # Bodies are ignored for DELETE requests, so we need to look at the request arguments instead.
        old_data_version = int(connexion.request.args.get("data_version"))
        dbo.rules.delete(where={"rule_id": id_or_alias}, changed_by=changed_by, old_data_version=old_data_version, transaction=transaction)

        return Response(status=200)


class RuleHistoryAPIView(HistoryView):
    """/rules/:id/revisions"""

    def __init__(self):
        super(RuleHistoryAPIView, self).__init__(dbo.rules)

    def _get_what(self, change):
        what = dict(
            backgroundRate=change["backgroundRate"],
            mapping=change["mapping"],
            fallbackMapping=change["fallbackMapping"],
            priority=change["priority"],
            alias=change["alias"],
            product=change["product"],
            version=change["version"],
            buildID=change["buildID"],
            channel=change["channel"],
            locale=change["locale"],
            distribution=change["distribution"],
            buildTarget=change["buildTarget"],
            osVersion=change["osVersion"],
            instructionSet=change["instructionSet"],
            memory=change["memory"],
            distVersion=change["distVersion"],
            comment=change["comment"],
            update_type=change["update_type"],
            headerArchitecture=change["headerArchitecture"],
        )
        return what

    @requirelogin
    def _post(self, rule_id, transaction, changed_by):
        return self.revert_to_revision(
            get_object_callback=lambda: self.table.getRule(rule_id),
            change_field="rule_id",
            get_what_callback=self._get_what,
            changed_by=changed_by,
            response_message="Excellent!",
            transaction=transaction,
            obj_not_found_msg="bad rule_id",
        )


class SingleRuleColumnView(AdminView):
    """/rules/columns/:column"""

    def get(self, column):
        rules = dbo.rules.getOrderedRules()
        column_values = []
        if column not in rules[0].keys():
            return problem(status=404, title="Not Found", detail="Rule column was not found", ext={"exception": "Requested column does not exist"})

        for rule in rules:
            for key, value in rule.items():
                if key == column and value is not None:
                    column_values.append(value)
        column_values = list(set(column_values))
        ret = {"count": len(column_values), column: column_values}
        return jsonify(ret)


class RuleScheduledChangesView(ScheduledChangesView):
    """/scheduled_changes/rules"""

    def __init__(self):
        super(RuleScheduledChangesView, self).__init__("rules", dbo.rules)

    def get(self):
        where = {}
        rule_id = connexion.request.args.get("rule_id")
        if rule_id:
            where["base_rule_id"] = rule_id

        return super(RuleScheduledChangesView, self).get(where)

    @requirelogin
    def _post(self, transaction, changed_by):
        if connexion.request.get_json().get("when", None) is None:
            return problem(400, "Bad Request", "'when' cannot be set to null when scheduling a new change " "for a Rule")
        if connexion.request.get_json():
            change_type = connexion.request.get_json().get("change_type")
        else:
            change_type = connexion.request.values.get("change_type")

        what = {}
        delete_change_type_allowed_fields = ["telemetry_product", "telemetry_channel", "telemetry_uptake", "when", "rule_id", "data_version", "change_type"]
        for field in connexion.request.get_json():
            # TODO: currently UI passes extra rule model fields in change_type == 'delete' request body. Fix it and
            # TODO: change the below operation from filter/pop to throw Error when extra fields are passed.
            if (change_type == "insert" and field in ["rule_id", "data_version"]) or (
                change_type == "delete" and field not in delete_change_type_allowed_fields
            ):
                continue

            if field in ["rule_id", "data_version"]:
                what[field] = int(connexion.request.get_json()[field])
            else:
                what[field] = connexion.request.get_json()[field]

        # Explicit checks for each change_type
        if change_type in ["update", "delete"]:
            for field in ["rule_id", "data_version"]:
                if not what.get(field, None):
                    return problem(400, "Bad Request", "Missing field", ext={"exception": "%s is missing" % field})

        elif change_type == "insert":
            for field in ["update_type", "backgroundRate", "priority"]:
                if what.get(field, None) is None or isinstance(what.get(field), str) and what.get(field).strip() == "":
                    return problem(
                        400,
                        "Bad Request",
                        "Null/Empty Value",
                        ext={"exception": "%s cannot be set to null/empty " "when scheduling insertion of a new rule" % field},
                    )

        if change_type in ["update", "insert"]:
            rule_dict, mapping_values, fallback_mapping_values = process_rule_form(what)
            what = rule_dict

            # if 'mapping' key is present in request body but is null
            if "mapping" in what:
                if what.get("mapping", None) is None:
                    return problem(400, "Bad Request", "mapping value cannot be set to null/empty")

            # if 'mapping' key-value is null/not-present-in-request-body and change_type == "insert"
            if what.get("mapping", None) is None:
                if change_type == "insert":
                    return problem(400, "Bad Request", "mapping value cannot be set to null/empty")

            # If mapping is present in request body and is non-empty string which does not match any release name
            if what.get("mapping") is not None and len(mapping_values) != 1:
                return problem(400, "Bad Request", "Invalid mapping value. No release name found in DB")

            if what.get("fallbackMapping") is not None and len(fallback_mapping_values) != 1:
                return problem(400, "Bad Request", "Invalid fallbackMapping value. No release name found in DB")

            alias = what.get("alias", None)
            if alias is not None and dbo.rules.getRule(alias):
                return problem(400, "Bad Request", "Rule with alias exists.")

        return super(RuleScheduledChangesView, self)._post(what, transaction, changed_by, change_type)


class RuleScheduledChangeView(ScheduledChangeView):
    """/scheduled_changes/rules/<int:sc_id>"""

    def __init__(self):
        super(RuleScheduledChangeView, self).__init__("rules", dbo.rules)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        # TODO: modify UI and clients to stop sending 'change_type' in request body
        sc_rule = self.sc_table.select(where={"sc_id": sc_id}, transaction=transaction, columns=["change_type"])
        if sc_rule:
            change_type = sc_rule[0]["change_type"]
        else:
            return problem(404, "Not Found", "Unknown sc_id", ext={"exception": "No scheduled change for rule found for given sc_id"})

        what = {}
        for field in connexion.request.get_json():
            # Unlike when scheduling a new change to an existing rule, rule_id is not
            # required (or even allowed) when modifying a scheduled change for an
            # existing rule. Allowing it to be modified would be confusing.
            if (
                field in ["rule_id", "sc_data_version"]
                or (change_type == "insert" and field == "data_version")
                or (change_type == "delete" and field not in ["sc_data_version", "when", "telemetry_product", "telemetry_channel", "telemetry_uptake"])
            ):
                continue

            what[field] = connexion.request.get_json()[field]

        if change_type == "update" and not what.get("data_version", None):
            return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})

        elif change_type == "insert":
            # edit scheduled change for new rule
            for field in ["update_type", "backgroundRate", "priority"]:
                if field in what and what.get(field) is None or isinstance(what.get(field), str) and what.get(field).strip() == "":
                    return problem(
                        400, "Bad Request", "Null/Empty Value", ext={"exception": "%s cannot be set to null " "when scheduling insertion of a new rule" % field}
                    )

        if change_type in ["update", "insert"]:
            rule_dict, mapping_values, fallback_mapping_values = process_rule_form(what)
            what = rule_dict

            # If 'mapping' key is present in request body but is null
            if "mapping" in what and what.get("mapping", None) is None:
                return problem(400, "Bad Request", "mapping value cannot be set to null/empty")

            # If 'mapping' key is present in request body and is non-empty string which does not match any release name
            if what.get("mapping") is not None and len(mapping_values) != 1:
                return problem(400, "Bad Request", "Invalid mapping value. No release name found in DB")

            if what.get("fallbackMapping") is not None and len(fallback_mapping_values) != 1:
                return problem(400, "Bad Request", "Invalid fallbackMapping value. No release name found in DB")

            # if a rule is present with another alias
            alias = what.get("alias", None)
            if alias is not None and dbo.rules.getRule(alias):
                return problem(400, "Bad Request", "Rule with alias exists.")

        return super(RuleScheduledChangeView, self)._post(sc_id, what, transaction, changed_by, connexion.request.get_json().get("sc_data_version", None))

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
    """/scheduled_changes/rules/<int:sc_id>/revisions"""

    def __init__(self):
        super(RuleScheduledChangeHistoryView, self).__init__("rules", dbo.rules)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(RuleScheduledChangeHistoryView, self)._post(sc_id, transaction, changed_by)
