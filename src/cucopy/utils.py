import pathlib
import yaml
import sdmx
import logging
import numpy as np
from joblib import Memory
from datetime import datetime

# Alle SDMX-Warnungen komplett stummschalten
logging.getLogger("sdmx").setLevel(logging.ERROR)

module_dir = pathlib.Path(__file__).parent
cache_path = module_dir / "cucopy_cache" # Cache within CuCoPy directory
memory = Memory(cache_path, verbose=0)

IMF_DATA = sdmx.Client('IMF_DATA')

IMF_DATASET_IDS = {'er_avg_sdr': ('ER', 'XDR_XDC.PA_RT'), # average of period, SDR per domestic currency
                   'er_avg_usd': ('ER', 'USD_XDC.PA_RT'), # average of period, USD per domestic currency
                   'cpi' : ('CPI', 'CPI._T.SRP_IX'), # consumer price index (CPI) for "All Items" using "Standard reference period (2010=100), Index"
                   'cpi_harmonised': ('CPI', 'HICP._T.SRP_IX')}

with open(module_dir / "data/currency_iso_map.yaml", encoding="utf-8") as f:
    CURRENCY_TO_COUNTRY_ISO_CODE_MAP = yaml.safe_load(f)


def map_currency_to_country_iso(currency_code):
    try:        
        country = CURRENCY_TO_COUNTRY_ISO_CODE_MAP[currency_code]
        return country
    except KeyError as exc:
        raise ValueError(f"Invalid or not implemented currency code: {currency_code}. Please contact the developers.") from exc


def get_single_imf_datapoint(dataset_id : str, currency : str, year : str, ignore_cache: bool = False, frequency: str='M') -> float:
    iso = map_currency_to_country_iso(currency)
    
    current_year = str(datetime.now().year)    
    if year == current_year:
        ignore_cache = True
        if frequency == 'A':
            # For current year, annual data not available, use monthly.
            print(f"Warning: Current year {current_year} requested with annual frequency. Using monthly frequency instead.")
            frequency = 'M'        

    if ignore_cache:
        # If current year is requested or cache should be ignored, always get fresh data.
        # We ignore the cache for current year, as the data is updated during the year.
        return get_imf_value_uncached(
            indicator=dataset_id, date=year, iso=iso, frequency=frequency
        )
    else:
        return get_imf_value_cached(
            indicator=dataset_id, date=year, iso=iso, frequency=frequency
        )


@memory.cache
def get_imf_value_cached(date: str, iso: str, indicator: tuple, frequency='M'):    
    return get_imf_value_uncached(date, iso, indicator, frequency=frequency)

def get_imf_value_uncached(date: str, iso: str, indicator: tuple, frequency='M'):
    key = f"{iso}.{indicator[1]}.{frequency}"
    try:
        data = IMF_DATA.data(indicator[0], key=key, params={'startPeriod': date, 'endPeriod': date})
        df = sdmx.to_pandas(data)
        values = df.values    
        return np.mean(values)    
    except:
        raise ValueError(f"Could not get IMF data point for indicator {indicator[0]}.{key} for year {date}.")

    