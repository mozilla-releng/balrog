import simplejson as json
import sys

from flaskext.wtf import Form, TextField, HiddenField, Required, TextInput, NumberRange, IntegerField, SelectField, validators

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

class JSONTextField(TextField):
    """TextField that parses incoming data as JSON."""
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            log.debug("JSONTextField.process_formdata: valuelist[0] is: %s", valuelist[0])
            try:
                self.data = json.loads(valuelist[0])
            # XXX: use JSONDecodeError when the servers support it
            except ValueError, e:
                # WTForms catches ValueError, which JSONDecodeError is a child
                # of. Because of this, we need to wrap this error in something
                # else in order for it to be properly raised.
                log.debug('JSONTextField.process_formdata: Caught ValueError')
                raise Exception("Couldn't process JSONTextField %s, caught ValueError" % self.name)
        else:
            log.debug('JSONTextField: No value list, setting self.data to {}')
            self.data = {}

class NullableTextField(TextField):
    """TextField that parses incoming data converting empty strings to None's."""
    def process_formdata(self, valuelist):
        log.debug("NullableTextField.process_formdata: data %s", valuelist)
        if valuelist and valuelist[0]:
            if valuelist[0] == '':
                log.debug("NullableTextField.process_formdata: data is empty string, setting it to NULL", valuelist[0])
                self.data = None
            else:
                self.data = valuelist[0]
        else:
            log.debug('NullableTextField: No value list, setting self.data to None')
            self.data = None

class DbEditableForm(Form):
    data_version = HiddenField('data_version', validators=[Required(), NumberRange()])

class PermissionForm(DbEditableForm):
    options = JSONTextField('Options')

class NewPermissionForm(PermissionForm):
    permission = TextField('Permission', validators=[Required()])

class ExistingPermissionForm(PermissionForm):
    permission = TextField('Permission', validators=[Required()], widget=DisableableTextInput(disabled=True))

class RuleForm(Form):
    throttle = IntegerField('Throttle', validators=[Required(), validators.NumberRange(0, 100) ])
    priority = IntegerField('Priority', validators=[Required()])
    mapping = SelectField('Mapping', validators=[])
    product = NullableTextField('Product', validators=[validators.Length(0, 15)] ) 
    version = NullableTextField('Version', validators=[validators.Length(0,10) ])
    build_id = NullableTextField('BuildID', validators=[validators.Length(0,20) ])
    channel = NullableTextField('Channel', validators=[validators.Length(0,75) ]) 
    locale = NullableTextField('Locale', validators=[validators.Length(0,10) ])
    distribution = NullableTextField('Distrubution', validators=[validators.Length(0,100) ])
    build_target = NullableTextField('Build Target', validators=[validators.Length(0,75) ]) 
    os_version = NullableTextField('OS Version', validators=[validators.Length(0,100) ])
    dist_version = NullableTextField('Dist Version', validators=[validators.Length(0,100) ])
    comment = NullableTextField('Comment', validators=[validators.Length(0,500) ])
    update_type = SelectField('Update Type', choices=[('minor','minor'), ('major', 'major')], validators=[]) 
    header_arch = NullableTextField('Header Architecture', validators=[validators.Length(0,10) ])

class EditRuleForm(RuleForm, DbEditableForm):
    pass
