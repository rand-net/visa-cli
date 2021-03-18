from art import *
import pandas as pd
import requests
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from sys import exit
from tabulate import tabulate


def get_sel_country_status(passport_df, res_country, dest_country):

    sel_country_data_df = passport_df[
        passport_df["Passport"] == res_country
    ].transpose()  # Select
    sel_country_data_df = sel_country_data_df.iloc[1:]  # Delete first two rows

    # Reset the index and rename the column names
    sel_country_data_df = sel_country_data_df.reset_index()
    sel_country_data_df.columns = ["Country", "Status"]
    sel_country_data_df = sel_country_data_df
    visa_dest_country = sel_country_data_df[
        sel_country_data_df["Country"] == dest_country.title()
    ]

    return visa_dest_country


class Visa_Status:
    def __init__(self, download_url, resident_country):
        tprint("VISA-CLI")
        print("Downloading Visa data...\n")
        self.download_url = download_url
        self.resident_country = resident_country

        # Generate Country dataframe
        # --------------------------

        self.passport_df = pd.read_csv(self.download_url)
        # Transpose the selected data
        country_data_df = self.passport_df[
            self.passport_df["Passport"] == resident_country
        ].transpose()  # Select
        country_data_df = country_data_df.iloc[1:]  # Delete first two rows

        # Reset the index and rename the column names
        country_data_df = country_data_df.reset_index()
        country_data_df.columns = ["Country", "Status"]
        self.country_data_df = country_data_df

    def get_status_vf(self):
        """Get Countries that doesn't need a Visa """

        visa_free_df = self.country_data_df[
            self.country_data_df["Status"] == "visa free"
        ]
        visa_free_df = visa_free_df.reset_index()
        visa_free_df = visa_free_df.drop("index", 1)
        visa_free_df.columns = ["Destination Country", "Status"]
        visa_free_df.insert(0, "Resident Country", self.resident_country)
        print(tabulate(visa_free_df, headers="keys", tablefmt="pretty", showindex=True))

    def get_status_vr(self):
        """Get Countries that needs a Visa"""

        visa_required_df = self.country_data_df[
            self.country_data_df["Status"] == "visa required"
        ]
        visa_required_df = visa_required_df.reset_index()
        visa_required_df = visa_required_df.drop("index", 1)
        visa_required_df.columns = ["Destination Country", "Status"]
        visa_required_df.insert(0, "Resident Country", self.resident_country)
        print(
            tabulate(
                visa_required_df, headers="keys", tablefmt="pretty", showindex=True
            )
        )

    def get_status_voa(self):
        """Get Countries that permits Visa On Arrival"""

        visa_on_arrival_df = self.country_data_df[
            self.country_data_df["Status"] == "visa on arrival"
        ]
        visa_on_arrival_df = visa_on_arrival_df.reset_index()
        visa_on_arrival_df = visa_on_arrival_df.drop("index", 1)
        visa_on_arrival_df.columns = ["Destination Country", "Status"]
        visa_on_arrival_df.insert(0, "Resident Country", self.resident_country)
        print(
            tabulate(
                visa_on_arrival_df, headers="keys", tablefmt="pretty", showindex=True
            )
        )

    def get_status_eta(self):
        """Get Countries offering Electronic Travel Authority"""

        # eta - electronic travel authority
        visa_eta_df = self.country_data_df[self.country_data_df["Status"] == "e-visa"]
        visa_eta_df = visa_eta_df.reset_index()
        visa_eta_df = visa_eta_df.drop("index", 1)
        visa_eta_df.columns = ["Destination Country", "Status"]
        visa_eta_df.insert(0, "Resident Country", self.resident_country)
        print(tabulate(visa_eta_df, headers="keys", tablefmt="pretty", showindex=True))

    def get_status_vfe(self):
        """Get Countries offering Visa Free Days """

        visa_free_days_df = self.country_data_df[
            pd.to_numeric(self.country_data_df["Status"], errors="coerce").notnull()
        ]
        visa_free_days_df = visa_free_days_df.reset_index()
        visa_free_days_df = visa_free_days_df.drop("index", 1)
        visa_free_days_df.columns = ["Destination Country", "Status"]
        visa_free_days_df.insert(0, "Resident Country", self.resident_country)
        visa_free_days_df.columns = [
            "Resident Country",
            "Destination Country",
            "Visa Free Days",
        ]
        print(
            tabulate(
                visa_free_days_df, headers="keys", tablefmt="pretty", showindex=True
            )
        )

    def get_covid_ban(self):
        """Get Countries that banned visa due to covid"""
        visa_covid_ban_df = self.country_data_df[
            self.country_data_df["Status"] == "covid ban"
        ]

        visa_covid_ban_df = visa_covid_ban_df.reset_index()
        visa_covid_ban_df = visa_covid_ban_df.drop("index", 1)
        visa_covid_ban_df.columns = ["Destination Country", "Status"]
        visa_covid_ban_df.insert(0, "Resident Country", self.resident_country)
        print(
            tabulate(
                visa_covid_ban_df, headers="keys", tablefmt="pretty", showindex=True
            )
        )

    def interactive_prompt(self):
        """Interactive Prompt to offer Visa status"""
        countries_list = self.country_data_df["Country"].to_list()
        print("Press Any Key to Exit!")
        while True:
            country_completer = FuzzyWordCompleter(countries_list)
            print("\n")

            selected_country = prompt(
                "Destination Country:", completer=country_completer
            )

            selected_country_status = self.country_data_df[
                self.country_data_df["Country"] == selected_country
            ]

            try:
                print(selected_country_status["Status"].to_list()[0])
            except:
                print("Exiting...\n")
                exit()

    def get_group_status(self, group, dest_country):
        """ Get status for a group of different citizens """
        print("Visa Status for various Resident Countries\n")
        group = group.title()  # Convert to Title Case
        countries_list = group.split(",")  # Convert to a list
        countries_list.insert(0, self.resident_country)
        result_index = 0
        result_df = pd.DataFrame(
            columns=["Resident Country", "Destination Country", "Status"]
        )
        for country in countries_list:
            country = country.strip()
            result_dest_country = get_sel_country_status(
                self.passport_df, country, dest_country
            )["Country"].to_string(header=False, index=False)

            result_dest_country_status = get_sel_country_status(
                self.passport_df, country, dest_country
            )["Status"].to_string(header=False, index=False)

            if (
                result_dest_country_status == "28"
                or result_dest_country_status == "30"
                or result_dest_country_status == "90"
                or result_dest_country_status == "120"
                or result_dest_country_status == "180"
            ):
                result_dest_country_status += " Days Visa Free"

            result_df.loc[result_index] = (
                [country.strip()]
                + [result_dest_country.strip()]
                + [result_dest_country_status]
            )

            result_index += 1
        print("\n")
        print(tabulate(result_df, headers="keys", tablefmt="pretty", showindex=True))

    def get_dest_country_status(self, dest_country):
        """Get Visa Status for the destination Country"""

        visa_dest_country = self.country_data_df[
            self.country_data_df["Country"] == dest_country.title()
        ]
        visa_dest_country = visa_dest_country.reset_index()
        visa_dest_country = visa_dest_country.drop("index", 1)
        visa_dest_country.columns = ["Destination Country", "Status"]
        visa_dest_country.insert(0, "Resident Country", self.resident_country)
        print(
            tabulate(
                visa_dest_country, headers="keys", tablefmt="pretty", showindex=True
            )
        )
