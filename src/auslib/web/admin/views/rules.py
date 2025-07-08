import flask
from flask import Response, jsonify

from auslib.global_state import dbo
from auslib.web.admin.views.base import requirelogin, transactionHandler
from auslib.web.admin.views.history import revert_to_revision
from auslib.web.admin.views.problem import problem
from auslib.web.admin.views.scheduled_changes import (
    delete_scheduled_change,
    delete_signoffs_scheduled_change,
    get_all_scheduled_change_history,
    get_by_id_scheduled_change,
    get_scheduled_change_history,
    get_scheduled_changes,
    post_enact_scheduled_change,
    post_scheduled_change,
    post_scheduled_change_history,
    post_scheduled_changes,
    post_signoffs_scheduled_change,
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


# changed_by is available via the requirelogin decorator
@requirelogin
@transactionHandler
def post_rules(rule, transaction, changed_by):
    # a Post here creates a new rule
    what, mapping_values, fallback_mapping_values = process_rule_form(rule)

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


def update_rules_id_or_alias(rule, id_or_alias, transaction, changed_by):
    # Verify that the rule_id or alias exists.
    existing_rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
    if not existing_rule:
        return problem(status=404, title="Not Found", detail="Requested rule wasn't found", ext={"exception": "Requested rule does not exist"})

    what, mapping_values, fallback_mapping_values = process_rule_form(rule)

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
    existing_rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
    return jsonify(new_data_version=existing_rule["data_version"])


# changed_by is available via the requirelogin decorator
@requirelogin
@transactionHandler
def post_rules_id_or_alias(rule, id_or_alias, transaction, changed_by):
    return update_rules_id_or_alias(rule, id_or_alias, transaction, changed_by)


@requirelogin
@transactionHandler
def put_rules_id_or_alias(rule, id_or_alias, transaction, changed_by):
    return update_rules_id_or_alias(rule, id_or_alias, transaction, changed_by)


@requirelogin
@transactionHandler
def delete_rules_id_or_alias(id_or_alias, data_version, transaction, changed_by):
    # Verify that the rule_id or alias exists.
    rule = dbo.rules.getRule(id_or_alias, transaction=transaction)
    if not rule:
        return problem(status=404, title="Not Found", detail="Requested rule wasn't found", ext={"exception": "Requested rule does not exist"})

    # Bodies are ignored for DELETE requests, so we need to look at the request arguments instead.
    dbo.rules.delete(where={"rule_id": id_or_alias}, changed_by=changed_by, old_data_version=data_version, transaction=transaction)

    return Response(status=200)


def _get_what_rule_history_api(change):
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
@transactionHandler
def post_rules_revisions(rule_id, transaction, changed_by, **kwargs):
    return revert_to_revision(
        table=dbo.rules,
        get_object_callback=lambda: dbo.rules.getRule(rule_id),
        change_field="rule_id",
        get_what_callback=_get_what_rule_history_api,
        changed_by=changed_by,
        response_message="Excellent!",
        transaction=transaction,
        obj_not_found_msg="bad rule_id",
    )


def get_single_rule_column(column):
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


def get_rules_scheduled_changes():
    where = {}
    rule_id = flask.request.args.get("rule_id")
    if rule_id:
        where["base_rule_id"] = rule_id

    return get_scheduled_changes(table=dbo.rules, where=where)


@requirelogin
@transactionHandler
def post_rules_scheduled_changes(sc_rule_body, transaction, changed_by):
    if sc_rule_body.get("when", None) is None:
        return problem(400, "Bad Request", "'when' cannot be set to null when scheduling a new change " "for a Rule")
    if sc_rule_body:
        change_type = sc_rule_body.get("change_type")
    else:
        change_type = flask.request.values.get("change_type")

    what = {}
    delete_change_type_allowed_fields = ["telemetry_product", "telemetry_channel", "telemetry_uptake", "when", "rule_id", "data_version", "change_type"]
    for field in sc_rule_body:
        # TODO: currently UI passes extra rule model fields in change_type == 'delete' request body. Fix it and
        # TODO: change the below operation from filter/pop to throw Error when extra fields are passed.
        if (change_type == "insert" and field in ["rule_id", "data_version"]) or (change_type == "delete" and field not in delete_change_type_allowed_fields):
            continue

        if field in ["rule_id", "data_version"]:
            what[field] = int(sc_rule_body[field])
        else:
            what[field] = sc_rule_body[field]

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

    return post_scheduled_changes(sc_table=dbo.rules.scheduled_changes, what=what, transaction=transaction, changed_by=changed_by, change_type=change_type)


def get_by_id_rules_scheduled_change(sc_id):
    return get_by_id_scheduled_change(table=dbo.rules, sc_id=sc_id)


@requirelogin
@transactionHandler
def post_rules_scheduled_change(sc_id, sc_rule_body, transaction, changed_by):
    # TODO: modify UI and clients to stop sending 'change_type' in request body
    sc_table = dbo.rules.scheduled_changes
    sc_rule = sc_table.select(where={"sc_id": sc_id}, transaction=transaction, columns=["change_type"])
    if sc_rule:
        change_type = sc_rule[0]["change_type"]
    else:
        return problem(404, "Not Found", "Unknown sc_id", ext={"exception": "No scheduled change for rule found for given sc_id"})

    what = {}
    for field in sc_rule_body:
        # Unlike when scheduling a new change to an existing rule, rule_id is not
        # required (or even allowed) when modifying a scheduled change for an
        # existing rule. Allowing it to be modified would be confusing.
        if (
            field in ["rule_id", "sc_data_version"]
            or (change_type == "insert" and field == "data_version")
            or (change_type == "delete" and field not in ["sc_data_version", "when", "telemetry_product", "telemetry_channel", "telemetry_uptake"])
        ):
            continue

        what[field] = sc_rule_body[field]

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

    return post_scheduled_change(
        sc_table=sc_table, sc_id=sc_id, what=what, transaction=transaction, changed_by=changed_by, old_sc_data_version=sc_rule_body.get("sc_data_version", None)
    )


@requirelogin
@transactionHandler
def delete_rules_scheduled_change(sc_id, data_version, transaction, changed_by):
    return delete_scheduled_change(sc_table=dbo.rules.scheduled_changes, sc_id=sc_id, data_version=data_version, transaction=transaction, changed_by=changed_by)


@requirelogin
@transactionHandler
def post_rules_enact_scheduled_change(sc_id, transaction, changed_by):
    return post_enact_scheduled_change(sc_table=dbo.rules.scheduled_changes, sc_id=sc_id, transaction=transaction, changed_by=changed_by)


@requirelogin
@transactionHandler
def post_rules_signoffs_scheduled_change(sc_id, sc_post_signoffs_body, transaction, changed_by):
    return post_signoffs_scheduled_change(
        signoffs_table=dbo.rules.scheduled_changes.signoffs, sc_id=sc_id, what=sc_post_signoffs_body, transaction=transaction, changed_by=changed_by
    )


@requirelogin
@transactionHandler
def delete_rules_signoffs_scheduled_change(sc_id, transaction, changed_by, **kwargs):
    return delete_signoffs_scheduled_change(signoffs_table=dbo.rules.scheduled_changes.signoffs, sc_id=sc_id, transaction=transaction, changed_by=changed_by)


def get_rules_scheduled_change_history(sc_id):
    return get_scheduled_change_history(sc_table=dbo.rules.scheduled_changes, sc_id=sc_id)


def get_all_rules_scheduled_change_history():
    return get_all_scheduled_change_history(sc_table=dbo.rules.scheduled_changes)


@requirelogin
@transactionHandler
def post_rules_scheduled_change_history(sc_id, transaction, changed_by, **kwargs):
    return post_scheduled_change_history(sc_table=dbo.rules.scheduled_changes, sc_id=sc_id, transaction=transaction, changed_by=changed_by)
