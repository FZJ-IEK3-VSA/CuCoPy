import urllib.request, json

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

IMF_DATASET_IDS = {'national_currency_per_sdr_eop':'ENSE_XDC_XDR_RATE', 'national_currency_per_sdr_aop':'ENSA_XDC_XDR_RATE'}
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


def get_wb_dataset(id : str, date : str, iso : str = 'all', format='json', download_as=None):
    dataset_url = get_wb_dataset_url(id=id, date=date, iso=iso, format=format, download_as=download_as)
    with urllib.request.urlopen(dataset_url) as url:
        data = json.loads(url.read().decode())
    return data

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
    return data['CompactData']['DataSet']

def get_imf_dataset_url(date : str, geo_code : str, indicator : str = 'ENSA_XDC_XDR_RATE'):
    if geo_code not in IMF_SUPPORTED_GEO:
        raise ValueError("Invalid geographical area code: {code}".format(code=geo_code))

    url = IMF_BASE_URL+"/A.{ref_area}.{indicator}?startPeriod={date1}&endPeriod={date2}".format(ref_area=geo_code,indicator=indicator, date1=date, date2=date)
    return url

