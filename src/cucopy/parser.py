from typing import Annotated
from datadesclib import meta
from . import utils 


@meta(
    semanticConcept="IMFDataParser",
    description="The Parser class provides functionality to parse data from IMF and extract CPI or exchange rates."
)
class Parser(object):
    """
    The Parser class provides the following functionality:
    * It parses data from a given dataset and extracts either the CPI value or the exchange rate for a currency from a given date.
    
    The parameter stored in a Parser object refers to:
    * the ISO 3166 ALPHA-2 code, which identifies a country and therefore the dominant currency.
    """
    @meta(description="Constructor for creating a Parser instance.")
    def __init__(
        self,
        ignore_cache: Annotated[bool, {
            "description": "Whether to ignore the local cache and fetch fresh data from IMF",
            "default": False
        }] = False,
        normalize_to: Annotated[str, {
            "description": "Target currency for normalization of exchange rates",
            "default": "USD"
        }] = "USD",
        aggregate_from: Annotated[str, {
            "description": "Frequency for data aggregation",
            "enum": ["A", "M"],
            "note": "'A' for annual, 'M' for monthly",
            "default": "A"
        }] = "A"
    ):
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

    @meta(
        semanticConcept="ConsumerPriceIndexRetrieval",
        description="Function for extracting the cpi from the International Monetary Fund dataset for CPI (PCPI_IX)."
    )
    def get_cpi(
        self,
        currency: Annotated[str, {
            "description": "ISO 4217 Currency code",
            "example": "EUR",
            "minLength": 3,
            "maxLength": 3
        }],
        year: Annotated[str, {
            "description": "Target year for the CPI data",
            "pattern": "^[0-9]{4}$",
            "example": "2023"
        }]
    ) -> Annotated[float, {"description": "The extracted Consumer Price Index (CPI) value", "type": "float"}]:
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

    @meta(
        semanticConcept="ExchangeRateRetrieval",
        description="Function for extracting the exchange rate from the International Monetary Fund dataset for Exchange Rates (ENSA_XDC_XDR_RATE)."
    )
    def get_exchange_rate(
        self,
        currency: Annotated[str, {
            "description": "ISO 4217 Currency code",
            "example": "JPY"
        }],
        year: Annotated[str, {
            "description": "Target year for the exchange rate",
            "pattern": "^[0-9]{4}$",
            "example": "2022"
        }]
    ) -> Annotated[float, {"description": "The extracted exchange rate relative to the normalized currency (USD/SDR)", "type": "float"}]:
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