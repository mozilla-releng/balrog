import codecs
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

        # Encode strings in utf-8.
        if param['type'] == 'string':
            val = codecs.encode(val, 'utf-8')
            request.path_params[param['name']] = val

        return self.validate_parameter('path', val, param)
