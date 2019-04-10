import logging
import operator

import simplejson as json
from flask_wtf import FlaskForm as Form
from six import text_type
from wtforms import BooleanField, IntegerField, SelectField, StringField
from wtforms.validators import InputRequired, Length, NumberRange, Optional, Regexp, ValidationError
from wtforms.widgets import FileInput, HiddenInput, TextInput

from auslib.util.comparison import get_op
from auslib.util.timestamp import getMillisecondTimestamp
from auslib.util.versions import MozillaVersion

log = logging.getLogger(__name__)


# If present, rule alias' must be a string containing at least one non-numeric character.
RULE_ALIAS_REGEXP = "(^[a-zA-Z][a-zA-Z0-9-]*$|^$)"


class DisableableTextInput(TextInput):
    """A TextInput widget that supports being disabled."""

    def __init__(self, disabled, *args, **kwargs):
        self.disabled = disabled
        TextInput.__init__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.disabled:
            kwargs["disabled"] = "disabled"
        return TextInput.__call__(self, *args, **kwargs)


class JSONStringField(StringField):
    """StringField that parses incoming data as JSON."""

    def __init__(self, default_value, *args, **kwargs):
        self.default_value = default_value
        super(JSONStringField, self).__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            try:
                self.data = json.loads(valuelist[0])
            # XXX: use JSONDecodeError when the servers support it
            except ValueError as e:
                # WTForms catches ValueError, which JSONDecodeError is a child
                # of. Because of this, we need to wrap this error in something
                # else in order for it to be properly raised.
                log.debug("Caught ValueError")
                self.process_errors.append(e.args[0])
        else:
            log.debug("No value list, setting self.data to default")
            self._set_default()

    def _set_default(self):
        self.data = self.default_value

    def _value(self):
        return json.dumps(self.data) if self.data is not None else ""


class NullableStringField(StringField):
    """StringField that parses incoming data converting empty strings to None's."""

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            if valuelist[0] == "":
                log.debug("data is empty string, setting it to NULL")
                self.data = None
            else:
                self.data = valuelist[0]
        else:
            log.debug("No value list, setting self.data to None")
            self.data = None


def NoneOrType(type_):
    """A helper method for SelectField's that returns the value coerced to
       the specified type when it is not None. By default, a SelectField coerces
       None to unicode, which ends up as u'None'."""

    def coercer(value):
        if value is None:
            return value
        else:
            return type_(value)

    return coercer


def operator_validator():
    log.debug("starting in operator_validator for buildID")

    def _validator(form, field):
        log.debug("starting in operator_validator: field.data is %s" % field.data)
        # empty input is fine
        if field.data is None:
            return
        try:
            op, operand = get_op(field.data)
            log.debug("Got (%s, %s) from get_op", op, operand)
        except TypeError:
            # get_op field returns None if no operator or no match, can't be unpacked
            raise ValidationError("Invalid input for %s. No Operator or Match found." % field.name)

    return _validator


def version_validator():
    log.debug("starting in version_validator for version")

    def _validator(form, field):
        log.debug("starting in version_validator: field.data is %s" % field.data)
        # empty input
        if field.data is None:
            return
        rulesVersionList = field.data.split(",")
        isListOfVersions = len(rulesVersionList) > 1
        for rule_version in rulesVersionList:
            try:
                op, operand = get_op(rule_version)
                if isListOfVersions and op != operator.eq:
                    raise ValidationError("Invalid input for %s .Relational Operators are not allowed" " when providing a list of versions." % field.name)
                version = MozillaVersion(operand)
            except ValidationError:
                raise
            except ValueError:
                raise ValidationError("ValueError. Couldn't parse version for %s. Invalid '%s' input value" % (field.name, field.name))
            except Exception:
                raise ValidationError("Invalid input for %s . No Operator or Match found." % field.name)
            # MozillaVersion doesn't error on empty strings
            if not hasattr(version, "version"):
                raise ValidationError("Couldn't parse the version for %s. No attribute 'version' was detected." % field.name)

    return _validator


def not_in_the_past():
    def _validator(form, field):
        if field.data is None:
            return

        if field.data < getMillisecondTimestamp():
            raise ValidationError("Changes may not be scheduled in the past")

    return _validator


class DbEditableForm(Form):
    data_version = IntegerField("data_version", validators=[InputRequired()], widget=HiddenInput())


class ScheduledChangeTimeForm(Form):
    when = IntegerField("When", validators=[Optional(), not_in_the_past()])


class ScheduledChangeUptakeForm(Form):
    telemetry_product = NullableStringField("Telemetry Product")
    telemetry_channel = NullableStringField("Telemetry Channel")
    telemetry_uptake = NullableStringField("Telemetry Uptake")


class NewPermissionForm(Form):
    options = JSONStringField(None, "Options")


class ExistingPermissionForm(DbEditableForm):
    options = JSONStringField(None, "Options")


class ScheduledChangeNewPermissionForm(ScheduledChangeTimeForm):
    """Permission and username are required when creating a new Permission, so they
    must be provided when Scheduled a Change that does the same. Options may also be
    provided."""

    permission = StringField("Permission", validators=[Length(0, 50), InputRequired()])
    username = StringField("Username", validators=[Length(0, 100), InputRequired()])
    options = JSONStringField(None, "Options")
    change_type = SelectField("Change Type", choices=[("insert", "insert")])


class ScheduledChangeExistingPermissionForm(ScheduledChangeTimeForm):
    """Permissions and username are required when Scheduling a Change that changes
    an existing Permission because they are needed to find that Permission. Options
    may also be provided."""

    permission = StringField("Permission", validators=[Length(0, 50), InputRequired()])
    username = StringField("Username", validators=[Length(0, 100), InputRequired()])
    options = JSONStringField(None, "Options")
    data_version = IntegerField("data_version", validators=[InputRequired()], widget=HiddenInput())
    change_type = SelectField("Change Type", choices=[("update", "update")])


class ScheduledChangeDeletePermissionForm(ScheduledChangeTimeForm):
    """Permissions and username are required when Scheduling a Change that deletes
    an existing Permission because they are needed to find that Permission."""

    permission = StringField("Permission", validators=[Length(0, 50), InputRequired()])
    username = StringField("Username", validators=[Length(0, 100), InputRequired()])
    data_version = IntegerField("data_version", validators=[InputRequired()], widget=HiddenInput())
    change_type = SelectField("Change Type", choices=[("delete", "delete")])


class EditScheduledChangeNewPermissionForm(ScheduledChangeTimeForm):
    """When editing an existing Scheduled Change for a Permission, any field
    may be changed."""

    permission = StringField("Permission", validators=[Length(0, 50), Optional()])
    username = StringField("Username", validators=[Length(0, 100), Optional()])
    options = JSONStringField(None, "Options")
    sc_data_version = IntegerField("sc_data_version", validators=[InputRequired()], widget=HiddenInput())


class EditScheduledChangeExistingPermissionForm(ScheduledChangeTimeForm):
    """When editing an existing Scheduled Change for a Permission only options may be
    provided. Because edits are identified by sc_id (in the URL), permission and username
    are not required (nor allowed, because they are PK fields)."""

    options = JSONStringField(None, "Options")
    data_version = IntegerField("data_version", widget=HiddenInput())
    sc_data_version = IntegerField("sc_data_version", validators=[InputRequired()], widget=HiddenInput())


class PartialReleaseForm(Form):
    # Because we do implicit release creation in the Releases views, we can't
    # have data_version be InputRequired(). The views are responsible for checking
    # for its existence in this case.
    data_version = IntegerField("data_version", widget=HiddenInput())
    product = StringField("Product", validators=[InputRequired()])
    hashFunction = StringField("Hash Function")
    data = JSONStringField({}, "Data", validators=[InputRequired()])
    schema_version = IntegerField("Schema Version")
    copyTo = JSONStringField({}, "Copy To", default=list)
    alias = JSONStringField({}, "Alias", default=list)


class RuleForm(Form):
    backgroundRate = IntegerField("Background Rate", validators=[NumberRange(0, 100, "Background rate must be between 0 and 100")])
    priority = IntegerField("Priority", validators=[NumberRange(min=0, message="Priority must be a non-negative integer")])
    mapping = SelectField("Mapping", validators=[])
    fallbackMapping = NullableStringField("fallbackMapping", validators=[Optional()])
    alias = NullableStringField("Alias", validators=[Length(0, 50), Regexp(RULE_ALIAS_REGEXP)])
    product = NullableStringField("Product", validators=[Length(0, 15)])
    version = NullableStringField("Version", validators=[Length(0, 75), version_validator()])
    buildID = NullableStringField("BuildID", validators=[Length(0, 20), operator_validator()])
    channel = NullableStringField("Channel", validators=[Length(0, 75)])
    locale = NullableStringField("Locale", validators=[Length(0, 200)])
    distribution = NullableStringField("Distribution", validators=[Length(0, 100)])
    buildTarget = NullableStringField("Build Target", validators=[Length(0, 75)])
    osVersion = NullableStringField("OS Version", validators=[Length(0, 1000)])
    instructionSet = NullableStringField("InstructionSet", validators=[Length(0, 1000)])
    memory = NullableStringField("Memory", validators=[Length(0, 100)])
    distVersion = NullableStringField("Dist Version", validators=[Length(0, 100)])
    comment = NullableStringField("Comment", validators=[Length(0, 500)])
    update_type = SelectField("Update Type", choices=[("minor", "minor"), ("major", "major")], validators=[])
    headerArchitecture = NullableStringField("Header Architecture", validators=[Length(0, 10)])


class EditRuleForm(DbEditableForm):
    backgroundRate = IntegerField("Background Rate", validators=[Optional(), NumberRange(0, 100)])
    priority = IntegerField("Priority", validators=[Optional()])
    mapping = SelectField("Mapping", validators=[Optional()], coerce=NoneOrType(text_type))
    fallbackMapping = NullableStringField("fallbackMapping", validators=[Optional()])
    alias = NullableStringField("Alias", validators=[Optional(), Length(0, 50), Regexp(RULE_ALIAS_REGEXP)])
    product = NullableStringField("Product", validators=[Optional(), Length(0, 15)])
    version = NullableStringField("Version", validators=[Optional(), Length(0, 75), version_validator()])
    buildID = NullableStringField("BuildID", validators=[Optional(), Length(0, 20), operator_validator()])
    channel = NullableStringField("Channel", validators=[Optional(), Length(0, 75)])
    locale = NullableStringField("Locale", validators=[Optional(), Length(0, 200)])
    distribution = NullableStringField("Distribution", validators=[Optional(), Length(0, 100)])
    buildTarget = NullableStringField("Build Target", validators=[Optional(), Length(0, 75)])
    osVersion = NullableStringField("OS Version", validators=[Optional(), Length(0, 1000)])
    instructionSet = NullableStringField("InstructionSet", validators=[Optional(), Length(0, 1000)])
    memory = NullableStringField("Memory", validators=[Optional(), Length(0, 100)])
    distVersion = NullableStringField("Dist Version", validators=[Optional(), Length(0, 100)])
    comment = NullableStringField("Comment", validators=[Optional(), Length(0, 500)])
    update_type = SelectField("Update Type", choices=[("minor", "minor"), ("major", "major")], validators=[Optional()], coerce=NoneOrType(text_type))
    headerArchitecture = NullableStringField("Header Architecture", validators=[Optional(), Length(0, 10)])


class ScheduledChangeNewRuleForm(ScheduledChangeTimeForm, ScheduledChangeUptakeForm, RuleForm):
    change_type = SelectField("Change Type", choices=[("insert", "insert")])


class ScheduledChangeExistingRuleForm(ScheduledChangeTimeForm, ScheduledChangeUptakeForm, EditRuleForm):
    # EditRuleForm doesn't have rule_id in it because rules are edited through
    # URLs that contain them. Scheduled changes, on the other hand, are edited
    # through URLs that contain scheduled change IDs, so we need to include
    # the rule_id in the form when editing scheduled changes for rules.
    rule_id = IntegerField("Rule ID", validators=[InputRequired()])
    change_type = SelectField("Change Type", choices=[("update", "update")])


class ScheduledChangeDeleteRuleForm(ScheduledChangeTimeForm, ScheduledChangeUptakeForm):
    """
    ScheduledChangeDeletionForm includes all the PK columns ,ScheduledChangeForm columns and data version
    """

    rule_id = IntegerField("Rule ID", validators=[InputRequired()])
    data_version = IntegerField("data_version", validators=[InputRequired()], widget=HiddenInput())
    change_type = SelectField("Change Type", choices=[("delete", "delete")])


class EditScheduledChangeNewRuleForm(ScheduledChangeTimeForm, ScheduledChangeUptakeForm, RuleForm):
    sc_data_version = IntegerField("sc_data_version", validators=[InputRequired()], widget=HiddenInput())


# Unlike when scheduling a new change to an existing rule, rule_id is not
# required (or even allowed) when modifying a scheduled change for an
# existing rule. Allowing it to be modified would be confusing.
class EditScheduledChangeExistingRuleForm(ScheduledChangeTimeForm, ScheduledChangeUptakeForm, EditRuleForm):
    sc_data_version = IntegerField("sc_data_version", validators=[InputRequired()], widget=HiddenInput())


class EditScheduledChangeDeleteRuleForm(ScheduledChangeTimeForm, ScheduledChangeUptakeForm):
    sc_data_version = IntegerField("sc_data_version", validators=[InputRequired()], widget=HiddenInput())


class SignoffForm(Form):
    role = StringField("Role", validators=[InputRequired()])


class CompleteReleaseForm(Form):
    name = StringField("Name", validators=[InputRequired()])
    product = StringField("Product", validators=[InputRequired()])
    blob = JSONStringField({}, "Data", validators=[InputRequired()], widget=FileInput())
    data_version = IntegerField("data_version", widget=HiddenInput())


class ReadOnlyForm(Form):
    name = StringField("Name", validators=[InputRequired()])
    product = StringField("Product", validators=[InputRequired()])
    read_only = BooleanField("read_only")
    data_version = IntegerField("data_version", widget=HiddenInput())


class ScheduledChangeNewReleaseForm(ScheduledChangeTimeForm):
    """All Release fields (name, product, data) are required when creating
    a new Release, so they must be provided when Scheduling a Change that
    does the same."""

    name = StringField("Name", validators=[InputRequired()])
    product = StringField("Product", validators=[InputRequired()])
    data = JSONStringField({}, "Data", validators=[InputRequired()], widget=FileInput())
    change_type = SelectField("Change Type", choices=[("insert", "insert")])


class ScheduledChangeExistingReleaseForm(ScheduledChangeTimeForm):
    """Name must be provided when Scheduling a Change that modifies an existing
    Release so that we can identify it. Other Release fields (product, data) are
    optional."""

    name = StringField("Name", validators=[InputRequired()])
    product = StringField("Product", validators=[Optional()])
    data = JSONStringField({}, "Data", validators=[Optional()], widget=FileInput())
    data_version = IntegerField("data_version", validators=[InputRequired()], widget=HiddenInput())
    change_type = SelectField("Change Type", choices=[("update", "update")])


class ScheduledChangeDeleteReleaseForm(ScheduledChangeTimeForm):
    """Name must be provided when Scheduling a Change that deletes an
    existing Permission so that we can find it."""

    name = StringField("Name", validators=[InputRequired()])
    data_version = IntegerField("data_version", validators=[InputRequired()], widget=HiddenInput())
    change_type = SelectField("Change Type", choices=[("delete", "delete")])


class EditScheduledChangeNewReleaseForm(ScheduledChangeTimeForm):
    """Any Release field may be changed when editing an Scheduled Change for a new
    Release."""

    name = StringField("Name", validators=[Optional()])
    product = StringField("Product", validators=[Optional()])
    data = JSONStringField(None, "Data", validators=[Optional()], widget=FileInput())
    sc_data_version = IntegerField("sc_data_version", validators=[InputRequired()], widget=HiddenInput())


class EditScheduledChangeExistingReleaseForm(ScheduledChangeTimeForm):
    """Only data may be changed when editing an existing Scheduled Change for
    a Release. Name cannot be changed because it is a PK field, and product
    cannot be changed because it almost never makes sense to (and can be done
    by deleting/recreating instead)."""

    data = JSONStringField(None, "Data", validators=[Optional()], widget=FileInput())
    data_version = IntegerField("data_version", widget=HiddenInput())
    sc_data_version = IntegerField("sc_data_version", validators=[InputRequired()], widget=HiddenInput())


class ProductRequiredSignoffForm(Form):
    product = StringField("Product", validators=[Length(0, 15), InputRequired()])
    channel = StringField("Channel", validators=[Length(0, 75), InputRequired()])
    role = StringField("Role", validators=[InputRequired()])
    signoffs_required = IntegerField("Signoffs Required", validators=[InputRequired()])


class ProductRequiredSignoffHistoryForm(Form):
    product = StringField("Product", validators=[Length(0, 15), InputRequired()])
    channel = StringField("Channel", validators=[Length(0, 75), InputRequired()])
    role = StringField("Role", validators=[InputRequired()])


class ScheduledChangeNewProductRequiredSignoffForm(ScheduledChangeTimeForm):
    product = StringField("Product", validators=[Length(0, 15), InputRequired()])
    channel = StringField("Channel", validators=[Length(0, 75), InputRequired()])
    role = StringField("Role", validators=[InputRequired()])
    signoffs_required = IntegerField("Signoffs Required", validators=[InputRequired()])
    change_type = SelectField("Change Type", choices=[("insert", "insert")])


class ScheduledChangeExistingProductRequiredSignoffForm(ScheduledChangeTimeForm):
    product = StringField("Product", validators=[Length(0, 15), InputRequired()])
    channel = StringField("Channel", validators=[Length(0, 75), InputRequired()])
    role = StringField("Role", validators=[InputRequired()])
    signoffs_required = IntegerField("Signoffs Required", validators=[InputRequired()])
    data_version = IntegerField("data_version", validators=[InputRequired()], widget=HiddenInput())
    change_type = SelectField("Change Type", choices=[("update", "update")])


class ScheduledChangeDeleteProductRequiredSignoffForm(ScheduledChangeTimeForm):
    product = StringField("Product", validators=[Length(0, 15), InputRequired()])
    channel = StringField("Channel", validators=[Length(0, 75), InputRequired()])
    role = StringField("Role", validators=[InputRequired()])
    data_version = IntegerField("data_version", validators=[InputRequired()], widget=HiddenInput())
    change_type = SelectField("Change Type", choices=[("delete", "delete")])


class EditScheduledChangeNewProductRequiredSignoffForm(ScheduledChangeTimeForm):
    product = StringField("Product", validators=[Length(0, 15), Optional()])
    channel = StringField("Channel", validators=[Length(0, 75), Optional()])
    role = StringField("Role", validators=[Optional()])
    signoffs_required = IntegerField("Signoffs Required", validators=[Optional()])
    sc_data_version = IntegerField("sc_data_version", validators=[InputRequired()], widget=HiddenInput())


class EditScheduledChangeExistingProductRequiredSignoffForm(ScheduledChangeTimeForm):
    signoffs_required = IntegerField("Signoffs Required", validators=[Optional()])
    data_version = IntegerField("data_version", widget=HiddenInput())
    sc_data_version = IntegerField("sc_data_version", validators=[InputRequired()], widget=HiddenInput())


class PermissionsRequiredSignoffForm(Form):
    product = StringField("Permissions", validators=[Length(0, 15), InputRequired()])
    role = StringField("Role", validators=[InputRequired()])
    signoffs_required = IntegerField("Signoffs Required", validators=[InputRequired()])


class PermissionsRequiredSignoffHistoryForm(Form):
    product = StringField("Product", validators=[Length(0, 15), InputRequired()])
    role = StringField("Role", validators=[InputRequired()])


class ScheduledChangeNewPermissionsRequiredSignoffForm(ScheduledChangeTimeForm):
    product = StringField("Permissions", validators=[Length(0, 15), InputRequired()])
    role = StringField("Role", validators=[InputRequired()])
    signoffs_required = IntegerField("Signoffs Required", validators=[InputRequired()])
    change_type = SelectField("Change Type", choices=[("insert", "insert")])


class ScheduledChangeExistingPermissionsRequiredSignoffForm(ScheduledChangeTimeForm):
    product = StringField("Permissions", validators=[Length(0, 15), InputRequired()])
    role = StringField("Role", validators=[InputRequired()])
    signoffs_required = IntegerField("Signoffs Required", validators=[InputRequired()])
    data_version = IntegerField("data_version", validators=[InputRequired()], widget=HiddenInput())
    change_type = SelectField("Change Type", choices=[("update", "update")])


class ScheduledChangeDeletePermissionsRequiredSignoffForm(ScheduledChangeTimeForm):
    product = StringField("Permissions", validators=[Length(0, 15), InputRequired()])
    role = StringField("Role", validators=[InputRequired()])
    data_version = IntegerField("data_version", validators=[InputRequired()], widget=HiddenInput())
    change_type = SelectField("Change Type", choices=[("delete", "delete")])


class EditScheduledChangeNewPermissionsRequiredSignoffForm(ScheduledChangeTimeForm):
    product = StringField("Permissions", validators=[Length(0, 15), Optional()])
    role = StringField("Role", validators=[Optional()])
    signoffs_required = IntegerField("Signoffs Required", validators=[Optional()])
    sc_data_version = IntegerField("sc_data_version", validators=[InputRequired()], widget=HiddenInput())


class EditScheduledChangeExistingPermissionsRequiredSignoffForm(ScheduledChangeTimeForm):
    signoffs_required = IntegerField("Signoffs Required", validators=[Optional()])
    data_version = IntegerField("data_version", widget=HiddenInput())
    sc_data_version = IntegerField("sc_data_version", validators=[InputRequired()], widget=HiddenInput())
