import urllib.request
import json
import requests
import xml.etree.ElementTree as ET

IMF_BASE_URL = "http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS"
IMF_CODELIST_URL = "https://sdmxcentral.imf.org/sdmx/v2/structure/codelist/IAEG-SDGs/CL_AREA/1.17"

IMF_DATASET_IDS = {'national_currency_per_sdr_eop': 'ENSE_XDC_XDR_RATE',
                   'national_currency_per_sdr_aop': 'ENSA_XDC_XDR_RATE',
                   'cpi' : 'PCPI_IX'}


ISO_COUNTRY_MAP = { 'AF': 'afghanistan', 'AL': 'albania', 'DZ': 'algeria', 'AS': 'american samoa', 'AD': 'andorra',
                    'AO': 'angola', 'AI': 'anguilla', 'AQ': 'antarctica', 'AG': 'antigua and barbuda', 'AR': 'argentina',
                    'AM': 'armenia', 'AW': 'aruba', 'AU': 'australia', 'AT': 'austria', 'AZ': 'azerbaijan', 'BS': 'bahamas',
                    'BH': 'bahrain', 'BD': 'bangladesh', 'BB': 'barbados', 'BY': 'belarus', 'BE': 'belgium', 'BZ': 'belize',
                    'BJ': 'benin', 'BM': 'bermuda', 'BT': 'bhutan', 'BO': 'bolivia (plurinational state of)', 'BQ': 'bonaire, sint eustatius and saba', 
                    'BA': 'bosnia and herzegovina', 'BW': 'botswana', 'BV': 'bouvet island', 'BR': 'brazil', 'IO': 'british indian ocean territory', 
                    'BN': 'brunei darussalam', 'BG': 'bulgaria', 'BF': 'burkina faso', 'BI': 'burundi', 'CV': 'cabo verde', 'KH': 'cambodia', 
                    'CM': 'cameroon', 'CA': 'canada', 'KY': 'cayman islands', 'CF': 'central african republic', 'TD': 'chad', 'CL': 'chile', 
                    'CN': 'china', 'CX': 'christmas island', 'CC': 'cocos (keeling) islands', 'CO': 'colombia', 'KM': 'comoros', 
                    'CD': 'democratic republic of the congo', 'CG': 'congo', 'CK': 'cook islands', 'CR': 'costa rica', 'HR': 'croatia', 
                    'CU': 'cuba', 'CW': 'curaçao', 'CY': 'cyprus', 'CZ': 'czechia', 'CI': "côte d'ivoire", 'DK': 'denmark', 'DJ': 'djibouti', 
                    'DM': 'dominica', 'DO': 'dominican republic', 'EC': 'ecuador', 'EG': 'egypt', 'SV': 'el salvador', 'GQ': 'equatorial guinea', 
                    'ER': 'eritrea', 'EE': 'estonia', 'SZ': 'eswatini', 'ET': 'ethiopia', 'FK': 'falkland islands (malvinas)', 'FO': 'faroe islands', 
                    'FJ': 'fiji', 'FI': 'finland', 'FR': 'france', 'GF': 'french guiana', 'PF': 'french polynesia', 'TF': 'french southern territories', 
                    'GA': 'gabon', 'GM': 'gambia', 'GE': 'georgia', 'DE': 'germany', 'GH': 'ghana', 'GI': 'gibraltar', 'GR': 'greece', 'GL': 'greenland', 
                    'GD': 'grenada', 'GP': 'guadeloupe', 'GU': 'guam', 'GT': 'guatemala', 'GG': 'guernsey', 'GN': 'guinea', 'GW': 'guinea-bissau',
                    'GY': 'guyana', 'HT': 'haiti', 'HM': 'heard island and mcdonald islands', 'VA': 'holy see', 'HN': 'honduras', 'HK': 'hong kong', 
                    'HU': 'hungary', 'IS': 'iceland', 'IN': 'india', 'ID': 'indonesia', 'IR': 'iran (islamic republic of)', 'IQ': 'iraq', 'IE': 'ireland', 
                    'IM': 'isle of man', 'IL': 'israel', 'IT': 'italy', 'JM': 'jamaica', 'JP': 'japan', 'JE': 'jersey', 'JO': 'jordan', 'KZ': 'kazakhstan', 
                    'KE': 'kenya', 'KI': 'kiribati', 'KP': "democratic people's republic of korea", 'KR': 'republic of korea', 'KW': 'kuwait', 
                    'KG': 'kyrgyzstan', 'LA': "lao people's democratic republic", 'LV': 'latvia', 'LB': 'lebanon', 'LS': 'lesotho', 
                    'LR': 'liberia', 'LY': 'libya', 'LI': 'liechtenstein', 'LT': 'lithuania', 'LU': 'luxembourg', 'MO': 'macao', 
                    'MG': 'madagascar', 'MW': 'malawi', 'MY': 'malaysia', 'MV': 'maldives', 'ML': 'mali', 'MT': 'malta', 'MH': 'marshall islands', 
                    'MQ': 'martinique', 'MR': 'mauritania', 'MU': 'mauritius', 'YT': 'mayotte', 'MX': 'mexico', 'FM': 'micronesia', 
                    'MD': 'republic of moldova', 'MC': 'monaco', 'MN': 'mongolia', 'ME': 'montenegro', 'MS': 'montserrat', 'MA': 'morocco', 
                    'MZ': 'mozambique', 'MM': 'myanmar', 'NA': 'namibia', 'NR': 'nauru', 'NP': 'nepal', 'NL': 'netherlands', 
                    'NC': 'new caledonia', 'NZ': 'new zealand', 'NI': 'nicaragua', 'NE': 'niger', 'NG': 'nigeria', 'NU': 'niue', 
                    'NF': 'norfolk island', 'MP': 'northern mariana islands', 'NO': 'norway', 'OM': 'oman', 'PK': 'pakistan', 
                    'PW': 'palau', 'PS': 'state of palestine', 'PA': 'panama', 'PG': 'papua new guinea', 'PY': 'paraguay', 'PE': 'peru', 
                    'PH': 'philippines', 'PN': 'pitcairn', 'PL': 'poland', 'PT': 'portugal', 'PR': 'puerto rico', 'QA': 'qatar', 
                    'MK': 'republic of north macedonia', 'RO': 'romania', 'RU': 'russian federation', 'RW': 'rwanda', 'RE': 'réunion', 
                    'BL': 'saint barthélemy', 'SH': 'saint helena', 'KN': 'saint kitts and nevis', 'LC': 'saint lucia', 
                    'MF': 'saint martin (french part)', 'PM': 'saint pierre and miquelon', 'VC': 'saint vincent and the grenadines', 
                    'WS': 'samoa', 'SM': 'san marino', 'ST': 'sao tome and principe', 'SA': 'saudi arabia', 'SN': 'senegal', 'RS': 'serbia', 
                    'SC': 'seychelles', 'SL': 'sierra leone', 'SG': 'singapore', 'SX': 'sint maarten (dutch part)', 'SK': 'slovakia', 'SI': 'slovenia', 
                    'SB': 'solomon islands', 'SO': 'somalia', 'ZA': 'south africa', 'GS': 'south georgia and the south sandwich islands', 
                    'SS': 'south sudan', 'ES': 'spain', 'LK': 'sri lanka', 'SD': 'sudan', 'SR': 'suriname', 'SJ': 'svalbard and jan mayen', 
                    'SE': 'sweden', 'CH': 'switzerland', 'SY': 'syrian arab republic', 'TW': 'taiwan', 'TJ': 'tajikistan', 
                    'TZ': 'tanzania, united republic of', 'TH': 'thailand', 'TL': 'timor-leste', 'TG': 'togo', 'TK': 'tokelau', 'TO': 'tonga', 
                    'TT': 'trinidad and tobago', 'TN': 'tunisia', 'TR': 'turkey', 'TM': 'turkmenistan', 'TC': 'turks and caicos islands', 
                    'TV': 'tuvalu', 'UG': 'uganda', 'UA': 'ukraine', 'AE': 'united arab emirates', 'GB': 'united kingdom of great britain and northern ireland', 
                    'UM': 'united states minor outlying islands', 'US': 'united states of america', 'UY': 'uruguay', 'UZ': 'uzbekistan', 'VU': 'vanuatu', 
                    'VE': 'venezuela', 'VN': 'viet nam', 'VG': 'british virgin islands', 'VI': 'united states virgin islands', 'WF': 'wallis and futuna',
                    'EH': 'western sahara', 'YE': 'yemen', 'ZM': 'zambia', 'ZW': 'zimbabwe', 'AX': 'åland islands'
}

def map_iso_to_country_name(iso: str):
    try:
        return ISO_COUNTRY_MAP[iso.upper()]
    except KeyError as exc:
        raise ValueError(f"Invalid ISO code: {iso}") from exc

def get_letter_id_by_name(name: str):
    res = requests.get(IMF_CODELIST_URL, timeout=60)

    if res.status_code != 200:
        raise ValueError(f"Failed to fetch data from {IMF_CODELIST_URL}")

    xml_content = res.content
    tree = ET.ElementTree(ET.fromstring(xml_content))

    namespaces = {
        'message': 'http://www.sdmx.org/resources/sdmxml/schemas/v3_0/message',
        'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v3_0/structure',
        'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v3_0/common'
    }

    codes = tree.findall('.//str:Code', namespaces)

    for code in codes:
        code_id = code.attrib['id']
        try:
            int(code_id)
            continue
        except:
            pass

        name_element = code.find('com:Name', namespaces)

        if name_element is not None and name_element.text.lower() == name.lower():
            return code_id

    raise ValueError(f"Failed to find code for {name}")

def get_single_imf_datapoint(dataset_id : str, country : str, year : str, frequency='A'):
    data = get_imf_dataset(
        indicator=dataset_id, date=year, country=country, frequency=frequency
    )

    return data['Series']['Obs']['@OBS_VALUE']

def get_imf_dataset(date: str, country: str, indicator: str = 'ENSA_XDC_XDR_RATE', frequency='A'):
    dataset_url = get_imf_dataset_url(
        date=date, country=country, indicator=indicator, frequency=frequency)
        
    with urllib.request.urlopen(dataset_url) as url:
        data = json.loads(url.read().decode())
    return data['CompactData']['DataSet']


def get_imf_dataset_url(date: str, country: str, indicator: str, frequency: str):
    iso_alpha2 = get_letter_id_by_name(country)
    url = IMF_BASE_URL+"/{frequency}.{ref_area}.{indicator}?startPeriod={date1}&endPeriod={date2}".format(
        frequency=frequency, ref_area=iso_alpha2, indicator=indicator, date1=date, date2=date)
    return url
