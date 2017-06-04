import unittest
import yaml
from os import path
from auslib.util.swagger import SpecBuilder
from flask import Flask

app = Flask(__name__)


class TestSpecBuilder(unittest.TestCase):
    def setUp(self):
        self.resources_dir = "test/util/resources"

    def test_build_spec(self):
        main_spec = path.join(app.root_path, "resources/api.yml")
        part_1 = path.join(self.resources_dir, "part_1.yml")
        part_2 = path.join(self.resources_dir, "part_2.yml")

        spec = SpecBuilder(app).add_main_spec(main_spec)\
                               .add_spec_part(part_1)\
                               .add_spec_part(part_2)\
                               .build()
        self.assertIsNotNone(spec)
        result_file = file(path.join(app.root_path, "resources/result.yml"), 'r')
        result = yaml.load(result_file)

        def check_dicts(l, r):
            for k, v in l.items():
                self.assertTrue(k in r, "%s not in %s" % (k, r))
                if isinstance(v, dict):
                    check_dicts(v, r[k])

        check_dicts(spec, result)
        check_dicts(result, spec)

    def test_build_spec_bad_spec_part(self):
        main_spec = path.join(app.root_path, "resources/api.yml")
        part_1 = path.join(self.resources_dir, "part_1.yml")
        part_3 = path.join(self.resources_dir, "part_3.yml")
        with self.assertRaises(ValueError):
            SpecBuilder(app).add_main_spec(main_spec)\
                            .add_spec_part(part_1)\
                            .add_spec_part(part_3)\
                            .build()

    def test_build_spec_Key_conflict(self):
        main_spec = path.join(app.root_path, "resources/api.yml")
        part_1 = path.join(self.resources_dir, "part_1.yml")
        with self.assertRaises(AssertionError):
            SpecBuilder(app).add_main_spec(main_spec)\
                            .add_spec_part(part_1)\
                            .add_spec_part(part_1)\
                            .build()
