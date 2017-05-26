import yaml


class SpecBuilder():
    def __init__(self, endpoints_key="paths", definitions_key="definitions"):
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

    def _read_yaml(self, file_name):
        content = ""
        with open(file_name, 'r') as f:
            content = f.read()
        return content

    def add_main_spec(self, file_name):
        stream = file(file_name, 'r')
        self._main_spec = yaml.load(stream)
        return self

    def add_spec_part(self, file_name):
        stream = file(file_name, 'r')
        self._spec_parts.append(yaml.load(stream))
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
