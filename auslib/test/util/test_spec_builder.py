import unittest
import yaml
from os import path
from auslib.util.swagger import SpecBuilder


class TestSpecBuilder(unittest.TestCase):
    def setUp(self):
        current_path = path.dirname(__file__)
        self.resources_dir = path.join(current_path, "resources")

    def test_build_spec(self):
        main_spec = path.join(self.resources_dir, "api.yml")
        part_1 = path.join(self.resources_dir, "part_1.yml")
        part_2 = path.join(self.resources_dir, "part_2.yml")

        spec = SpecBuilder().add_spec(main_spec)\
                            .add_spec(part_1)\
                            .add_spec(part_2)

        self.assertIsNotNone(spec)
        result_file = file(path.join(self.resources_dir, "result.yml"), 'r')
        result = yaml.load(result_file)

        def check_dicts(l, r):
            for k, v in l.items():
                self.assertTrue(k in r, "%s not in %s" % (k, r))
                if isinstance(v, dict):
                    check_dicts(v, r[k])

        check_dicts(spec, result)
        check_dicts(result, spec)

    def test_build_spec_bad_spec_part(self):
        main_spec = path.join(self.resources_dir, "api.yml")
        part_1 = path.join(self.resources_dir, "part_1.yml")
        part_3 = path.join(self.resources_dir, "part_3.yml")
        with self.assertRaises(ValueError):
            SpecBuilder().add_spec(main_spec)\
                         .add_spec(part_1)\
                         .add_spec(part_3)
