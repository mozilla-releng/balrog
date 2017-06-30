import yaml
from collections import OrderedDict


class SpecBuilder(OrderedDict):
    def __init__(self, *args, **kwargs):
        OrderedDict.__init__(self, *args, **kwargs)
        self._paths_key = "paths"
        self._definitions_key = "definitions"
        self._parameters_key = "parameters"

    def _load_spec(self, file_name):
        with file(file_name, 'r') as spec_file:
            return yaml.load(spec_file)

    def _merge_part(self, key, part_dict):
        if part_dict:
            if key not in self:
                self[key] = {}
            self._merge_dict(self[key], part_dict)

    def _merge_dict(self, main_dict, part_dict):
        self._test_merge(main_dict, part_dict)
        main_dict.update(part_dict)

    def _test_merge(self, main_dict, part_dict):
        for k, v in part_dict.items():
            if k in main_dict:
                raise ValueError("Key {} already exists in spec file.".format(k))

    def _cut_part(self, spec, key):
        part = {}
        if key in spec:
            part = spec[key]
            del spec[key]
        return part

    def add_spec(self, file_name):
        spec = self._load_spec(file_name)
        paths = self._cut_part(spec, self._paths_key)
        definitions = self._cut_part(spec, self._definitions_key)
        parameters = self._cut_part(spec, self._parameters_key)

        self._merge_dict(self, spec)
        self._merge_part(self._paths_key, paths)
        self._merge_part(self._definitions_key, definitions)
        self._merge_part(self._parameters_key, parameters)

        return self
