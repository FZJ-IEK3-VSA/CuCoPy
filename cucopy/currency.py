import datetime
import warnings
from .parser import Parser
from . import utils

class Currency(object):
    """
    Currency class

    The Currency class provides the following functionality:

    * It provides the basic structure of a value, meaning, it stores information about its dimension (i.e. the actual monetary value), its recording date and its unit.
    * In addition to the most common scientific number notations (K, M, B, T), it is also possible to store a currency with a custom notation and value.
    * It allows for easy adjustment for inflation of the provided value, in terms of taking a base value from date A and calculating its worth at date B.
    * It allows for easy exchange from one currency to another, using their ISO 2 codes.
    
    The parameters stored in a Currency object refer to:

    * the year, at which the value, which is to be transformed, was recorded (**recording_year**)
    * the actual value to be adjusted (**value**)
    * the scientific notation of the value (**notation**; e.g. 'K' for 1.000, 'M' for 1.000.000, etc.)
    * the iso code of the country in which the value was recorded (**iso**; default: 'de')

    When creating a Currency object with a custom notation, following parameters are added:

    * the scientific notation of the new unit (**notation_pow**; the value of a unit is determined as follows: 1E[notation_pow]).
    
    Following parameters are also stored in an instance of this class, but only after initialization:

    * the target year, meaning, the year, to which adjust the value to (**target_year**)
    * the parser, which handles the extraction of consumer price indices and exchange rate information from the World Bank and International Monetary Fund respectively (**parser**)
    """

    " dictionary of the most important scientific number notations and their value "
    _allowed_notations = {
        ""  : int(1e0),
        "K" : int(1e3),
        "M" : int(1e6),
        "B" : int(1e9),
        "T" : int(1e12)         
    }

    def __init__(self, recording_year : str, value : float = 1, iso : str = 'de', use_local_data=False, local_country=None, **kwargs):
        """
        Constructor for creating a Currency class instance

        **Required arguments:**
        :param recording_year: the year, at which a value was recorded
        :type recording_year: string

        **Default arguments:**
        :param value: the monetary value. The default value is 1
        :type value: float

        :param notation: the notation of the value. The default is '', meaning 1E0
        :type notation: string

        :param iso: the country code in which the value was recorded. The default is 'de'.
        :type iso: string
        """
        self.recording_year = self._validate_year(recording_year)
        self.value = value
        self.iso = iso
        self.parser = Parser(iso, use_local_data)
        self.use_local_data = use_local_data
        self.local_country = local_country

        if('notation' in kwargs):
            _notation = kwargs.get('notation')
            if _notation in self._allowed_notations:
                self.notation = kwargs.get('notation')
            else:
                raise ValueError(f"Notation {_notation} not supported.\nSupported notations are: {self._allowed_notations}.")
        else:
            self.notation = ""

    @classmethod
    def unique_notation(cls, recording_year : str, notation : str, notation_pow : int, value : float = 1, **kwargs):
        """
        Decorator for creating a Currency class instance with a custom notation.

        **Required arguments:**
        :param recording_year: the date, at which a value was recorded
        :type recording_year: string

        :param notation: the new and unique symbol/ string, by which the notation should be referred to
        :type notation: string

        :param notation_pow: the scientific notation of the new unit. The value of a unit is determined as follows: 1E[notation_pow]
        :type notation_pow: int

        **Default arguments:**
        :param value: the monetary value. The default value is 1
        :type value: float

        :param currency: the currency in which the value was recorded. The default is 'Eur'.
        :type currency: string
        """
        if value == None:
            value = 1
        if notation not in cls._allowed_notations:
            cls._allowed_notations[notation] = 10**notation_pow
        else:
            raise ValueError(f"Notation {notation} already defined.")
        return cls(recording_year, value, notation=notation, kwargs=kwargs)

    def _validate_year(self, year_str):
        """
        Helper function for checking, if a given string matches the YYYY date format.
        """
        try:
            return datetime.datetime.strptime(year_str, "%Y").year
        except ValueError:
            raise ValueError("Incorrect year format, should be YYYY")

    def set_value(self, val):
        """
        Function for setting the monetary value to be associated with this instance.

        :param val: the value to be associated with this Currency object
        :type val: float
        """
        self.value = val

    def set_recording_currency(self, iso_code):
        """
        Function for setting the recording country, from which should be exchanged.

        :param iso_code: the recording country's ISO code
        :type iso_code: string
        """
        self.iso = iso_code

    def set_recording_year(self, year_str):
        """
        Function for setting the recording year, from which should be adjusted.

        :param year_str: the recording year, as a string
        :type year_str: string
        """
        self.recording_year = self._validate_year(year_str)

    def set_target_year(self, year_str):
        """
        Function for setting the target year, to which should be adjusted to.

        :param year_str: the target year, as a string
        :type year_str: string
        """
        self.target_date = self._validate_year(year_str)

    def set_target_currency(self, iso_code):
        """
        Function for setting the target country, to which should be exchanged to.

        :param iso_code: the target country's ISO code
        :type iso_code: string
        """
        self.target_currency = iso_code

    def real_value(self):
        """
        Function for getting the real value of the Currency object.
        Obtained by multiplying the object's value with it's notation's value.

        :returns: the real value of the object
        :rtype: float
        """
        if self.notation:
            return self.value * self._allowed_notations[self.notation]
        return self.value

    def get_equivalent_worth(self):
        """
        Function for getting the inflation-corrected value.

        :returns: the base value adjusted for inflation
        :rtype: float
        """
        try:
            if self.use_local_data:
                recording_cpi = self.parser.get_cpi_from_csv(self.recording_year, _country=self.local_country)
                recording_cpi = float(recording_cpi)
            else:
                recording_cpi = self.parser.get_cpi(self.recording_year)

            try:
                if self.use_local_data:
                    target_cpi = self.parser.get_cpi_from_csv(self.target_date, _country=self.local_country)
                    target_cpi = float(target_cpi)
                else:
                    target_cpi = self.parser.get_cpi(self.target_date)
            except AttributeError:
                warnings.warn("No target date specified. Did you forget to call \'set_target_year(year_str)\'?", RuntimeWarning)
                return None

            return ((self.value * target_cpi)/recording_cpi)
        except AttributeError:
            warnings.warn("No parser assigned. Did you forget to call \'set_parser(...)\'?", RuntimeWarning)
            return None

    def get_purchasing_power(self):
        """
        Function for getting the purchasing power of a value.

        :returns: the base value's remaining purchasing power
        :rtype: float
        """
        try:
            if self.use_local_data:
                recording_cpi = self.parser.get_cpi_from_csv(self.recording_year, _country=self.local_country)
            else:
                recording_cpi = self.parser.get_cpi(self.recording_year)

            try:
                if self.use_local_data:
                    target_cpi = self.parser.get_cpi_from_csv(self.target_date, _country=self.local_country)
                else:
                    target_cpi = self.parser.get_cpi(self.target_date)
            except AttributeError:
                warnings.warn("No target date specified. Did you forget to call \'set_target_year(year_str)\'?", RuntimeWarning)
                return None

            return (recording_cpi/target_cpi)*self.value
        except AttributeError:
            warnings.warn("No parser assigned. Did you forget to call \'set_parser(...)\'?", RuntimeWarning)
            return None

    def get_exchanged_value(self, currency_iso=None):
        """
        Function for calculating the worth of the current currency in another country.
        The resulting value indicates how much it would take of the target countrie's currency to match the value of the object's value.

        :returns: the exchanged value of the current object (CURRENT/TARGET)
        :rtype: float
        """
        exchange_year = self.recording_year

        iso = currency_iso
        if iso == None:
            if self.target_currency == None:
                warnings.warn("Target currency was not set. Either pass an iso code to get_exchanged_value(currency_iso) or set a target currency using set_target_currency(iso_code).", RuntimeWarning)
                return None
            else:
                iso = self.target_currency

        if iso.upper() not in utils.IMF_SUPPORTED_GEO:
            warnings.warn("ISO code {iso} not supported. Did you you check spelling?".format(iso=iso), RuntimeWarning)
            return None

        if self.use_local_data:
            self_exchange_rate = self.parser.get_exchange_rate_from_csv(exchange_year, _country=self.local_country)
            other_exchange_rate = self.parser.get_exchange_rate_from_csv(exchange_year, _country=self.local_country, _iso=iso)
        else:
            self_exchange_rate = self.parser.get_exchange_rate(exchange_year)
            other_exchange_rate = self.parser.get_exchange_rate(exchange_year, _iso=iso)

        target_value = (other_exchange_rate/self_exchange_rate)*self.value
        return target_value
        