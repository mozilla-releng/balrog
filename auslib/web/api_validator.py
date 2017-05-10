import logging
from connexion.decorators.validation import ParameterValidator

log = logging.getLogger(__name__)


class BalrogParameterValidator(ParameterValidator):
    """
    This class is used to keep the flask "defaults" feature behavior on spec validation level.
    """

    def __init__(self, *args, **kwargs):
        super(BalrogParameterValidator, self).__init__(*args, **kwargs)

    def validate_path_parameter(self, param, request):
        # Keep the base class behavior.
        val = request.path_params.get(param['name'].replace('-', '_'))

        # Supporting the flask add_url_rule "defaults" parameter to the swagger path parameter.
        if val is None and 'default' in param:
            val = param['default']
            request.path_params[param['name']] = val

        # We don't expect any unicode in the update URL, nor do we know which
        # encoding it would use if we get it, so we simply ignore any that is
        # given. All known cases of this are misconfiguration on the client end.
        # This will need to be changed if we ever have a case where a client is
        # validly sending unicode.
        if param['type'] == 'string':
            request.path_params[param['name']] = val.encode('ascii', 'ignore')

        return self.validate_parameter('path', val, param)
