import urllib.request, json
import datetime
from dateutil.relativedelta import relativedelta

WB_BASE_URL = "http://api.worldbank.org/v2/country"
IMF_BASE_URL = "http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS"

OUTPUT_FORMATS = ('xml','json')
DOWNLOAD_FORMATS = ('csv','xml','json')

WB_DATASET_IDS = {'cpi' : 'FP.CPI.TOTL', 'ppp' : 'PA.NUS.PPP', 'fcrf' : 'PA.NUS.FCRF'}
WB_SUPPORTED_ISO = ('AW','ZH','AF','A9','ZI','AO','AL','AD','1A','AE','AR','AM','AS','AG','AU','AT','AZ','BI','B4','B7','BE','BJ','BF','BD','BG',
                'B1','BH','BS','BA','B2','BY','BZ','B3','BM','BO','BR','BB','BN','B6','BT','BW','C9','CF','CA','C4','B8','C5','CH','JG','CL',
                'CN','CI','C6','C7','CM','CD','CG','CO','KM','CV','CR','C8','S3','CU','CW','KY','CY','CZ','D4','D7','DE','D8','DJ','D2','DM',
                'D3','D9','DK','N6','DO','D5','F6','D6','DZ','4E','V2','Z4','7E','Z7','EC','EG','XC','ER','ES','EE','ET','EU','F1','FI','FJ',
                'FR','FO','FM','6F','GA','GB','GE','GH','GI','GN','GM','GW','GQ','GR','GD','GL','GT','GU','GY','XD','HK','HN','XE','HR','HT',
                'HU','ZB','XF','ZT','XG','XH','ID','XI','IM','IN','XY','IE','IR','IQ','IS','IL','IT','JM','JO','JP','KZ','KE','KG','KH','KI',
                'KN','KR','KW','XJ','LA','LB','LR','LY','LC','ZJ','XL','XM','LI','LK','XN','XO','LS','V3','LT','LU','LV','MO','MF','MA','MC',
                'MD','M1','MG','MV','ZQ','MX','MH','XP','MK','ML','MT','MM','XQ','ME','MN','MP','MZ','MR','MU','MW','MY','XU','M2','NA','NC',
                'NE','NG','NI','NL','NO','NP','6X','NR','6N','NZ','OE','OM','S4','PK','PA','PE','PH','PW','PG','PL','V1','PR','KP','PT','PY',
                'PS','S2','V4','PF','QA','RO','R6','RU','RW','8S','SA','SD','SN','SG','SB','SL','SV','SM','SO','RS','ZF','SS','ZG','S1','ST',
                'SR','SK','SI','SE','SZ','SX','A4','SC','SY','TC','TD','T4','T7','TG','TH','TJ','TM','T2','TL','T3','TO','T5','T6','TT','TN',
                'TR','TV','TW','TZ','UG','UA','XT','UY','US','UZ','VC','VE','VG','VI','VN','VU','1W','WS','XK','A5','YE','ZA','ZM','ZW')

IMF_DATASET_IDS = {'national_currency_per_sdr_eop':'ENSE_XDC_XDR_RATE', 'national_currency_per_sdr_aop':'ENSA_XDC_XDR_RATE', 'real_effective_exchange_rate_b_cpi':'EREER_IX'}
IMF_SUPPORTED_GEO = ('AF','AL','DZ','AD','AO','AI','AG','5M','AR','AM','AW','AU','AT','AZ','BS','BH','BD','5W','5B','BB','BY','BE','R1','BZ',
                'BJ','BM','BT','BO','BA','BW','BR','BN','BG','BF','BI','CV','KH','CM','CA','KY','CF','1C_752','TD','CL','HK','MO','CN','CO',
                'KM','CD','CG','CR','CI','HR','CU','1C_355','CW','CY','CZ','CSH','DK','DJ','DM','DO','5I','DE2','EC','EG','SV','GQ','ER','EE',
                'SZ','ET','U2','4F','FO','FJ','FI','FR','PF','GA','GM','GE','DE','GH','GI','GR','GL','GD','GP','GU','GT','GG','GF','GN','GW',
                'GY','HT','HN','HU','IS','IN','ID','1E','X0','IR','IQ','IE','7B','IM','IL','IT','JM','JP','JE','JO','KZ','KE','KI','KR','XK',
                'KW','KG','LA','LV','LB','LS','LR','LY','LT','LU','MG','MW','MY','MV','ML','MT','MH','MQ','MR','MU','MX','FM','MD','MN','ME',
                'MS','MA','MZ','MM','NA','NR','NP','AN','NL','NC','NZ','NI','NE','NG','MK','NO','OM','PK','PW','PA','PG','PY','PE','PH','PL',
                'PT','QA','RE','RO','RU','RW','PM','WS','SM','ST','SA','SN','RS','SC','SL','SG','SX','SK','SI','SB','SO','ZA','SS','ES','LK',
                'KN','LC','VC','SD','SR','SE','CH','SY','TW','TJ','TZ','TH','TL','TG','TO','TT','TN','TR','TM','TC','TV','UG','UA','AE','GB',
                'US','UY','SUH','UZ','VU','VE','VN','PS','1C_473','1C_459','YE','YUC','ZM','ZW','XR29','F1','F19','1C_ALLC','1C_ALL','W0',
                '1C_All_Countries_Published','1C_ALLG','R16','5O','5X','1C_904','R14','Countries_Home_Portal_Presentation','F3','5Y','XS25',
                'XR43','1C_903','1C_994','1C_EMU','E1','1C_080','1C_092','F97','F98','1C_Middle_East_and_Central_Asia','1C_440','1C_NANSA',
                '1C_NASA','XR44','1C_NSC','XR21','XA69','1C_970','1C_SRF_less_EMU','1C_SRF_plus_EMU','1C_SRF','F6','7A','A10','W00')

IMF_REF_TO_COUNTRY_NAME = {
                "AW":"Aruba", "AF":"Afghanistan", "AO":"Angola", "AI":"Anguilla", "AL":"Albania", "AD":"Andorra", "AN":"Netherlands Antilles", "AE":"United Arab Emirates", 
                "AR":"Argentina", "AM":"Armenia", "AS":"American Samoa", "AG":"Antigua and Barbuda", "AU":"Australia", "AT":"Austria", "AZ":"Azerbaijan", "BI":"Burundi", 
                "BE":"Belgium", "BJ":"Benin", "BF":"Burkina Faso", "BD":"Bangladesh", "BG":"Bulgaria", "BH":"Bahrain", "BS":"Bahamas", "BA":"Bosnia and Herzegovina", 
                "BY":"Belarus", "BZ":"Belize", "BM":"Bermuda", "BO":"Bolivia", "BR":"Brazil", "BB":"Barbados", "BN":"Brunei Darussalam", "BT":"Bhutan", "BW":"Botswana", 
                "CF":"Central African Republic", "CA":"Canada", "CH":"Switzerland", "CL":"Chile", "CN":"China", "CI":"Cote d'Ivoire", "CM":"Cameroon", "CD":"Congo", 
                "CG":"Congo", "CK":"Cook Islands", "CO":"Colombia", "KM":"Comoros", "CV":"Cape Verde", "CR":"Costa Rica", "CU":"Cuba", "KY":"Cayman Islands", "CY":"Cyprus", 
                "CZ":"Czech Republic", "DE":"Germany", "DJ":"Djibouti", "DM":"Dominica", "DK":"Denmark", "DO":"Dominican Republic", "DZ":"Algeria", "EC":"Ecuador", 
                "EG":"Egypt", "ER":"Eritrea", "EH":"Western Sahara", "ES":"Spain", "EE":"Estonia", "ET":"Ethiopia", "FI":"Finland", "FJ":"Fiji", "FK":"Falkland Islands (Malvinas)",
                "FR":"France", "FO":"Faeroe Islands", "GA":"Gabon", "GB":"United Kingdom", "GE":"Georgia", "GG":"Guernsey", "GH":"Ghana", "GI":"Gibraltar", "GN":"Guinea", 
                "GP":"Guadeloupe", "GM":"Gambia", "GW":"Guinea-Bissau", "GQ":"Equatorial Guinea", "GR":"Greece", "GD":"Grenada", "GL":"Greenland", "GT":"Guatemala", 
                "GF":"French Guiana", "GU":"Guam", "GY":"Guyana", "HK":"Hong Kong", "HN":"Honduras", "HR":"Croatia", "HT":"Haiti", "HU":"Hungary", "ID":"Indonesia", 
                "IM":"Isle of Man", "IN":"India", "IE":"Ireland", "IR":"Iran", "IQ":"Iraq", "IS":"Iceland", "IL":"Israel", "IT":"Italy", "JM":"Jamaica", "JE":"Jersey", 
                "JO":"Jordan", "JP":"Japan", "KZ":"Kazakhstan", "KE":"Kenya", "KG":"Kyrgyzstan", "KH":"Cambodia", "KI":"Kiribati", "KN":"Saint Kitts and Nevis", 
                "KR":"Korea", "KW":"Kuwait", "LA":"Lao People's Dem. Rep.", "LB":"Lebanon", "LR":"Liberia", "LY":"Libyan Arab Jamahiriya", "LC":"Saint Lucia", 
                "LI":"Liechtenstein", "LK":"Sri Lanka", "LS":"Lesotho", "LT":"Lithuania", "LU":"Luxembourg", "LV":"Latvia", "MO":"Macau", "MA":"Morocco", "MC":"Monaco",
                "MD":"Moldova", "MG":"Madagascar", "MV":"Maldives", "MX":"Mexico", "MH":"Marshall Islands", "MK":"Macedonia", "ML":"Mali", "MT":"Malta", "MM":"Myanmar",
                "ME":"Montenegro", "MN":"Mongolia", "MP":"Northern Mariana Islands", "MZ":"Mozambique", "MR":"Mauritania", "MS":"Montserrat", "MQ":"Martinique", "MU":"Mauritius",
                "MW":"Malawi", "MY":"Malaysia", "NA":"Namibia", "NC":"New Caledonia", "NE":"Niger", "NF":"Norfolk Island", "NG":"Nigeria", "NI":"Nicaragua", "NU":"Niue", 
                "NL":"Netherlands", "NO":"Norway", "NP":"Nepal", "NR":"Nauru", "NZ":"New Zealand", "OM":"Oman", "PK":"Pakistan", "PA":"Panama", "PE":"Peru", "PH":"Philippines", 
                "PW":"Palau", "PG":"Papua New Guinea", "PL":"Poland", "PR":"Puerto Rico", "KP":"Korea", "PT":"Portugal", "PY":"Paraguay", "PS":"West Bank and Gaza Strip", 
                "PF":"French Polynesia", "QA":"Qatar", "RE":"Reunion", "RO":"Romania", "RU":"Russian Federation", "RW":"Rwanda", "SA":"Saudi Arabia", "SD":"Sudan", "SN":"Senegal", 
                "SG":"Singapore", "SH":"Saint Helena", "SB":"Solomon Islands", "SL":"Sierra Leone", "SV":"El Salvador", "SM":"San Marino", "SO":"Somalia", "PM":"Saint Pierre and Miquelon", 
                "RS":"Serbia", "ST":"Sao Tome and Principe", "SR":"Suriname", "SK":"Slovakia", "SI":"Slovenia", "SE":"Sweden", "SZ":"Swaziland", "SC":"Seychelles", "SY":"Syrian Arab Republic", 
                "TC":"Turks and Caicos Islands", "TD":"Chad", "TG":"Togo", "TH":"Thailand", "TJ":"Tajikistan", "TK":"Tokelau", "TM":"Turkmenistan", "TL":"Timor-Leste", "TO":"Tonga", 
                "TT":"Trinidad and Tobago", "TN":"Tunisia", "TR":"Turkey", "TV":"Tuvalu", "TW":"Taiwan", "TZ":"Tanzania", "UG":"Uganda", "UA":"Ukraine", "UY":"Uruguay", "US":"United States", 
                "UZ":"Uzbekistan", "VC":"Saint Vincent and the Grenadines", "VE":"Venezuela", "VG":"British Virgin Islands", "VI":"Virgin Islands", "VN":"Vietnam", "VU":"Vanuatu", 
                "WF":"Wallis and Futuna Islands", "WS":"Samoa", "YE":"Yemen", "ZA":"South Africa", "ZM":"Zambia", "ZW":"Zimbabwe" }

COUNTRY_TO_ISO3 = {
    "?": "", "africa": "ZAF", "algeria": "DZA", "australia": "AUS", 
    "bangladesh": "BGD", "benin": "BEN", "cameroon": "CMR", "canada": "CAN", 
    "china": "CHN", "colombia": "COL", "croatia": "HRV", "egypt": "EGY", "ethiopia": "ETH", 
    "germany": "DEU", "ghana": "GHA", "greece": "GRC", "hong kong": "HKG", "india": "IND", 
    "indonesia": "IDN", "iran": "IRN", "iraq": "IRQ", "italy": "ITA", "japan": "JPN", "jordan": "JOR", 
    "kenya": "KEN", "malawi": "MWI", "malaysia": "MYS", "maldives": "MDV", "nepal": "NPL", 
    "new zealand": "NZL", "nigeria": "NGA", "no specific country": "", "north korea": "PRK", 
    "oman": "OMN", "pakistan": "PAK", "peru": "PER", "philippines": "PHL", "portugal": "PRT", 
    "republic of korea": "KOR", "rwanda": "RWA", "saudi arabia": "SAU", "scottland": "GBR", 
    "sierra leone": "SLE", "spain": "ESP", "sweden": "SWE", "tanzania": "TZA", "tunisia": "TUN", 
    "turkey": "TUR", "uganda": "UGA", "united arab emirates": "ARE", "yemen": "YEM"
    }

ISO3_TO_IMF_REF = {
    "ABW": "AW", "AFG": "AF", "AGO": "AO", "AIA": "AI", "ALA": "AX",
"ALB": "AL", "AND": "AD", "ANT": "AN", "ARE": "AE", "ARG": "AR", "ARM": "AM",
"ASM": "AS", "ATA": "AQ", "ATF": "TF", "ATG": "AG", "AUS": "AU", "AUT": "AT",
"AZE": "AZ", "BDI": "BI", "BEL": "BE", "BEN": "BJ", "BFA": "BF", "BGD": "BD",
"BGR": "BG", "BHR": "BH", "BHS": "BS", "BIH": "BA", "BLM": "BL", "BLR": "BY",
"BLZ": "BZ", "BMU": "BM", "BOL": "BO", "BRA": "BR", "BRB": "BB", "BRN": "BN",
"BTN": "BT", "BVT": "BV", "BWA": "BW", "CAF": "CF", "CAN": "CA", "CCK": "CC",
"CHE": "CH", "CHL": "CL", "CHN": "CN", "CIV": "CI", "CMR": "CM", "COD": "CD",
"COG": "CG", "COK": "CK", "COL": "CO", "COM": "KM", "CPV": "CV", "CRI": "CR",
"CUB": "CU", "CXR": "CX", "CYM": "KY", "CYP": "CY", "CZE": "CZ", "DEU": "DE",
"DJI": "DJ", "DMA": "DM", "DNK": "DK", "DOM": "DO", "DZA": "DZ", "ECU": "EC",
"EGY": "EG", "ERI": "ER", "ESH": "EH", "ESP": "ES", "EST": "EE", "ETH": "ET",
"FIN": "FI", "FJI": "FJ", "FLK": "FK", "FRA": "FR", "FRO": "FO", "FSM": "FM",
"GAB": "GA", "GBR": "GB", "GEO": "GE", "GGY": "GG", "GHA": "GH", "GIB": "GI",
"GIN": "GN", "GLP": "GP", "GMB": "GM", "GNB": "GW", "GNQ": "GQ", "GRC": "GR",
"GRD": "GD", "GRL": "GL", "GTM": "GT", "GUF": "GF", "GUM": "GU", "GUY": "GY",
"HKG": "HK", "HMD": "HM", "HND": "HN", "HRV": "HR", "HTI": "HT", "HUN": "HU",
"IDN": "ID", "IMN": "IM", "IND": "IN", "IOT": "IO", "IRL": "IE", "IRN": "IR",
"IRQ": "IQ", "ISL": "IS", "ISR": "IL", "ITA": "IT", "JAM": "JM", "JEY": "JE",
"JOR": "JO", "JPN": "JP", "KAZ": "KZ", "KEN": "KE", "KGZ": "KG", "KHM": "KH",
"KIR": "KI", "KNA": "KN", "KOR": "KR", "KWT": "KW", "LAO": "LA", "LBN": "LB",
"LBR": "LR", "LBY": "LY", "LCA": "LC", "LIE": "LI", "LKA": "LK", "LSO": "LS",
"LTU": "LT", "LUX": "LU", "LVA": "LV", "MAC": "MO", "MAF": "MF", "MAR": "MA",
"MCO": "MC", "MDA": "MD", "MDG": "MG", "MDV": "MV", "MEX": "MX", "MHL": "MH",
"MKD": "MK", "MLI": "ML", "MLT": "MT", "MMR": "MM", "MNE": "ME", "MNG": "MN",
"MNP": "MP", "MOZ": "MZ", "MRT": "MR", "MSR": "MS", "MTQ": "MQ", "MUS": "MU",
"MWI": "MW", "MYS": "MY", "MYT": "YT", "NAM": "NA", "NCL": "NC", "NER": "NE",
"NFK": "NF", "NGA": "NG", "NIC": "NI", "NIU": "NU", "NLD": "NL", "NOR": "NO",
"NPL": "NP", "NRU": "NR", "NZL": "NZ", "OMN": "OM", "PAK": "PK", "PAN": "PA",
"PCN": "PN", "PER": "PE", "PHL": "PH", "PLW": "PW", "PNG": "PG", "POL": "PL",
"PRI": "PR", "PRK": "KP", "PRT": "PT", "PRY": "PY", "PSE": "PS", "PYF": "PF",
"QAT": "QA", "REU": "RE", "ROU": "RO", "RUS": "RU", "RWA": "RW", "SAU": "SA",
"SDN": "SD", "SEN": "SN", "SGP": "SG", "SGS": "GS", "SHN": "SH", "SJM": "SJ",
"SLB": "SB", "SLE": "SL", "SLV": "SV", "SMR": "SM", "SOM": "SO", "SPM": "PM",
"SRB": "RS", "STP": "ST", "SUR": "SR", "SVK": "SK", "SVN": "SI", "SWE": "SE",
"SWZ": "SZ", "SYC": "SC", "SYR": "SY", "TCA": "TC", "TCD": "TD", "TGO": "TG",
"THA": "TH", "TJK": "TJ", "TKL": "TK", "TKM": "TM", "TLS": "TL", "TON": "TO",
"TTO": "TT", "TUN": "TN", "TUR": "TR", "TUV": "TV", "TWN": "TW", "TZA": "TZ",
"UGA": "UG", "UKR": "UA", "UMI": "UM", "URY": "UY", "USA": "US", "UZB": "UZ",
"VAT": "VA", "VCT": "VC", "VEN": "VE", "VGB": "VG", "VIR": "VI", "VNM": "VN",
"VUT": "VU", "WLF": "WF", "WSM": "WS", "YEM": "YE", "ZAF": "ZA", "ZMB": "ZM",
"ZWE": "ZW"
}


def get_wb_dataset(id : str, date : str, iso : str = 'all', format='json', download_as=None):
    try:
        if str(date) == '1960':
            return [0, [{'value' : 1}]] 
        dataset_url = get_wb_dataset_url(id=id, date=date, iso=iso, format=format, download_as=download_as)
        with urllib.request.urlopen(dataset_url) as url:
            data = json.loads(url.read().decode())
            print(data)
            if data[1][0]['value'] == None:
                prior_year = datetime.datetime.strptime(str(date), "%Y").date()
                prior_year = (prior_year - relativedelta(years=1)).strftime("%Y")
                data = get_wb_dataset(id=id, date=prior_year, iso=iso, format=format, download_as=download_as)
        return data
    except urllib.error.HTTPError as e:
        print(e)
        return None
    

def get_wb_dataset_url(id : str, date : str, iso : str = 'all', format='json', download_as=None):
    if format not in OUTPUT_FORMATS:
        raise ValueError('Format {format} is not supported. Available output formats are {output_formats}'.format(format=format, output_formats=OUTPUT_FORMATS))

    url = WB_BASE_URL+"/{iso_code}/indicator/{dataset_id}?format={output_format}".format(iso_code=iso, dataset_id=id, output_format=format)

    if date is not None:
        url += "&date={date}".format(date=date)

    if download_as is not None:
        if download_as not in DOWNLOAD_FORMATS:
            raise ValueError('Download format {format} is not supported. Available download formats are {download_formats}'.format(format=download_as, output_formats=DOWNLOAD_FORMATS))
        url += "&source=2&downloadformat={download_format}".format(download_as)
    
    return url

def get_imf_dataset(date : str, geo_code : str, indicator : str = 'ENSA_XDC_XDR_RATE'):
    dataset_url = get_imf_dataset_url(date=date, geo_code=geo_code, indicator=indicator)
    with urllib.request.urlopen(dataset_url) as url:
        data = json.loads(url.read().decode())
        print(data)
    return data['CompactData']['DataSet'], dataset_url

def get_imf_dataset_url(date : str, geo_code : str, indicator : str = 'ENSA_XDC_XDR_RATE'):
    if geo_code not in IMF_SUPPORTED_GEO:
        raise ValueError("Invalid geographical area code: {code}".format(code=geo_code))

    url = IMF_BASE_URL+"/A.{ref_area}.{indicator}?startPeriod={date1}&endPeriod={date2}".format(ref_area=geo_code,indicator=indicator, date1=date, date2=date)
    return url

