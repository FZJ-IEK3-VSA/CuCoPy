import pytest
from cucopy import Currency

cur = Currency(ignore_cache=True, normalize_to="USD", aggregate_from="A")

CPI_DATA = {
    "EUR": {
        "2016": 1.076224477013655, "2017": 1.092777509350227, "2018": 1.11195218410551, "2019": 1.125248295485049,
        "2020": 1.128084679944883, "2021": 1.157280649952578, "2022": 1.254308262200033, "2023": 1.322318856140729, "2024": 1.353581718294234
    },
    "USD": {
        "2016": 1.100670089342698, "2017": 1.124115573023076, "2018": 1.151573032247906, "2019": 1.172441954762282,
        "2020": 1.186905015771978, "2021": 1.242664138258379, "2022": 1.342112061684602, "2023": 1.397357935632595, "2024": 1.438573360146079
    },
    "JPY": {
        "2016": 1.034628229917384, "2017": 1.03963789769731, "2018": 1.049920899982422, "2019": 1.054842678853929,
        "2020": 1.054579012128669, "2021": 1.052118122692916, "2022": 1.078396906310424, "2023": 1.113640358586746, "2024": 1.144137809808403
    }
}

# Reference values from https://data.imf.org/en/Data-Explorer?datasetUrn=IMF.STA:ER(4.0.1) (annual averages)
ER_DATA = {
    "USD_per_EUR": {
        "2016": 1.1069031128405, "2017": 1.1296811764706, "2018": 1.1809545098039, "2019": 1.1194745098039,
        "2020": 1.1421961089494, "2021": 1.1827403100775,"2022": 1.0530486381323, "2023": 1.081268627451, "2024": 1.08238046875
    },
    "JPY_per_EUR": {
        "2016": 120.4231997167862, "2017": 126.7119782175355, "2018": 130.4047516297099, "2019": 122.0335422982557,
        "2020": 121.9575123948534, "2021": 129.8108630101786, "2022": 138.4739377112355, "2023": 151.9086189334877, "2024": 163.8359173332215
    }
}

def test_get_inflation_value():
    for year, equivalent_worth in CPI_DATA['EUR'].items():
        adj_value = cur.convert_currency(value=1, base_year="2010", base_currency="EUR", target_year=year, target_currency="EUR")
        print(f"Year: {year}, adjusted value: {adj_value}, expected value: {equivalent_worth}")
        assert round(adj_value, 6) == round(equivalent_worth, 6)
    
    for year, equivalent_worth in CPI_DATA['USD'].items():
        adj_value = cur.convert_currency(value=1, base_year="2010", base_currency="USD", target_year=year, target_currency="USD")
        print(f"Year: {year}, adjusted value: {adj_value}, expected value: {equivalent_worth}")
        assert round(adj_value, 6) == round(equivalent_worth, 6)

    for year, equivalent_worth in CPI_DATA['JPY'].items():
        adj_value = cur.convert_currency(value=1, base_year="2010", base_currency="JPY", target_year=year, target_currency="JPY")
        print(f"Year: {year}, adjusted value: {adj_value}, expected value: {equivalent_worth}")
        assert round(adj_value, 6) == round(equivalent_worth, 6)


def test_get_exchanged_value():
    for year, equivalent_worth in ER_DATA['USD_per_EUR'].items():
        adj_value = cur.convert_currency(value=1, base_year=year, base_currency="EUR", target_year=year, target_currency="USD")
        print(f"Year: {year}, adjusted value: {adj_value}, expected value: {equivalent_worth}")
        assert round(adj_value, 6) == round(equivalent_worth, 6)

    for year, equivalent_worth in ER_DATA['JPY_per_EUR'].items():
        adj_value = cur.convert_currency(value=1, base_year=year, base_currency="EUR", target_year=year, target_currency="JPY")
        print(f"Year: {year}, adjusted value: {adj_value}, expected value: {equivalent_worth}")
        assert round(adj_value, 6) == round(equivalent_worth, 6)


def test_get_combined_value():
    """
    Test combined inflation (EUR) + exchange rate (EUR→USD, EUR→JPY).
    Erwartung: 1 EUR (2010) in USD oder JPY (target_year)
    """

    for target_year in CPI_DATA['EUR'].keys():
        # Schritt 1: Inflation in EUR
        eur_inflated = CPI_DATA['EUR'][target_year]

        # Schritt 2: Wechselkurs für dieses Jahr
        eur_to_usd = ER_DATA['USD_per_EUR'][target_year]
        eur_to_jpy = ER_DATA['JPY_per_EUR'][target_year]

        # Erwartungswert = Inflation * Wechselkurs
        expected_usd = eur_inflated * eur_to_usd
        expected_jpy = eur_inflated * eur_to_jpy

        # Tatsächlicher Wert über Currency
        converted_usd = cur.convert_currency(value=1, base_year="2010", base_currency="EUR", target_year=target_year, target_currency="USD")

        converted_jpy = cur.convert_currency(value=1, base_year="2010", base_currency="EUR", target_year=target_year, target_currency="JPY")

        print(f"\n{target_year}:")
        print(f"  EUR→USD expected: {expected_usd:.6f}, got: {converted_usd:.6f}")
        print(f"  EUR→JPY expected: {expected_jpy:.6f}, got: {converted_jpy:.6f}")

        # Test mit kleiner Toleranz (Rundungsfehler/IMF Glättung)
        assert round(converted_usd, 6) == round(expected_usd, 6)
        assert round(converted_jpy, 6) == round(expected_jpy, 6)

if __name__ == "__main__":    
    print("------------ TEST INFLATION ------------")
    test_get_inflation_value()
    print("------------ TEST Exchange Rate ------------")
    test_get_exchanged_value()
    print("------------ TEST Inflation + ER ------------")
    test_get_combined_value()
    print("All tests passed.")
