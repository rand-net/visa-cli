from .visa_status import *
from tabulate import tabulate
import pandas as pd
import argparse
import sys

pd.set_option("display.max_rows", None)


__version__ = "0.2.0"


def tabprint(print_df):
    print(tabulate(print_df, headers="keys", tablefmt="fancy_grid", showindex=True))


def main(argv=None):
    argv = sys.argv if argv is None else argv
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "resident_country",
        type=str,
        help="Current Resident Country",
    )

    parser.add_argument(
        "-d",
        "--destination-country",
        help="Destination Country",
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

    parser.add_argument(
        "-l",
        "--resident-countries",
        help='A list of resident Countries in addition to the current resident Country. \n Format argument in a comma-delimited string "Israel, Russia, China"',
    )
    args = parser.parse_args()

    vstat = VisaStatus(
        args.resident_country.title(), args.resident_countries, args.destination_country
    )
    vstat.get_visa_data()

    all_arguments = [
        args.resident_countries,
        args.visa_required,
        args.visa_free,
        args.visa_voa,
        args.visa_eta,
        args.visa_free_days,
        args.visa_covid_ban,
        args.interactive_prompt,
        args.destination_country,
    ]

    # Print status for all destination Countries
    if args.resident_country and not any(all_arguments):
        vstat.get_status_all_dest_countries()
        tabprint(vstat.get_all_countries())

    # Print status for only the given destination Country
    if (
        args.destination_country
        and args.resident_country
        and not args.resident_countries
    ):
        tabprint(vstat.get_status_given_dest_country())

    if not args.resident_countries and args.resident_country and args.visa_free:
        vstat.get_status_all_dest_countries()
        print(
            "\nCountries offering Visa-Free travel for residents of {}\n".format(
                args.resident_country
            )
        )
        tabprint(vstat.get_vf_countries())

    if not args.resident_countries and args.resident_country and args.visa_required:
        vstat.get_status_all_dest_countries()
        print(
            "\nCountries requiring Visa for residents of {}\n".format(
                args.resident_country
            )
        )
        tabprint(vstat.get_vr_countries())

    if not args.resident_countries and args.resident_country and args.visa_voa:
        vstat.get_status_all_dest_countries()
        print(
            "\nCountries offering Visa on Arrival(VOA) for residents of {}\n".format(
                args.resident_country
            )
        )
        tabprint(vstat.get_voa_countries())

    if not args.resident_countries and args.resident_country and args.visa_eta:
        vstat.get_status_all_dest_countries()
        print(
            "\nCountries offering Electronic Travel Authority(ETA) for residents of {}\n".format(
                args.resident_country
            )
        )
        tabprint(vstat.get_eta_countries())

    if not args.resident_countries and args.resident_country and args.visa_free_days:
        vstat.get_status_all_dest_countries()
        print(
            "\nCountries offering Visa free days for residents of {}\n".format(
                args.resident_country
            )
        )
        tabprint(vstat.get_vfe_countries())

    if not args.resident_countries and args.resident_country and args.visa_covid_ban:
        vstat.get_status_all_dest_countries()
        print(
            "\nCountries banning travel due to Covid-19 for residents of {}\n".format(
                args.resident_country
            )
        )
        tabprint(vstat.get_covid_ban_countries())

    if (
        not args.resident_countries
        and args.resident_country
        and args.interactive_prompt
    ):
        vstat.get_status_all_dest_countries()
        vstat.launch_interactive_prompt()

    if args.resident_country and args.resident_countries and args.destination_country:
        tabprint(vstat.get_status_multi_resident_countries())
