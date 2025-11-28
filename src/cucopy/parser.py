from . import utils 


class Parser(object):
    """
    The Parser class provides the following functionality:
    * It parses data from a given dataset and extracts either the CPI value or the exchange rate for a currency from a given date.
    
    The parameter stored in a Parser object refers to:
    * the ISO 3166 ALPHA-2 code, which identifies a country and therefore the dominant currency.
    """
    def __init__(self, ignore_cache: bool=False, normalize_to: str="USD", aggregate_from: str="A"):
        """
        Constructor for creating a Currency class instance
        **Arguments:**
        :param iso: the ISO 3166 ALPHA-2 code, which identifies a country.
        :type iso: string
        """
        self.ignore_cache = ignore_cache
        self.normalize_to = normalize_to.lower() # "USD" or "SDR"
        self.aggregate_from = aggregate_from # "A" or "M"
        #self.country_name = country

    def get_cpi(self, currency: str, year : str) -> float:
        """
        Function for extracting the cpi from the International Monetary Fund dataset for CPI (PCPI_IX).

        Args:
            currency (str): Currency, from which to get the CPI.
            year (str): Year, from which to get the CPI for the currency.
        """

        if currency == "EUR":
            cpi = utils.get_single_imf_datapoint(
                dataset_id=utils.IMF_DATASET_IDS['cpi_harmonised'],
                currency=currency,
                year=year,
                ignore_cache=self.ignore_cache,
                frequency=self.aggregate_from
            ) 

        elif currency in {"XOF", "XCD"}:
            raise ValueError(f"CPI data not available for currency {currency}")
        
        else:
            cpi = utils.get_single_imf_datapoint(
                dataset_id=utils.IMF_DATASET_IDS['cpi'],
                currency=currency,
                year=year,
                ignore_cache=self.ignore_cache,
                frequency=self.aggregate_from
            )

        return cpi


    def get_exchange_rate(self, currency: str, year : str) -> float:
        """
        Function for extracting the exchange rate from the International Monetary Fund dataset for Exchange Rates (ENSA_XDC_XDR_RATE).

        Args:
            currency (str): Currency, from which to get the ER.
            year (str): Year, from which to get the ER for the currency.
            normalize_to (str): Either "usd" or "sdr", to which the exchange rate should be normalized.
        """

        exchange_rate = utils.get_single_imf_datapoint(
            dataset_id=utils.IMF_DATASET_IDS[f'er_avg_{self.normalize_to}'],
            currency=currency,
            year=year,
            ignore_cache=self.ignore_cache,
            frequency=self.aggregate_from
        )

        return exchange_rate