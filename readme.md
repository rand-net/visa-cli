# visa-cli

A python script to lookup [Passport Index Dataset](https://github.com/ilyankou/passport-index-dataset)

## Installation

```
git clone
pip install -r requirements.txt
chmod +x visa-cli
visa-cli -f  Sweden

```

## Usage

```

usage: visa-cli [-h] [-f] [-r] [-o] [-e] [-n] [-c] [-i] resident_country

positional arguments:
  resident_country      Current Resident Country

optional arguments:
  -h, --help            show this help message and exit
  -f, --visa-free       Countries not requiring Visa
  -r, --visa-required   Countries requiring Visa
  -o, --visa-on-arrival
                        Countries offering Visa on arrival
  -e, --eta             Countries offering Electronic Travel Authority
  -n, --visa-free-days  Countries offering Visa free days
  -c, --covid-ban       Countries not offering Visa due to Covid-19
  -i, --interactive     Interactive Prompt

```

* Lookup  all Countries offering visa-free travel given a resident Country.
```
visa-cli Germany -f

```
* Lookup all Countries requiring visa given a resident Country.
```
visa-cli   China -r

```
* Lookup all Countries offering visa-on-arrival given a resident Country.
```
visa-cli  Vatican -o

```
* Lookup all Countries offering ETA(Electronic Travel Authority) given a resident Country.
```
visa-cli  Vatican -e

```
