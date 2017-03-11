import connexion
from connexion.operation import Operation
from connexion.resolver import Resolver


RANDOM_DIGITS = 6


class BalrogApi(connexion.Api):
    def __init__(self, *args, **kwargs):
        super(BalrogApi, self).__init__(*args, **kwargs)

    def add_operation(self, method, path, swagger_operation, path_parameters):
        operation = Operation(method=method,
                              path=path,
                              path_parameters=path_parameters,
                              operation=swagger_operation,
                              app_produces=self.produces,
                              app_consumes=self.consumes,
                              app_security=self.security,
                              security_definitions=self.security_definitions,
                              definitions=self.definitions,
                              parameter_definitions=self.parameter_definitions,
                              response_definitions=self.response_definitions,
                              validate_responses=self.validate_responses,
                              validator_map=self.validator_map,
                              strict_validation=self.strict_validation,
                              resolver=self.resolver,
                              randomize_endpoint=RANDOM_DIGITS)
        self._add_operation_internal(method, path, operation)


class BalrogApp(connexion.App):
    def __init__(self, *args, **kwargs):
        super(BalrogApp, self).__init__(*args, **kwargs)

    def add_api(self, specification, base_path=None, arguments=None, auth_all_paths=None, swagger_json=None,
                swagger_ui=None, swagger_path=None, swagger_url=None, validate_responses=False,
                strict_validation=False, resolver=Resolver(), resolver_error=None):
        # References to this implementation: https://github.com/zalando/connexion/blob/master/connexion/app.py#L101
        self.resolver_error = resolver_error
        resolver_error_handler = None
        if self.resolver_error is not None:
            resolver_error_handler = self._resolver_error_handler

        resolver = Resolver(resolver) if hasattr(resolver, '__call__') else resolver

        swagger_json = swagger_json if swagger_json is not None else self.swagger_json
        swagger_ui = swagger_ui if swagger_ui is not None else self.swagger_ui
        swagger_path = swagger_path if swagger_path is not None else self.swagger_path
        swagger_url = swagger_url if swagger_url is not None else self.swagger_url
        auth_all_paths = auth_all_paths if auth_all_paths is not None else self.auth_all_paths
        # TODO test if base_url starts with an / (if not none)
        arguments = arguments or dict()
        arguments = dict(self.arguments, **arguments)  # copy global arguments and update with api specfic

        if isinstance(specification, dict):
            specification = specification
        else:
            specification = self.specification_dir / specification

        api = BalrogApi(specification=specification,
                        base_url=base_path, arguments=arguments,
                        swagger_json=swagger_json,
                        swagger_ui=swagger_ui,
                        swagger_path=swagger_path,
                        swagger_url=swagger_url,
                        resolver=resolver,
                        resolver_error_handler=resolver_error_handler,
                        validate_responses=validate_responses,
                        strict_validation=strict_validation,
                        auth_all_paths=auth_all_paths,
                        debug=self.debug,
                        validator_map=self.validator_map)
        self.app.register_blueprint(api.blueprint)
        return api
