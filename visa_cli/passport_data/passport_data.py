import requests
import socket
import pandas as pd
import json
import sys


class PassportData:
    """Retrieves  Passport Data of Countries"""

    def __init__(self):
        self.country_codes_url = "https://gist.githubusercontent.com/ilyankou/b2580c632bdea4af2309dcaa69860013/raw/420fb417bcd17d833156efdf64ce8a1c3ceb2691/country-codes"
        self.country_codes = ""
        self.passport_comparison_data_url = (
            "https://www.passportindex.org/comparebyPassport.php?p1=ro&p2=gt&p3=qa"
        )
        self.passport_data_url = "https://www.passportindex.org/incl/compare2.php"
        self.passport_data = ""
        self.passport_data_cleaned = {}

    def get_country_codes_iso2(self):
        """Get Country codes in ISO2 format"""

        self.country_codes = (
            pd.read_csv(
                self.country_codes_url,
                dtype=str,
            )
            .fillna("NA")
            .set_index("ISO2")
        )

    def fix_country_codes_iso2(self, x):
        """Fix ISO2 Country codes for some Countries """

        o = {"UK": "GB", "RK": "XK"}
        return o[x] if x in o else x

    def get_passport_data(self):
        """Retrieves Passport data from passportindex.org"""

        try:
            passport_data_raw = requests.post(
                self.passport_data_url,
                headers={
                    "Host": "www.passportindex.org",
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Length": "9",
                    "Origin": "https://www.passportindex.org",
                    "DNT": "1",
                    "Connection": "keep-alive",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "TE": "Trailers",
                },
                data={"compare": "1"},
            )
        except socket.gaierror as e:
            print("Error Connecting!\n", e)
            sys.exit(1)
        except requests.ConnectionError as e:
            print("Error Connecting!\n", e)
            sys.exit(1)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            sys.exit(1)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            sys.exit(1)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            sys.exit(1)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            sys.exit(1)

        self.passport_data = json.loads(passport_data_raw.text)

    def clean_passport_data(self):
        "Clean Passport data and filter them by Visa requirements"

        for passport in self.passport_data:
            # Fix ISO-2 codes
            passport = self.fix_country_codes_iso2(passport)

            # Add passport to the passport_data_cleaned
            if passport not in self.passport_data_cleaned:
                self.passport_data_cleaned[passport] = {}

            # Add destinations for the given passport
            for dest in self.passport_data[passport]["destination"]:

                text = dest["text"]
                res = ""

                # ** Visa required, incl Cuba's tourist card **
                if text == "visa required" or text == "tourist card":
                    res = "visa required"

                # ** Visa on arrival **
                elif "visa on arrival" in text:
                    res = "visa on arrival"

                # ** Covid-19 ban **
                elif text == "COVID-19 ban":
                    res = "covid ban"

                # ** Visa-free, incl. Seychelles' tourist registration **
                elif "visa-free" in text or "tourist registration" in text:
                    res = dest["dur"] if dest["dur"] != "" else "visa free"

                # ** eVisas, incl eVisitors (Australia), eTourist cards (Suriname),
                # eTA (US), and pre-enrollment (Ivory Coast) **
                elif (
                    "eVis" in text
                    or "eTourist" in text
                    or text == "eTA"
                    or text == "pre-enrollment"
                ):
                    res = "e-visa"

                # ** No admission, including Trump ban **
                elif text == "trump ban" or text == "not admitted":
                    res = "no admission"

                # Update the result!
                self.passport_data_cleaned[passport][
                    self.fix_country_codes_iso2(dest["code"])
                ] = (res if res != "" else dest["text"])

    def get_passport_data_country_names_matrix(self):
        """ Returns Passport data in Country names matrix format"""

        matrix = pd.DataFrame(self.passport_data_cleaned).T.fillna(-1)
        iso2name = {x: y["Country"] for x, y in self.country_codes.iterrows()}
        matrix = matrix.rename(columns=iso2name, index=iso2name)
        # Set Index Label
        matrix["Passport"] = matrix.index
        matrix = matrix.reset_index(drop=True)
        return matrix
