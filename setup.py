import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="visa-cli",
    version="0.2.0",
    description="CLI tool to lookup Visa status for Countries",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rand-net/visa-cli",
    author="rand-net",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    # packages=["visa_cli"],
    include_package_data=True,
    entry_points={"console_scripts": ["visa-cli = visa_cli.__init__:main"]},
    install_requires=["art", "prompt-toolkit", "requests", "pandas", "tabulate"],
    keywords=["awesome list", "awesome", "resources", "lists", "mammoths"],
)
