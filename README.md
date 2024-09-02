<a href="https://www.fz-juelich.de/en/iek/iek-3"><img src="https://raw.githubusercontent.com/OfficialCodexplosive/README_Assets/862a93188b61ab4dd0eebde3ab5daad636e129d5/FJZ_IEK-3_logo.svg" alt="FZJ Logo" width="300px"></a>

# CuCoPy - Currency Conversion for Python

The CuCoPy package provides methods for exchanging currencies and adjusting monetary values for inflation until 1960 on a yearly basis.

## Features
* adjust money for inflation (1960 - last calendar year)
* exchange currencies from 260+ countries

## Installation


### Installation from conda-forge

CuCoPy can be installed into a new environment with the following command

	mamba create -n -c conda-forge cucopy_env cucopy

Or can be installed into an exisitng and activated environment with

	mamba install -c conda-forge cucopy
 

**Note on Mamba vs.Conda:** `mamba` commands can be substitued with `conda`. We highly recommend using [(Micro-)Mamba](https://mamba.readthedocs.io/en/latest/) instead of Conda. The recommended way to use Mamba on your system is to install the [Miniforge distribution](https://github.com/conda-forge/miniforge#miniforge3). They offer installers for Windows, Linux and OS X. In principle, Conda and Mamba are interchangeable. The commands and concepts are the same. The distributions differ in the methodology for determining dependencies when installing Python packages. Mamba relies on a more modern methodology, which (with the same result) leads to very significant time savings during the installation of ETHOS.FINE. Switching to Mamba usually does not lead to any problems, as it is virtually identical to Conda in terms of operation.


### Installation from pypi into a conda envrionment

First create a new environment that contains python and pip

	mamba create -n cucopy_env python pip

Activate the environment

	mamba activate cucopy_env
CuCoPy can be installed directly via pip:

	pip install cucopy

**Note on using pip within a conda environment** To install packages within a conda environment pip must already be installed in that environment. Please see this [Stack Overflow post](https://stackoverflow.com/questions/41060382/using-pip-to-install-packages-to-anaconda-environment) and this [Anaconda Article](https://www.anaconda.com/blog/understanding-conda-and-pip).


### Local installation for Development 
Alternatively, it can also be installed via git - this will preserve the connection to the GitHub repository:

	git clone https://github.com/FZJ-IEK3-VSA/CuCoPy

Change the directory into the new repository

	cd cucopy


### Installation with Conda Dependencies
Create a new environment with all necessary conda depenendcies

	mamba env create --file=environment.yml

Install the local package in development mode

	pip install -e . --no-deps

#### Installation with PyPi Dependencies
Then install CuCoPy via python as follows
	
	
	pip install -e .

## Example	
In the following code snippet, a value from 2010 is given in Euros and its remaining purchasing power in 2021 is to be calculated:

	from cucopy import Currency

	# Here, the ISO code may be omitted as the CuCoPy package defaults to "de" (Euro)
	de_cur = Currency(recording_year="2010", value=500, iso="de")
	de_cur.set_target_year("2021")

	remaining_pp = de_cur.get_purchasing_power()
	>> 492.9009...

Subsequently one might also want to get the equivalent worth of an earlier recorded value:
    
	...
	gb_cur = Currency(recording_year="1999", value=100, iso="gb")
	gb_cur.set_target_year("2000")

	equiv_worth = gb_cur.get_equivalent_worth()
	>> 101.1829...

Note: the preceding example is taken from the UK Parliament's statistical literacy guide "How to adjust for inflation", which provided formulas on working with the consumer price index (CPI) and inflation rates.

To exchange monetary values between currencies, the target currency's ISO code has to be provided:

	...
	de_cur = Currency("2015", 500)
	de_cur.set_target_currency("us")

	exchanged_val = de_cur.get_exchanged_value()
	>> 554.7564...

A workflow to adjust for inflation and exchange the newly-adjusted value might look like this:

	...
	recording_year = "2015"
	recording_value = 100
	recording_iso = "de"
	target_iso = "us"
	target_year = "2020"

	recording_cur = Currency(recording_year, recording_value, recording_iso)
	recording_cur.set_target_year(target_year)

	adjusted_value = recording_cur.get_equivalent_worth()
	>> 105.8093...

	recording_cur.set_value(adjusted_value)
	recording_cur.set_recording_year(target_year)

	recording_cur.set_target_currency(target_iso)
	recording_cur.get_exchanged_value()
	>> 120.8549...

## License

MIT License

Copyright (c) 2021-2024 Julian Schönau (FZJ/ICE-2), Patrick Kuckertz (FZJ/ICE-2), Jann Weinand (FZJ/ICE-2), Leander Kotzur (FZJ/IEK-3), Detlef Stolten (FZJ/ICE-2)

You should have received a copy of the MIT License along with this program.
If not, see https://opensource.org/licenses/MIT

## About Us

<p align="center"><a href="https://www.fz-juelich.de/en/ice/ice-2"><img src="https://raw.githubusercontent.com/FZJ-IEK3-VSA/README_assets/main/JSA-Header.svg" alt="Institut ICE-2"></a></p>
We are the <a href="https://www.fz-juelich.de/en/ice/ice-2">Institute of Climate and Energy Systems (ICE) - Jülich Systems Analysis</a> belonging to the <a href="https://www.fz-juelich.de/en">Forschungszentrum Jülich</a>. Our interdisciplinary department's research is focusing on energy-related process and systems analyses. Data searches and system simulations are used to determine energy and mass balances, as well as to evaluate performance, emissions and costs of energy systems. The results are used for performing comparative assessment studies between the various systems. Our current priorities include the development of energy strategies, in accordance with the German Federal Government’s greenhouse gas reduction targets, by designing new infrastructures for sustainable and secure energy supply chains and by conducting cost analysis studies for integrating new technologies into future energy market frameworks.

## Acknowledgements

The CuCoPy package relies heavily on the datasets made available by the *International Monetary Fund* (IMF), but is neither affiliated with or endorsed by either parties.

The *IMF* API provides information on international exchange rates as well as consumer price indices and is used for research purposes. Their terms can be accessed here: https://www.imf.org/external/terms.htm

This work is supported by the Federal Ministry for Economic Affairs and Climate Action (BMWK) with a grant for the project LOD-GEOSS (03EI1005B).

<a href="https://www.bmwk.de/Navigation/EN/Home/home.html"><img src="https://www.bmwk.de/SiteGlobals/BMWI/StyleBundles/Bilder/bmwi_logo_en.svg?__blob=normal&v=13" alt="BMWK Logo" width="130px"></a>
