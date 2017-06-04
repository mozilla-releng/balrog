import yaml
import auslib

from os import path

AUS_DIR = path.dirname(auslib.__file__)


class SpecBuilder():
    def __init__(self,
                 app,
                 endpoints_key="paths",
                 definitions_key="definitions",
                 parameters_key="parameters",
                 version_file="version.txt"):
        self._app = app
        self.endpoints_key = endpoints_key
        self.definitions_key = definitions_key
        self.parameters_key = parameters_key
        self._main_spec = {}
        self._spec_parts = []
        self._version_file = version_file

    def _get_version(self):
        version = ''
        root_path = path.dirname(AUS_DIR)
        version_file = path.join(root_path, self._version_file)
        if path.exists(version_file):
            with open(version_file, 'r') as f:
                version = f.read()
        return version

    def _get_dict(self, spec, key):
        for k, v in spec.items():
            if k == key:
                return v
            elif isinstance(v, dict):
                self._get_dict(v, key)
        return {}

    def _load_spec(self, file_name):
        with file(file_name, 'r') as spec_file:
            return yaml.load(spec_file)

    def _try_change_version(self, info_dict):
        version_key = 'version'
        if info_dict and version_key in info_dict:
            version = self._get_version()
            if version:
                info_dict[version_key] = version

    def add_main_spec(self, file_name):
        """
        Adds the current application specification file.

        @param file_name: File relative to app path.
        @type: string
        """
        app_dir = self._app.root_path
        file_name = path.join(app_dir, file_name)
        self._main_spec = self._load_spec(file_name)
        return self

    def add_spec_part(self, file_name):
        """
        Adds a part of specification containing either paths, definitions, parameters or both.

        @param file_name: File relative to auslib module to facilitate the reusing of spec files from other places.
        @type: string
        """
        file_name = path.join(AUS_DIR, file_name)
        spec_part = self._load_spec(file_name)

        if (self.definitions_key not in spec_part and
                self.endpoints_key not in spec_part and
                self.parameters_key not in spec_part):
            raise ValueError("Mergeable swagger keys was not found in: {}".format(file_name))

        self._spec_parts.append(spec_part)
        return self

    def _test_merge(self, main_dict, part_dict):
        for k, v in part_dict.items():
            assert k not in main_dict, "Key {} already exists in spec file.".format(k)

    def _update_endpoints(self, main_endpoints, spec_part):
        if self.endpoints_key in spec_part:
            if not main_endpoints:
                self._main_spec[self.endpoints_key] = main_endpoints
            part_endpoints = spec_part[self.endpoints_key]
            self._test_merge(main_endpoints, part_endpoints)
            main_endpoints.update(part_endpoints)

    def _update_definitions(self, main_definitions, spec_part):
        if self.definitions_key in spec_part:
            if not main_definitions:
                self._main_spec[self.definitions_key] = main_definitions
            part_definitions = spec_part[self.definitions_key]
            self._test_merge(main_definitions, part_definitions)
            main_definitions.update(part_definitions)

    def _update_parameters_definitions(self, main_parameters, spec_part):
        if self.parameters_key in spec_part:
            if not main_parameters:
                self._main_spec[self.parameters_key] = main_parameters
            part_parameters = spec_part[self.parameters_key]
            self._test_merge(main_parameters, part_parameters)
            main_parameters.update(part_parameters)

    def build(self):
        self._try_change_version(self._get_dict(self._main_spec, 'info'))
        main_endpoints = self._get_dict(self._main_spec, self.endpoints_key)
        main_definitions = self._get_dict(self._main_spec, self.definitions_key)
        main_parameters = self._get_dict(self._main_spec, self.parameters_key)
        for spec_part in self._spec_parts:
            self._update_endpoints(main_endpoints, spec_part)
            self._update_definitions(main_definitions, spec_part)
            self._update_parameters_definitions(main_parameters, spec_part)
        return self._main_spec
