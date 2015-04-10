import simplejson as json

from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField
from wtforms.widgets import TextInput, FileInput, HiddenInput
from wtforms.validators import Required, Optional, NumberRange, Length

import logging
log = logging.getLogger(__name__)

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
            except ValueError, e:
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

class DbEditableForm(Form):
    data_version = IntegerField('data_version', validators=[Required()], widget=HiddenInput())

class PermissionForm(DbEditableForm):
    options = JSONStringField('Options')

class NewPermissionForm(PermissionForm):
    permission = StringField('Permission', validators=[Required()])

class ExistingPermissionForm(PermissionForm):
    permission = StringField('Permission', validators=[Required()], widget=DisableableTextInput(disabled=True))

class ReleaseForm(Form):
    # Because we do implicit release creation in the Releases views, we can't
    # have data_version be Required(). The views are responsible for checking
    # for its existence in this case.
    data_version = IntegerField('data_version', widget=HiddenInput())
    product = StringField('Product', validators=[Required()])
    version = StringField('Version', validators=[Required()])
    hashFunction = StringField('Hash Function')
    data = JSONStringField('Data', validators=[Required()])
    schema_version = IntegerField('Schema Version')
    copyTo = JSONStringField('Copy To', default=list)
    alias = JSONStringField('Alias', default=list)

class RuleForm(Form):
    backgroundRate = IntegerField('Background Rate', validators=[Required(), NumberRange(0, 100) ])
    priority = IntegerField('Priority', validators=[Required()])
    mapping = SelectField('Mapping', validators=[])
    product = NullableStringField('Product', validators=[Length(0, 15)] )
    version = NullableStringField('Version', validators=[Length(0,10) ])
    buildID = NullableStringField('BuildID', validators=[Length(0,20) ])
    channel = NullableStringField('Channel', validators=[Length(0,75) ])
    locale = NullableStringField('Locale', validators=[Length(0,200) ])
    distribution = NullableStringField('Distribution', validators=[Length(0,100) ])
    buildTarget = NullableStringField('Build Target', validators=[Length(0,75) ])
    osVersion = NullableStringField('OS Version', validators=[Length(0,1000) ])
    distVersion = NullableStringField('Dist Version', validators=[Length(0,100) ])
    comment = NullableStringField('Comment', validators=[Length(0,500) ])
    update_type = SelectField('Update Type', choices=[('minor','minor'), ('major', 'major')], validators=[])
    headerArchitecture = NullableStringField('Header Architecture', validators=[Length(0,10) ])

class EditRuleForm(DbEditableForm):
    backgroundRate = IntegerField('Background Rate', validators=[Optional(), NumberRange(0, 100) ])
    priority = IntegerField('Priority', validators=[Optional()])
    mapping = SelectField('Mapping', validators=[Optional()], coerce=NoneOrType(unicode))
    product = NullableStringField('Product', validators=[Optional(), Length(0, 15)] )
    version = NullableStringField('Version', validators=[Optional(), Length(0,10) ])
    buildID = NullableStringField('BuildID', validators=[Optional(), Length(0,20) ])
    channel = NullableStringField('Channel', validators=[Optional(), Length(0,75) ])
    locale = NullableStringField('Locale', validators=[Optional(), Length(0,200) ])
    distribution = NullableStringField('Distribution', validators=[Optional(), Length(0,100) ])
    buildTarget = NullableStringField('Build Target', validators=[Optional(), Length(0,75) ])
    osVersion = NullableStringField('OS Version', validators=[Optional(), Length(0,1000) ])
    distVersion = NullableStringField('Dist Version', validators=[Optional(), Length(0,100) ])
    comment = NullableStringField('Comment', validators=[Optional(), Length(0,500) ])
    update_type = SelectField('Update Type', choices=[('minor','minor'), ('major', 'major')], validators=[Optional()], coerce=NoneOrType(unicode))
    headerArchitecture = NullableStringField('Header Architecture', validators=[Optional(), Length(0,10) ])

class NewReleaseForm(Form):
    name = StringField('Name', validators=[Required()])
    version = StringField('Version', validators=[Required()])
    product = StringField('Product', validators=[Required()])
    blob = JSONStringField('Data', validators=[Required()], widget=FileInput())
