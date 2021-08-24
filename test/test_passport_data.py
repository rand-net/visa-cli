import pandas as pd
import unittest
import sys

sys.path.append("../visa_cli/")
from visa_cli.passport_data.passport_data import *


class TestPassportData(unittest.TestCase):
    def test_get_country_codes_iso2(self):
        print("test_get_country_codes_iso2")
        passdata = PassportData()
        passdata.get_country_codes_iso2()
        self.assertIsNotNone(passdata.country_codes)
        columns = passdata.country_codes.shape[1]
        rows = passdata.country_codes.shape[0]
        self.assertGreaterEqual(columns, 2)
        self.assertGreaterEqual(rows, 195)

    def test_get_passport_data(self):
        print("test_get_passport_data")
        passdata = PassportData()
        passdata.get_country_codes_iso2()
        passdata.get_passport_data()
        self.assertIsNotNone(passdata.passport_data)
        records = len(passdata.passport_data)
        self.assertGreaterEqual(records, 195)

    def test_clean_passport_data(self):
        print("test_clean_passport_data")
        passdata = PassportData()
        passdata.get_country_codes_iso2()
        passdata.get_passport_data()
        passdata.clean_passport_data()
        self.assertIsNotNone(passdata.passport_data)
        records = len(passdata.passport_data_cleaned)
        self.assertGreaterEqual(records, 195)

    def test_get_passport_data_country_names_matrix(self):
        print("test_get_passport_data_country_names_matrix")
        passdata = PassportData()
        passdata.get_country_codes_iso2()
        passdata.get_passport_data()
        passdata.clean_passport_data()
        self.assertIsNotNone(passdata.get_passport_data_country_names_matrix())
        columns = passdata.get_passport_data_country_names_matrix().shape[1]
        rows = passdata.get_passport_data_country_names_matrix().shape[0]
        self.assertGreaterEqual(columns, 195)
        self.assertGreaterEqual(rows, 195)


if __name__ == "__main__":
    unittest.main()
