<a href="https://www.fz-juelich.de/en/iek/iek-3"><img src="https://raw.githubusercontent.com/OfficialCodexplosive/README_Assets/862a93188b61ab4dd0eebde3ab5daad636e129d5/FJZ_IEK-3_logo.svg" alt="FZJ Logo" width="300px"></a>

# CuCoPy - Currency Conversion for Python

The CuCoPy package provides methods for exchanging currencies and adjusting monetary values for inflation until 1960 on a yearly basis.

## Features
* Adjust money for inflation (1960 - last calendar year)
* Exchange currencies from 60+ countries.
* Data sources: Exchange rates (ER) and Consumer Price Index (CPI) from the [International Monetary Fund (IMF) API](https://fgeerolf.com/data/imf/api.html#ifs) and [IMF Data Explorer](https://data.imf.org/en/Data-Explorer?datasetUrn=IMF.STA:PPI(3.0.0))  

**Note on the Euro:** For countries using the Euro (EUR), CuCoPy assumes the harmonized inflation value for the Euro Area.

**Missing countries:** If the ER or CPI of a country's currency is missing for your conversion, please contact the developers to request support.


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

	mamba env create -f env.yml

Install the local package in development mode

	pip install -e . --no-deps

#### Installation with PyPi Dependencies
Then install CuCoPy via python as follows
	
	
	pip install -e .

## Example	
In the following code section, the value in 2020 Euro is converted to the value in 2025 USD.

	from cucopy import Currency
	cur = Currency()

	cur.convert_currency(value=100, base_year="2020", base_currency="EUR", target_year="2025", target_currency="USD", operation_order="inflation_first")
	>> 137.41

For a deeper look into the features of CuCoPy, there a tutorial notebook is available.

## License

MIT License

Copyright (C) 2021-2026 FZJ-ICE-2

Active Developers: Maxime Gorres, Jan Göpfert, Patrick Kuckertz, Jann Weinand

Alumni: Julian Schönau, Leander Kotzur, Detlef Stolten

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
