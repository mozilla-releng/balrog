import yaml
import auslib

from os import path

AUS_DIR = path.dirname(auslib.__file__)


class SpecBuilder():
    def __init__(self, app, endpoints_key="paths", definitions_key="definitions"):
        self._app = app
        self.endpoints_key = endpoints_key
        self.definitions_key = definitions_key
        self._main_spec = {}
        self._spec_parts = []

    def _get_dict(self, spec, key):
        for k, v in spec.items():
            if k == key:
                return v
            elif isinstance(v, dict):
                self._get_dict(v, key)
        return None

    def _load_spec(self, file_name):
        with file(file_name, 'r') as spec_file:
            return yaml.load(spec_file)

    def add_main_spec(self, file_name):
        app_dir = self._app.root_path
        file_name = path.join(app_dir, file_name)
        self._main_spec = self._load_spec(file_name)
        return self

    def add_spec_part(self, file_name):
        file_name = path.join(AUS_DIR, file_name)
        self._spec_parts.append(self._load_spec(file_name))
        return self

    def build(self):
        main_endpoints = self._get_dict(self._main_spec, self.endpoints_key)
        main_definitions = self._get_dict(self._main_spec, self.definitions_key)
        for spec_part in self._spec_parts:
            if self.endpoints_key in spec_part:
                part_endpoints = spec_part[self.endpoints_key]
                main_endpoints.update(part_endpoints)

            if self.definitions_key in spec_part:
                if not main_definitions:
                    self._main_spec[self.definitions_key] = {}
                    main_definitions = self._main_spec[self.definitions_key]
                part_definitions = spec_part[self.definitions_key]
                main_definitions.update(part_definitions)

        return self._main_spec
