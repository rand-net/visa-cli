import pandas as pd
import sys
from visa_cli.passport_data.passport_data import PassportData
from art import tprint
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from tabulate import tabulate


class VisaStatus:
    """Retrives Visa Information for a Country or a group of Countries """

    def __init__(self, resident_country, resident_countries, destination_country):
        tprint("VISA-CLI")
        self.resident_country = resident_country
        self.resident_countries = resident_countries
        self.destination_country = destination_country
        self.visa_data_raw = ""
        self.visa_status_all_countries = ""
        self.max_days_visa_free = 300

    def get_visa_data(self):
        """Downloads visa status CSV data for all Countries"""
        print("Downloading Visa data...")
        passdata = PassportData()
        passdata.get_country_codes_iso2()
        passdata.get_passport_data()
        passdata.clean_passport_data()
        self.visa_data_raw = passdata.get_passport_data_country_names_matrix()

    def get_status_all_dest_countries(self):
        """Retrieves Visa status for all destination Countries"""

        # Transpose the dataframe
        self.visa_status_all_countries = self.visa_data_raw[
            self.visa_data_raw["Passport"] == self.resident_country
        ].transpose()

        # Reset the index and rename the column names
        self.visa_status_all_countries = self.visa_status_all_countries.reset_index()
        self.visa_status_all_countries.columns = ["Destination Country", "Status"]
        self.visa_status_all_countries = self.visa_status_all_countries.iloc[
            :-1
        ]  # Drop the existing labels

    def get_status_given_dest_country(self):
        """Retrieves Visa Status for a selected destination Country"""

        self.get_status_all_dest_countries()
        visa_status_dest_country = self.visa_status_all_countries[
            self.visa_status_all_countries["Destination Country"]
            == self.destination_country.title()
        ]
        return visa_status_dest_country

    def get_status_multi_resident_countries(self):
        """ Get Visa status for a group of resident Countries """

        print("Visa Status for various Resident Countries\n")

        # Generate the list of resident Countries
        resident_countries = self.resident_countries.split(",")  # Convert to a list
        resident_countries = [country.title() for country in resident_countries]
        # Append default resident country
        resident_countries.insert(0, self.resident_country)

        # Generate Multi Resident Dataframe
        df_row_counter = 0
        multi_resident_visa_status = pd.DataFrame(
            columns=["Resident Country", "Destination Country", "Status"]
        )

        for resident_country in resident_countries:
            self.resident_country = resident_country.strip()

            # Get Visa status for current resident Country
            visa_status_destination_country = self.get_status_given_dest_country()[
                "Status"
            ].to_string(header=False, index=False)

            # If Visa free days, describe it
            if visa_status_destination_country in [
                str(i) for i in range(0, self.max_days_visa_free)
            ]:
                visa_status_destination_country += " Days Visa Free"

            # Add current row to dataframe
            multi_resident_visa_status.loc[df_row_counter] = (
                [resident_country.strip()]
                + [self.destination_country]
                + [visa_status_destination_country]
            )
            df_row_counter += 1

        return multi_resident_visa_status

    def format_countries_dataframe(self, countries_dataframe):
        countries_dataframe = countries_dataframe.reset_index()
        countries_dataframe = countries_dataframe.drop("index", axis=1)
        countries_dataframe.insert(0, "Resident Country", self.resident_country)
        countries_dataframe.sort_values("Destination Country")
        return countries_dataframe

    def get_all_countries(self):
        """Get Visa Status for all the Countries, given the resident Country"""

        visa_status_all_countries = self.visa_status_all_countries
        return self.format_countries_dataframe(visa_status_all_countries)

    def get_vf_countries(self):
        """Retrieves destination Countries that doesn't require a Visa """

        visa_free_countries = self.visa_status_all_countries[
            self.visa_status_all_countries["Status"] == "visa free"
        ]
        return self.format_countries_dataframe(visa_free_countries)

    def get_vr_countries(self):
        """Retrieves destination Countries that requires a Visa"""

        visa_required_df = self.visa_status_all_countries[
            self.visa_status_all_countries["Status"] == "visa required"
        ]
        return self.format_countries_dataframe(visa_required_df)

    def get_voa_countries(self):
        """Retrieves destination Countries that permits Visa On Arrival"""

        visa_on_arrival_countries = self.visa_status_all_countries[
            self.visa_status_all_countries["Status"] == "visa on arrival"
        ]
        return self.format_countries_dataframe(visa_on_arrival_countries)

    def get_eta_countries(self):
        """Retrieves destination Countries offering Electronic Travel Authority"""

        # eta - electronic travel authority
        visa_eta_countries = self.visa_status_all_countries[
            self.visa_status_all_countries["Status"] == "e-visa"
        ]
        return self.format_countries_dataframe(visa_eta_countries)

    def get_vfe_countries(self):
        """Retrieves destination  Countries offering Visa Free Days """

        visa_free_days_countries = self.visa_status_all_countries[
            pd.to_numeric(
                self.visa_status_all_countries["Status"], errors="coerce"
            ).notnull()
        ]
        return self.format_countries_dataframe(visa_free_days_countries)

    def get_covid_ban_countries(self):
        """Retrieves destination Countries that banned Visa due to Covid-19"""

        visa_covid_ban_countries = self.visa_status_all_countries[
            self.visa_status_all_countries["Status"] == "covid ban"
        ]
        return self.format_countries_dataframe(visa_covid_ban_countries)

    def launch_interactive_prompt(self):
        """Interactive Prompt to offer Visa status for all destination Countries """

        destination_countries_list = self.visa_status_all_countries[
            "Destination Country"
        ].to_list()
        destination_country_completer = FuzzyWordCompleter(destination_countries_list)
        print("\nPress Ctrl+c Key to Exit!\n")
        try:
            while True:
                selected_destination_country = prompt(
                    "Destination Country:", completer=destination_country_completer
                )

                # Get Visa Status of the selected destination Country
                selected_destination_country_visa_data = self.visa_status_all_countries[
                    self.visa_status_all_countries["Destination Country"]
                    == selected_destination_country
                ]
                selected_destination_country_visa_status = (
                    selected_destination_country_visa_data["Status"].to_list()[0]
                )
                print(selected_destination_country_visa_status)

        except KeyboardInterrupt:
            print("Exiting Visa-cli...\n")
            sys.exit(0)
