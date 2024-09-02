from . import utils 

class Parser(object):
    """
    Parser class
    The Parser class provides the following functionality:
    * It parses data from a given dataset and extracts either the CPI value or the exchange rate for a currency from a given date.
    
    The parameter stored in a Parser object refers to:
    * the ISO 3166 ALPHA-2 code, which identifies a country and therefore the dominant currency.
    """
    def __init__(self, country : str):
        """
        Constructor for creating a Currency class instance
        **Arguments:**
        :param iso: the ISO 3166 ALPHA-2 code, which identifies a country.
        :type iso: string
        """
        self.country_name = country

    def get_cpi(self, year : str):
        """
        Function for extracting the cpi from the International Monetary Fund dataset for CPI (PCPI_IX).
        :param year: the year, from which to get the CPI for the currency identified by its ISO code.
        :type year: string
        """
        cpi = utils.get_single_imf_datapoint(
            dataset_id=utils.IMF_DATASET_IDS['cpi'],
            country=self.country_name,
            year=year
        )

        return float(cpi)

    def get_exchange_rate(self, year : str, _country=None):
        """
        Function for extracting the exchange rate from the International Monetary Fund dataset for Exchange Rates (ENSA_XDC_XDR_RATE).
        :param year: the year, from which to get the CPI for the currency identified by its ISO code.
        :type year: string
        """
        country_name = self.country_name if _country is None else _country

        exchange_rate = utils.get_single_imf_datapoint(
            dataset_id=utils.IMF_DATASET_IDS['national_currency_per_sdr_aop'],
            country=country_name,
            year=year
        )

        return float(exchange_rate)        