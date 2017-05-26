import unittest
import yaml
from os import path
from auslib.util.swagger import SpecBuilder


class TestSpecBuilder(unittest.TestCase):
    def setUp(self):
        self.resources_dir = path.join(path.dirname(__file__), "resources")

    def testBuildSpec(self):
        main_spec = path.join(self.resources_dir, "api.yml")
        part_1 = path.join(self.resources_dir, "part_1.yml")
        part_2 = path.join(self.resources_dir, "part_2.yml")

        spec = SpecBuilder().add_main_spec(main_spec)\
                            .add_spec_part(part_1)\
                            .add_spec_part(part_2)\
                            .build()
        self.assertIsNotNone(spec)
        result_file = file(path.join(self.resources_dir, "result.yml"))
        result = yaml.load(result_file)

        def check_dicts(l, r):
            for k, v in l.items():
                self.assertTrue(k in r, "%s not in %s" % (k, r))
                if isinstance(v, dict):
                    check_dicts(v, r[k])

        check_dicts(spec, result)
        check_dicts(result, spec)
