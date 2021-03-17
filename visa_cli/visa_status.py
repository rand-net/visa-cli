from art import *
import pandas as pd
import requests
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from sys import exit


class Visa_Status:
    def __init__(self, download_url, resident_country):
        tprint("VISA-CLI")
        print("Downloading Visa data...\n")
        self.download_url = download_url
        self.resident_country = resident_country

        # Generate Country dataframe
        # --------------------------
        # passport_csv = requests.get(self.download_url)
        # passport_df = pd.read_csv(passport_csv)

        passport_df = pd.read_csv(self.download_url)
        # Transpose the selected data
        country_data_df = passport_df[
            passport_df["Passport"] == resident_country
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
        return visa_free_df

    def get_status_vr(self):
        """Get Countries that needs a Visa"""

        visa_required_df = self.country_data_df[
            self.country_data_df["Status"] == "visa required"
        ]
        return visa_required_df

    def get_status_voa(self):
        """Get Countries that permits Visa On Arrival"""

        visa_on_arrival_df = self.country_data_df[
            self.country_data_df["Status"] == "visa on arrival"
        ]
        return visa_on_arrival_df

    def get_status_eta(self):
        """Get Countries offering Electronic Travel Authority"""

        # eta - electronic travel authority
        visa_eta_df = self.country_data_df[self.country_data_df["Status"] == "e-visa"]
        return visa_eta_df

    def get_status_vfe(self):
        """Get Countries offering Visa Free Days """

        visa_free_days_df = self.country_data_df[
            pd.to_numeric(self.country_data_df["Status"], errors="coerce").notnull()
        ]
        return visa_free_days_df

    def get_covid_ban(self):
        """Get Countries that banned visa due to covid"""
        visa_covid_ban = self.country_data_df[
            self.country_data_df["Status"] == "covid ban"
        ]

        return visa_covid_ban

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
