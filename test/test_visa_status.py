import pandas as pd
import unittest
import sys

sys.path.append("../visa_cli/")
from visa_cli.visa_status import *


class TestVisaStatus(unittest.TestCase):
    def test_get_visa_data(self):
        print("test_get_visa_data")
        vstatus = VisaStatus("Russia", None, "Germany")
        vstatus.get_visa_data()
        self.assertIsNotNone(vstatus.visa_data_raw)
        columns = vstatus.visa_data_raw.shape[1]
        rows = vstatus.visa_data_raw.shape[0]
        self.assertGreaterEqual(columns, 195)
        self.assertGreaterEqual(rows, 195)

    def test_get_status_all_dest_countries(self):
        print("test_get_status_all_dest_countries")
        vstatus = VisaStatus("Russia", None, "Germany")
        vstatus.get_visa_data()
        vstatus.get_status_all_dest_countries()
        self.assertIsNotNone(vstatus.visa_data_raw)
        rows = vstatus.visa_status_all_countries.shape[0]
        self.assertGreaterEqual(rows, 195)

    def test_get_status_given_dest_country(self):
        print("test_get_status_given_dest_country")
        vstatus = VisaStatus("Russia", None, "Germany")
        vstatus.get_visa_data()
        self.assertIsNotNone(vstatus.visa_data_raw)
        self.assertTupleEqual(vstatus.get_status_given_dest_country().shape, (1, 2))

    def test_get_status_multi_resident_countries(self):
        print("test_get_status_multi_resident_countries")
        vstatus = VisaStatus("Russia", "Nepal, Albania, Algeria", "Germany")
        vstatus.get_visa_data()
        self.assertIsNotNone(vstatus.visa_data_raw)
        self.assertTupleEqual(
            vstatus.get_status_multi_resident_countries().shape, (4, 3)
        )


if __name__ == "__main__":
    unittest.main()
