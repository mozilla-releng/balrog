import auslib.web
from os import path
from auslib.util.swagger import SpecBuilder


current_dir = path.dirname(__file__)
web_dir = path.dirname(auslib.web.__file__)


def _join_current_path(f):
    return path.join(current_dir, f)


def _join_web_path(f):
    return path.join(web_dir, f)


def get_spec():
    spec = SpecBuilder().add_spec(_join_current_path('api.yml'))

    spec.add_spec(_join_web_path('common/swagger/common_definitions.yml'))\
        .add_spec(_join_web_path('common/swagger/common_responses.yml'))\
        .add_spec(_join_web_path('common/swagger/common_parameters.yml'))

    spec.add_spec(_join_current_path('releases_spec.yml'))\
        .add_spec(_join_web_path('common/swagger/releases_parameters.yml'))\
        .add_spec(_join_web_path('common/swagger/releases_definitions.yml'))\
        .add_spec(_join_web_path('common/swagger/releases_responses.yml'))

    spec.add_spec(_join_current_path('rules_spec.yml'))\
        .add_spec(_join_web_path('common/swagger/rules_parameters.yml'))\
        .add_spec(_join_web_path('common/swagger/rules_definitions.yml'))\
        .add_spec(_join_web_path('common/swagger/rules_responses.yml'))

    return spec
