<a href="https://www.fz-juelich.de/en/iek/iek-3"><img src="https://www.fz-juelich.de/static/media/Logo.2ceb35fc.svg" alt="FZJ Logo" width="200px"></a>

# CuCoPy - Currency Conversion for Python

The CuCoPy package provides methods for exchanging currencies and adjusting monetary values for inflation until 1960 on a yearly basis.

## Features
* adjust money for inflation (1960 - last calendar year)
* exchange currencies from 260+ countries

## Installation
CuCoPy can be installed directly via git - this will preserve the connection to the GitHub repository:

	git clone https://jugit.fz-juelich.de/iek-3/groups/data-and-model-integration/cucopy

Then install CuCoPy via python as follows
	
	cd cucopy
	python setup.py install 

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

Copyright (c) 2021-2022 Julian Schönau (FZJ/IEK-3), Patrick Kuckertz (FZJ/IEK-3), Jann Weinand (FZJ/IEK-3), Leander Kotzur (FZJ/IEK-3), Detlef Stolten (FZJ/IEK-3)

You should have received a copy of the MIT License along with this program.
If not, see https://opensource.org/licenses/MIT

## About Us

We are the [Institute of Energy and Climate Research - Techno-economic Systems Analysis (IEK-3)](https://www.fz-juelich.de/en/iek/iek-3) belonging to the [Forschungszentrum Jülich](https://www.fz-juelich.de/en). Our interdisciplinary department's research is focusing on energy-related process and systems analyses. Data searches and system simulations are used to determine energy and mass balances, as well as to evaluate performance, emissions and costs of energy systems. The results are used for performing comparative assessment studies between the various systems. Our current priorities include the development of energy strategies, in accordance with the German Federal Government’s greenhouse gas reduction targets, by designing new infrastructures for sustainable and secure energy supply chains and by conducting cost analysis studies for integrating new technologies into future energy market frameworks.

## Acknowledgements

The CuCoPy package relies heavily on the datasets made available by the *World Bank Group* and the *International Monetary Fund* (IMF), but is neither affiliated with or endorsed by either parties.

The *World Bank* API provides extensive information about consumer price indices and is used under the CC BY 4.0 license. Its terms of use can be accessed here: https://data.worldbank.org/summary-terms-of-use, https://creativecommons.org/licenses/by/4.0/

The *IMF* API provides information on international exchange rates and is used for research purposes. Their terms can be accessed here: https://www.imf.org/external/terms.htm

This work is supported by the Federal Ministry for Economic Affairs and Climate Action (BMWK) with a grant for the project LOD-GEOSS (03EI1005B).

<a href="https://www.bmwk.de/Navigation/EN/Home/home.html"><img src="https://www.bmwk.de/SiteGlobals/BMWI/StyleBundles/Bilder/bmwi_logo_en.svg?__blob=normal&v=13" alt="BMWK Logo" width="130px"></a>