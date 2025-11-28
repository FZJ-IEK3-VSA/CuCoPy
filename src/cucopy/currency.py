import datetime
from .parser import Parser


class Currency(object):
    """
    Currency class for handling values with inflation and exchange rate adjustments.

    Features:
        * Store and convert monetary values with scientific or custom notations (e.g. K, M, B).
        * Adjust values for inflation between two years.
        * Convert values between currencies using exchange rates.

    Attributes:
        _allowed_notations (dict): Mapping of notation symbols to their multiplier values.
        parser (Parser): Parser object for CPI and exchange rate data.
    """

    # dictionary of the most important scientific number notations and their value
    _allowed_notations = {
        ""  : int(1e0),
        "K" : int(1e3),
        "M" : int(1e6),
        "B" : int(1e9),
        "T" : int(1e12)         
    }

    def __init__(self, ignore_cache: bool=False, normalize_to: str="USD", aggregate_from: str="A", **kwargs):
        """
        Initialize a Currency instance with a Parser.

        Args:
            ignore_cache (bool): Whether to ignore cached data when fetching CPI and exchange rates.
            normalize_to (str): Currency to normalize input and target currency to for calculating exchange rates ("USD" or "SDR").
            aggregate_from (str): Frequency for exchange rates ("A" for annual, "M" for monthly).        
        """
        self.parser = Parser(ignore_cache=ignore_cache, normalize_to=normalize_to, aggregate_from=aggregate_from, **kwargs)         


    @classmethod
    def unique_notation(cls, notation : str, notation_pow : int):
        """
        Register a new notation symbol globally for all Currency objects.
        Example: Currency.unique_notation("G", 9)  # "G" = 10^9

        Args:
            notation (str): New and unique symbol/ string, by which the notation should be referred to
            notation_pow (int): Scientific notation of the new unit. The value of a unit is determined as follows: 1E[notation_pow]
        """

        if notation not in cls._allowed_notations:
            cls._allowed_notations[notation] = 10**notation_pow
        else:
            raise ValueError(f"Notation {notation} already defined.")


    def validate_year(self, year_str : str) -> str:
        """
        Validate that a string matches the YYYY format.

        Args:
            year_str (str): Year as a string.

        """

        try:
            year = datetime.datetime.strptime(year_str, "%Y").year
            return str(year)
        except ValueError as exc:
            raise ValueError("Incorrect year format, should be YYYY") from exc
    
        
    def apply_notation(self, value: float, value_notation: str):
        """
        Function to convert the value using a notation.

        Args:
            value (str): The value to convert.
            notation (str): Notation for converting the value.
        """

        if value_notation in self._allowed_notations:
            return value * self._allowed_notations[value_notation]
        else:
            raise ValueError(f"Notation {value_notation} not supported.\nSupported notations are: {self._allowed_notations}.")


    def adjust_for_inflation(self, value: float, currency: str, base_year: str, target_year: str, value_notation: str = None, mode: str = "equivalent"):
        """
        Function for getting the inflation-corrected value

        Args:
            value (float): The value to convert.
            currency(str): ISO code of the currency
            base_year (str): Year of the base value.
            target_year (str): Year for conversion.
            value_notation(str): Notation to be used for the value.
            mode (str, optional): "equivalent" (inflation-corrected worth) or "purchasing_power". Defaults to "equivalent".
        """
        
        base_year, target_year = self.validate_year(base_year), self.validate_year(target_year)
        if value_notation:
            value = self.apply_notation(value, value_notation)
        
        if base_year == target_year:
            # No adjustment needed.
            target_value = value  
        else:
            # Calculate inflation.
            base_cpi = self.parser.get_cpi(currency, base_year)
            target_cpi = self.parser.get_cpi(currency, target_year)

            if mode == "equivalent":
                target_value = value * target_cpi / base_cpi
            elif mode == "purchasing_power":
                target_value = value * base_cpi / target_cpi
            else:
                raise ValueError("Mode must be 'equivalent' or 'purchasing_power'.")
            
        return target_value


    def get_exchanged_value(self, value: float, year: str, base_currency: str, target_currency: str, value_notation: str = None):
        """
        Function for calculating the worth of the current currency in another country.

        Args:
            value (float): The value to convert.
            year (str): Year of the value.
            base_currency (str): ISO code of the base currency.
            target_currency (str): ISO code of the target currency.
            value_notation(str): Notation to be used for the value.
        """
        
        year = self.validate_year(year)
        if value_notation:
            value = self.apply_notation(value, value_notation)

        if base_currency == target_currency:
            # No conversion needed.
            target_value = value
        else:
            # Calculate exchanged value.
            base_rate = self.parser.get_exchange_rate(base_currency, year) #  USD or SDR per domestic currency
            target_rate = self.parser.get_exchange_rate(target_currency, year) # USD or SDR per domestic currency
            target_value = value * base_rate / target_rate

        return target_value
    
    
    def convert_currency(self, value: str, base_year: str, base_currency: str, target_year: str, target_currency: str, value_notation: str = None, operation_order: str = "inflation_first"):
        """
        Convert a currency value considering inflation and/or exchange rate.

        Args:
            value (float): Value to convert.
            base_year (str): Year of the base value.
            base_currency (str): ISO code of the currency of the input value.
            target_year (str): Year for conversion.
            target_currency (str): ISO code of the desired target currency.
            value_notation (str, optional): Scientific notation of the value (e.g., 'K', 'M').
            operation_order (str, optional): Determines which operation is applied first:
                                            - "inflation_first": adjust for inflation, then exchange
                                            - "exchange_first": convert currency, then adjust for inflation
                                            Defaults to "inflation_first".
        """
        
        if operation_order not in ["inflation_first", "exchange_first"]:
            raise ValueError("operation_order must be 'inflation_first' or 'exchange_first'")                

        if operation_order == "inflation_first":            
            # 1. Inflation adjustment in base currency
            value_after_inflation = self.adjust_for_inflation(value, base_currency, base_year, target_year, value_notation)
            # 2. Currency exchange to target currency
            converted_value = self.get_exchanged_value(value_after_inflation, target_year, base_currency, target_currency)
        else:  # exchange_first
            # 1. Exchange to target currency in base year
            value_after_exchange = self.get_exchanged_value(value, base_year, base_currency, target_currency, value_notation)
            # 2. Adjust for inflation in target currency
            converted_value = self.adjust_for_inflation(value_after_exchange, target_currency, base_year, target_year)

        return converted_value