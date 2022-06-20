from . import utils 

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
    def __init__(self, iso : str):
        """
        Constructor for creating a Currency class instance
        **Arguments:**
        :param iso: the ISO 3166 ALPHA-2 code, which identifies a country.
        :type iso: string
        """
        self.iso_code = iso

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
        return float(data[1][0]['value'])

    def get_exchange_rate(self, year : str, _iso=None):
        """
        Function for extracting the exchange rate from the World Bank dataset for total CPI (FP.CPI.TOTL).
        :param year: the year, from which to get the CPI for the currency identified by its ISO code.
        :type year: string
        """
        dataset_id = utils.IMF_DATASET_IDS['national_currency_per_sdr_aop']
        iso = self.iso_code.upper() if _iso==None else _iso.upper()

        if iso in EURO_AREA and int(year) > int(EURO_ADOPTION):
            iso = 'U2'
        data = utils.get_imf_dataset(indicator=dataset_id, date=year, geo_code=iso.upper())

        exchange_rate = data['Series']['Obs']['@OBS_VALUE']

        return float(exchange_rate)


        