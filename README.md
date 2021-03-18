# visa-cli

A python script to lookup [Passport Index Dataset](https://github.com/ilyankou/passport-index-dataset)

![PyPI](https://img.shields.io/pypi/v/visa-cli?style=flat-square)
![GitHub](https://img.shields.io/github/license/rand-net/visa-cli?style=flat-square)

## Installation

```
pip install visa-cli

```

## Usage

```
usage: visa-cli [-h] [-d DESTINATION_COUNTRY] [-f] [-r] [-o] [-e] [-n] [-c]
                [-i] [-l RESIDENT_COUNTRIES]
                resident_country

positional arguments:
  resident_country      Current Resident Country

optional arguments:
  -h, --help            show this help message and exit
  -d DESTINATION_COUNTRY, --destination-country DESTINATION_COUNTRY
                        Destination Country
  -f, --visa-free       Countries not requiring Visa
  -r, --visa-required   Countries requiring Visa
  -o, --visa-on-arrival
                        Countries offering Visa on arrival
  -e, --eta             Countries offering Electronic Travel Authority
  -n, --visa-free-days  Countries offering Visa free days
  -c, --covid-ban       Countries not offering Visa due to Covid-19
  -i, --interactive     Interactive Prompt
  -l RESIDENT_COUNTRIES, --resident-countries RESIDENT_COUNTRIES
                        A list of Resident Countries in addition to the
                        Current Resident Country. Format argument in a comma-
                        delimited string "Israel, Russia, China"

```


* Lookup on an interactive prompt
```
visa-cli -i Vatican

__     __ ___  ____      _             ____  _      ___
\ \   / /|_ _|/ ___|    / \           / ___|| |    |_ _|
 \ \ / /  | | \___ \   / _ \   _____ | |    | |     | |
  \ V /   | |  ___) | / ___ \ |_____|| |___ | |___  | |
   \_/   |___||____/ /_/   \_\        \____||_____||___|


Downloading Visa data...

Press Any Key to Exit!


Destination Country:Italy
90


Destination Country:United States
visa required


Destination Country:Romania
90


Destination Country:
                     Albania
                     Algeria
                     Andorra


```

* Lookup for a particular resident and destination Country.

```
visa-cli  Vatican -d Russia

__     __ ___  ____      _             ____  _      ___
\ \   / /|_ _|/ ___|    / \           / ___|| |    |_ _|
 \ \ / /  | | \___ \   / _ \   _____ | |    | |     | |
  \ V /   | |  ___) | / ___ \ |_____|| |___ | |___  | |
   \_/   |___||____/ /_/   \_\        \____||_____||___|


Downloading Visa data...

+---+------------------+---------------------+-----------+
|   | Resident Country | Destination Country |  Status   |
+---+------------------+---------------------+-----------+
| 0 |     Vatican      |       Russia        | covid ban |
+---+------------------+---------------------+-----------+

```

* Lookup for a group of resident Countries.

```
$ visa-cli  Israel  -l "Germany, Austria, India" -d Canada

__     __ ___  ____      _             ____  _      ___
\ \   / /|_ _|/ ___|    / \           / ___|| |    |_ _|
 \ \ / /  | | \___ \   / _ \   _____ | |    | |     | |
  \ V /   | |  ___) | / ___ \ |_____|| |___ | |___  | |
   \_/   |___||____/ /_/   \_\        \____||_____||___|


Downloading Visa data...

Visa Status for various Resident Countries



+---+------------------+---------------------+-----------+
|   | Resident Country | Destination Country |  Status   |
+---+------------------+---------------------+-----------+
| 0 |      Israel      |       Canada        | covid ban |
| 1 |     Germany      |       Canada        | covid ban |
| 2 |     Austria      |       Canada        | covid ban |
| 3 |      India       |       Canada        | covid ban |
+---+------------------+---------------------+-----------+

```
