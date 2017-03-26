import flask
from connexion.decorators.validation import ParameterValidator


CONNEXION_IGNORE_VALIDATION_AVAST = ["avast", "force"]


class BalrogParameterValidator(ParameterValidator):
    def __init__(self, *args, **kwargs):
        super(BalrogParameterValidator, self).__init__(*args, **kwargs)

    def validate_path_parameter(self, args, param):
        val = args.get(param['name'].replace('-', '_'))

        if val is None and 'default' in param:
            val = param['default']
            args[param['name']] = val

        return self.validate_parameter('path', val, param)

    def validate_query_parameter(self, param):
        if param['name'] in CONNEXION_IGNORE_VALIDATION_AVAST:
            print "IGNORE", param['name']
            return
        val = flask.request.args.get(param['name'])
        return self.validate_parameter('query', val, param)
