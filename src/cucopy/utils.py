import pathlib
import yaml
import sdmx
import logging
import numpy as np
from typing import Annotated, Tuple, Any
from datadesclib import meta
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


@meta(
    semanticConcept="CurrencyToCountryMapping",
    description="Map a currency code to its country's ISO 3166 ALPHA-2 code."
)
def map_currency_to_country_iso(
    currency_code: Annotated[str, {
        "description": "ISO 4217 Currency Code",
        "example": "USD",
        "minLength": 3,
        "maxLength": 3
    }]
) -> Annotated[str, {"description": "ISO 3166 ALPHA-2 Country Code (e.g., 'US')"}]:
    try:        
        country = CURRENCY_TO_COUNTRY_ISO_CODE_MAP[currency_code]
        return country
    except KeyError as exc:
        raise ValueError(f"Invalid or not implemented currency code: {currency_code}. Please contact the developers.") from exc


@meta(
    semanticConcept="IMFDataRetrieval",
    description="Get a single data point from the IMF dataset, handling caching and frequency fallback."
)
def get_single_imf_datapoint(
    dataset_id: Annotated[Tuple[str, str], {
        "description": "Tuple containing IMF Dataflow ID and Data Key",
        "example": ("CPI", "CPI._T.SRP_IX")
    }],
    currency: Annotated[str, {
        "description": "ISO 4217 Currency code",
        "example": "EUR"
    }],
    year: Annotated[str, {
        "description": "Target year for data retrieval",
        "pattern": "^[0-9]{4}$",
        "example": "2023"
    }],
    ignore_cache: Annotated[bool, {
        "description": "Force fresh data retrieval from IMF API",
        "default": False
    }] = False,
    frequency: Annotated[str, {
        "description": "Data frequency",
        "enum": ["A", "M"],
        "note": "'A' for Annual, 'M' for Monthly",
        "default": "M"
    }] = 'M'
) -> Annotated[float, {"description": "The retrieved data value (CPI or Exchange Rate)"}]:
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
        try:
            return get_imf_value_uncached(
                indicator=dataset_id, date=year, iso=iso, frequency=frequency
            )
        except ValueError:
            if frequency != 'M':
                print(f"Warning: No {frequency} data for year {year}. Using monthly frequency instead.")
                return get_imf_value_uncached(
                    indicator=dataset_id, date=year, iso=iso, frequency='M'
                )
            raise
    else:
        try:
            return get_imf_value_cached(
                indicator=dataset_id, date=year, iso=iso, frequency=frequency
            )
        except ValueError:
            if frequency != 'M':
                # If annual data is not available, fall back to monthly data.
                # We ignore the cache here as well, as annual data can be available in the future
                print(f"Warning: No {frequency} data for year {year}. Using monthly frequency instead.")
                return get_imf_value_uncached(
                    indicator=dataset_id, date=year, iso=iso, frequency='M'
                )
            raise

@meta(
    semanticConcept="CachedIMFQuery",
    description="Retrieve IMF value from local cache if available."
)
@memory.cache
def get_imf_value_cached(
    date: Annotated[str, {"description": "Year string"}],
    iso: Annotated[str, {"description": "Country ISO code"}],
    indicator: Annotated[Tuple[str, str], {"description": "IMF Indicator Tuple"}],
    frequency: Annotated[str, {"description": "Data frequency", "enum": ["A", "M"]}] = 'M'
) -> Annotated[float, {"description": "Cached data value"}]:
    return get_imf_value_uncached(date, iso, indicator, frequency=frequency)

@meta(
    semanticConcept="DirectIMFQuery",
    description="Retrieve IMF value directly from the API without using cache."
)
def get_imf_value_uncached(
    date: Annotated[str, {"description": "Year string"}],
    iso: Annotated[str, {"description": "Country ISO code"}],
    indicator: Annotated[Tuple[str, str], {"description": "IMF Indicator Tuple"}],
    frequency: Annotated[str, {"description": "Data frequency", "enum": ["A", "M"]}] = 'M'
) -> Annotated[float, {"description": "Fetched data value"}]:
    key = f"{iso}.{indicator[1]}.{frequency}"
    try:
        data = IMF_DATA.data(indicator[0], key=key, params={'startPeriod': date, 'endPeriod': date})
        df = sdmx.to_pandas(data)
        values = df.values    
        mean_value = np.mean(values)
        if np.isnan(mean_value):
            raise ValueError(f"Could not get IMF data point for indicator {indicator[0]}.{key} for year {date}.")
        return mean_value    
    except:
        raise ValueError(f"Could not get IMF data point for indicator {indicator[0]}.{key} for year {date}.")