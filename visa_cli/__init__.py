from .visa_status import Visa_Status
import pandas as pd
import argparse
import sys

pd.set_option("display.max_rows", None)


__version__ = "0.0.1"


def main(argv=None):
    argv = sys.argv if argv is None else argv
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "resident_country", type=str, help="Current Resident Country",
    )

    parser.add_argument(
        "-f",
        "--visa-free",
        help="Countries not requiring Visa",
        dest="visa_free",
        action="store_true",
    )

    parser.add_argument(
        "-r",
        "--visa-required",
        help="Countries requiring Visa",
        dest="visa_required",
        action="store_true",
    )

    parser.add_argument(
        "-o",
        "--visa-on-arrival",
        help="Countries offering Visa on arrival",
        dest="visa_voa",
        action="store_true",
    )

    parser.add_argument(
        "-e",
        "--eta",
        help="Countries offering Electronic Travel Authority",
        dest="visa_eta",
        action="store_true",
    )

    parser.add_argument(
        "-n",
        "--visa-free-days",
        help="Countries offering Visa free days",
        dest="visa_free_days",
        action="store_true",
    )

    parser.add_argument(
        "-c",
        "--covid-ban",
        help="Countries not offering Visa due to Covid-19",
        dest="visa_covid_ban",
        action="store_true",
    )

    parser.add_argument(
        "-i",
        "--interactive",
        help="Interactive Prompt",
        dest="interactive_prompt",
        action="store_true",
    )
    args = parser.parse_args()

    # https://raw.githubusercontent.com/ilyankou/passport-index-dataset/master/passport-index-matrix.csv
    current_residency = Visa_Status(
        "https://raw.githubusercontent.com/ilyankou/passport-index-dataset/master/passport-index-matrix.csv",
        args.resident_country,
    )

    if args.visa_free:
        print(current_residency.get_status_vf())

    if args.visa_required:
        print(current_residency.get_status_vr())

    if args.visa_voa:
        print(current_residency.get_status_voa())

    if args.visa_eta:
        print(current_residency.get_status_eta())

    if args.visa_free_days:
        print(current_residency.get_status_vfe())

    if args.visa_covid_ban:
        print(current_residency.get_covid_ban())

    if args.interactive_prompt:
        current_residency.interactive_prompt()
