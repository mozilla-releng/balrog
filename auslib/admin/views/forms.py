import simplejson as json

from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField, BooleanField
from wtforms.widgets import TextInput, FileInput, HiddenInput
from wtforms.validators import Required, Optional, NumberRange, Length, Regexp, ValidationError
from auslib.util.comparison import get_op
from auslib.util.versions import MozillaVersion

import logging
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
            kwargs['disabled'] = 'disabled'
        return TextInput.__call__(self, *args, **kwargs)


class JSONStringField(StringField):
    """StringField that parses incoming data as JSON."""

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            try:
                self.data = json.loads(valuelist[0])
            # XXX: use JSONDecodeError when the servers support it
            except ValueError as e:
                # WTForms catches ValueError, which JSONDecodeError is a child
                # of. Because of this, we need to wrap this error in something
                # else in order for it to be properly raised.
                log.debug('Caught ValueError')
                self.process_errors.append(e.args[0])
        else:
            log.debug('No value list, setting self.data to default')
            self._set_default()

    def _set_default(self):
        self.data = {}

    def _value(self):
        return json.dumps(self.data) if self.data is not None else u''


class NullableStringField(StringField):
    """StringField that parses incoming data converting empty strings to None's."""

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            if valuelist[0] == '':
                log.debug("data is empty string, setting it to NULL")
                self.data = None
            else:
                self.data = valuelist[0]
        else:
            log.debug('No value list, setting self.data to None')
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
    log.debug('starting in operator_validator for buildID')

    def _validator(form, field):
        log.debug('starting in operator_validator: field.data is %s' % field.data)
        # empty input is fine
        if field.data is None:
            return
        try:
            op, operand = get_op(field.data)
            log.debug('Got (%s, %s) from get_op', op, operand)
        except TypeError:
            # get_op field returns None if no operator or no match, can't be unpacked
            raise ValidationError("Invalid input for %s. No Operator or Match found." % field.name)
    return _validator


def version_validator():
    log.debug('starting in version_validator for version')

    def _validator(form, field):
        log.debug('starting in version_validator: field.data is %s' % field.data)
        # empty input
        if field.data is None:
            return
        try:
            op, operand = get_op(field.data)
            version = MozillaVersion(operand)
        except ValueError:
            raise ValidationError("ValueError. Couldn't parse version for %s. Invalid '%s' input value" % (field.name, field.name))
        except:
            raise ValidationError('Invalid input for %s . No Operator or Match found.' % field.name)
        # MozillaVersion doesn't error on empty strings
        if not hasattr(version, 'version'):
            raise ValidationError("Couldn't parse the version for %s. No attribute 'version' was detected." % field.name)

    return _validator


class DbEditableForm(Form):
    data_version = IntegerField('data_version', validators=[Required()], widget=HiddenInput())


class ScheduledChangeForm(Form):
    telemetry_product = NullableStringField("Telemetry Product")
    telemetry_channel = NullableStringField("Telemetry Channel")
    telemetry_uptake = NullableStringField("Telemetry Uptake")
    when = IntegerField("When")


class NewPermissionForm(Form):
    options = JSONStringField('Options')


class ExistingPermissionForm(DbEditableForm):
    options = JSONStringField('Options')


class PartialReleaseForm(Form):
    # Because we do implicit release creation in the Releases views, we can't
    # have data_version be Required(). The views are responsible for checking
    # for its existence in this case.
    data_version = IntegerField('data_version', widget=HiddenInput())
    product = StringField('Product', validators=[Required()])
    hashFunction = StringField('Hash Function')
    data = JSONStringField('Data', validators=[Required()])
    schema_version = IntegerField('Schema Version')
    copyTo = JSONStringField('Copy To', default=list)
    alias = JSONStringField('Alias', default=list)


class RuleForm(Form):
    backgroundRate = IntegerField('Background Rate', validators=[Required(), NumberRange(0, 100)])
    priority = IntegerField('Priority', validators=[Required()])
    mapping = SelectField('Mapping', validators=[])
    alias = NullableStringField('Alias', validators=[Length(0, 50), Regexp(RULE_ALIAS_REGEXP)])
    product = NullableStringField('Product', validators=[Length(0, 15)])
    version = NullableStringField('Version', validators=[Length(0, 10), version_validator()])
    buildID = NullableStringField('BuildID', validators=[Length(0, 20), operator_validator()])
    channel = NullableStringField('Channel', validators=[Length(0, 75)])
    locale = NullableStringField('Locale', validators=[Length(0, 200)])
    distribution = NullableStringField('Distribution', validators=[Length(0, 100)])
    buildTarget = NullableStringField('Build Target', validators=[Length(0, 75)])
    osVersion = NullableStringField('OS Version', validators=[Length(0, 1000)])
    distVersion = NullableStringField('Dist Version', validators=[Length(0, 100)])
    whitelist = NullableStringField('Whitelist', validators=[Length(0, 100)])
    comment = NullableStringField('Comment', validators=[Length(0, 500)])
    update_type = SelectField('Update Type', choices=[('minor', 'minor'), ('major', 'major')], validators=[])
    headerArchitecture = NullableStringField('Header Architecture', validators=[Length(0, 10)])


class EditRuleForm(DbEditableForm):
    backgroundRate = IntegerField('Background Rate', validators=[Optional(), NumberRange(0, 100)])
    priority = IntegerField('Priority', validators=[Optional()])
    mapping = SelectField('Mapping', validators=[Optional()], coerce=NoneOrType(unicode))
    alias = NullableStringField('Alias', validators=[Optional(), Length(0, 50), Regexp(RULE_ALIAS_REGEXP)])
    product = NullableStringField('Product', validators=[Optional(), Length(0, 15)])
    version = NullableStringField('Version', validators=[Optional(), Length(0, 10), version_validator()])
    buildID = NullableStringField('BuildID', validators=[Optional(), Length(0, 20), operator_validator()])
    channel = NullableStringField('Channel', validators=[Optional(), Length(0, 75)])
    locale = NullableStringField('Locale', validators=[Optional(), Length(0, 200)])
    distribution = NullableStringField('Distribution', validators=[Optional(), Length(0, 100)])
    buildTarget = NullableStringField('Build Target', validators=[Optional(), Length(0, 75)])
    osVersion = NullableStringField('OS Version', validators=[Optional(), Length(0, 1000)])
    distVersion = NullableStringField('Dist Version', validators=[Optional(), Length(0, 100)])
    whitelist = NullableStringField('Whitelist', validators=[Optional(), Length(0, 100)])
    comment = NullableStringField('Comment', validators=[Optional(), Length(0, 500)])
    update_type = SelectField('Update Type', choices=[('minor', 'minor'), ('major', 'major')], validators=[Optional()], coerce=NoneOrType(unicode))
    headerArchitecture = NullableStringField('Header Architecture', validators=[Optional(), Length(0, 10)])


class ScheduledChangeNewRuleForm(ScheduledChangeForm, RuleForm):
    pass


class ScheduledChangeExistingRuleForm(ScheduledChangeForm, EditRuleForm):
    rule_id = IntegerField('Rule ID', validators=[Required()])


class EditScheduledChangeNewRuleForm(ScheduledChangeNewRuleForm):
    sc_data_version = IntegerField('sc_data_version', validators=[Required()], widget=HiddenInput())


class EditScheduledChangeExistingRuleForm(ScheduledChangeForm, EditRuleForm):
    sc_data_version = IntegerField('sc_data_version', validators=[Required()], widget=HiddenInput())


class CompleteReleaseForm(Form):
    name = StringField('Name', validators=[Required()])
    product = StringField('Product', validators=[Required()])
    blob = JSONStringField('Data', validators=[Required()], widget=FileInput())
    data_version = IntegerField('data_version', widget=HiddenInput())


class ReadOnlyForm(Form):
    name = StringField('Name', validators=[Required()])
    read_only = BooleanField('read_only')
    data_version = IntegerField('data_version', widget=HiddenInput())
