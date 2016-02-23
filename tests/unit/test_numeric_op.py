import unittest
import yaml
from jnpr.jsnapy.check import Comparator
from mock import patch


class TestNumericOperators(unittest.TestCase):

    def setUp(self):

        self.diff = False
        self.hostname = "10.216.193.114"
        self.db = dict()
        self.db['store_in_sqlite'] = False
        self.db['check_from_sqlite'] = False
        self.db['db_name'] = ""
        self.snap_del = False
        self.action = None

    def test_in_range(self):
        self.chk = False
        comp = Comparator()
        conf_file = "configs/main_in-range.yml"
        config_file = open(conf_file, 'r')
        main_file = yaml.load(config_file)

        oper = comp.generate_test_files(
            main_file,
            self.hostname,
            self.chk,
            self.diff,
            self.db,
            self.snap_del,
            "snap_in-range_pre")
        self.assertEqual(oper.no_passed, 1)
        self.assertEqual(oper.no_failed, 0)

    def test_in_range_fail(self):
        self.chk = False
        comp = Comparator()
        conf_file = "configs/main_in-range.yml"
        config_file = open(conf_file, 'r')
        main_file = yaml.load(config_file)

        oper = comp.generate_test_files(
            main_file,
            self.hostname,
            self.chk,
            self.diff,
            self.db,
            self.snap_del,
            "snap_in-range_fail_pre")

        self.assertEqual(oper.no_passed, 0)
        self.assertEqual(oper.no_failed, 1)

    def test_not_range_fail(self):
        self.chk = False
        comp = Comparator()
        conf_file = "configs/main_not-range.yml"
        config_file = open(conf_file, 'r')
        main_file = yaml.load(config_file)

        oper = comp.generate_test_files(
            main_file,
            self.hostname,
            self.chk,
            self.diff,
            self.db,
            self.snap_del,
            "snap_not-range_pre")

        self.assertEqual(oper.no_passed, 0)
        self.assertEqual(oper.no_failed, 1)

    def test_not_range_pass(self):
        self.chk = False
        comp = Comparator()
        conf_file = "configs/main_not-range.yml"
        config_file = open(conf_file, 'r')
        main_file = yaml.load(config_file)

        oper = comp.generate_test_files(
            main_file,
            self.hostname,
            self.chk,
            self.diff,
            self.db,
            self.snap_del,
            "snap_in-range_fail_pre")

        self.assertEqual(oper.no_passed, 1)
        self.assertEqual(oper.no_failed, 0)

    def test_is_lt(self):
        self.chk = False
        comp = Comparator()
        conf_file = "configs/main_is-lt.yml"
        config_file = open(conf_file, 'r')
        main_file = yaml.load(config_file)

        oper = comp.generate_test_files(
            main_file,
            self.hostname,
            self.chk,
            self.diff,
            self.db,
            self.snap_del,
            "snap_is-lt_pre")

        self.assertEqual(oper.no_passed, 0)
        self.assertEqual(oper.no_failed, 1)

    def test_is_lt_pass(self):
        self.chk = False
        comp = Comparator()
        conf_file = "configs/main_is-lt.yml"
        config_file = open(conf_file, 'r')
        main_file = yaml.load(config_file)

        oper = comp.generate_test_files(
            main_file,
            self.hostname,
            self.chk,
            self.diff,
            self.db,
            self.snap_del,
            "snap_is-lt_fail_pre")

        self.assertEqual(oper.no_passed, 1)
        self.assertEqual(oper.no_failed, 0)

    def test_is_gt(self):
        self.chk = False
        comp = Comparator()
        conf_file = "configs/main_is-gt.yml"
        config_file = open(conf_file, 'r')
        main_file = yaml.load(config_file)

        oper = comp.generate_test_files(
            main_file,
            self.hostname,
            self.chk,
            self.diff,
            self.db,
            self.snap_del,
            "snap_is-gt_pre")

        self.assertEqual(oper.no_passed, 1)
        self.assertEqual(oper.no_failed, 0)

    def test_is_gt_fail(self):
        self.chk = False
        comp = Comparator()
        conf_file = "configs/main_is-gt.yml"
        config_file = open(conf_file, 'r')
        main_file = yaml.load(config_file)

        oper = comp.generate_test_files(
            main_file,
            self.hostname,
            self.chk,
            self.diff,
            self.db,
            self.snap_del,
            "snap_is-gt_fail_pre")

        self.assertEqual(oper.no_passed, 0)
        self.assertEqual(oper.no_failed, 1)

with patch('logging.Logger') as mock_logger:
    if __name__ == "__main__":
        suite = unittest.TestLoader().loadTestsFromTestCase(
            TestNumericOperators)
        unittest.TextTestRunner(verbosity=2).run(suite)
