from . import utils 
import pandas as pd
import os

EURO_AREA = ['DE']
EURO_ADOPTION = 1999

class Parser(object):
    """
    Parser class
    The Parser class provides the following functionality:
    * It parses data from a given dataset and extracts either the CPI value or the exchange rate for a currency from a given date.
    
    The parameter stored in a Parser object refers to:
    * the ISO 3166 ALPHA-2 code, which identifies a country and therefore the dominant currency.
    """
    def __init__(self, iso : str, use_local_data : bool = False):
        """
        Constructor for creating a Currency class instance
        **Arguments:**
        :param iso: the ISO 3166 ALPHA-2 code, which identifies a country.
        :type iso: string
        """
        self.iso_code = iso

        if use_local_data:
            self.use_local_data = use_local_data
            self.er_df = self.load_csv("data/IFS_EREER_1979-2021.csv")
            self.cpi_df = self.load_csv("data/IFS_CPI_1950-2021.csv")

    def get_cpi(self, year : str):
        """
        Function for extracting the cpi from the World Bank dataset for total CPI (FP.CPI.TOTL).
        :param year: the year, from which to get the CPI for the currency identified by its ISO code.
        :type year: string
        """
        dataset_id = utils.WB_DATASET_IDS['cpi']
        iso = self.iso_code
        out_format = 'json'
        data = utils.get_wb_dataset(id=dataset_id, date=year, iso=iso, format=out_format, download_as=None)
        if data == None:
            print(dataset_id, year, iso, out_format)
        try:
            return float(data[1][0]['value'])
        except Exception as e:
            print(e, "\n", dataset_id, year, iso, out_format)

    def get_exchange_rate(self, year : str, _iso=None):
        """
        Function for extracting the exchange rate from the World Bank dataset for total CPI (FP.CPI.TOTL).
        :param year: the year, from which to get the CPI for the currency identified by its ISO code.
        :type year: string
        """
        #dataset_id = utils.IMF_DATASET_IDS['national_currency_per_sdr_aop']
        dataset_id = utils.IMF_DATASET_IDS['real_effective_exchange_rate_b_cpi']
        iso = self.iso_code.upper() if _iso==None else _iso.upper()
        data, url_ = utils.get_imf_dataset(indicator=dataset_id, date=year, geo_code=iso.upper())

        try:
            exchange_rate = data['Series']['Obs']['@OBS_VALUE']
        except Exception as e:
            raise( ValueError("No data available.") )

        return float(exchange_rate)

    def load_csv(self, _path="data/IFS_EREER_1979-2021.csv"):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, _path)
        return pd.read_csv(filename)

    def get_exchange_rate_from_csv(self, year, _iso=None, _path=None, _country=None):
        if _path is not None:
            self.er_df = self.load_csv(_path)
        ref = self.iso_code.upper() if _iso==None else _iso.upper()
        country_name = utils.IMF_REF_TO_COUNTRY_NAME[ref.upper()] if _country == None else _country
        try:
            edf = self.er_df.copy()
            rval = edf.loc[edf['Country Name'] == country_name][str(year)].values[0]
            return rval
        except Exception as e:
            print(e)

    def get_cpi_from_csv(self, year, _iso=None, _path=None, _country=None):
        if _path is not None:
            self.cpi_df = self.load_csv(_path)
        ref = self.iso_code.upper() if _iso==None else _iso.upper()
        country_name = utils.IMF_REF_TO_COUNTRY_NAME[ref.upper()] if _country == None else _country
        try:
            cdf = self.cpi_df.copy()
            rval = cdf.loc[(cdf["Country Name"] == country_name) & (cdf["Attribute"] == "Value")][str(year)].values[0]
            return rval
        except Exception as e:
            print(e)

        