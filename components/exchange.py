import pandas as pd
import pathlib

def getHistoricalRate(base=None, targetBase=None, fromDate=None, toDate=None, ):
    print(base, targetBase, fromDate, toDate)

    global legacy_path
    legacy_path = pathlib.Path(__file__).parent.absolute().joinpath("../data/legacy/legacy_fcrf.csv")

    df_currency = pd.read_csv(legacy_path)

    if not base == None and not targetBase == None and not fromDate == None and toDate == None:
        normalizedTargetValue(base, targetBase, fromDate)

    if not base == None and not targetBase == None and not fromDate == None and not toDate == None:
        normalizedTargetSpan(base, targetBase, fromDate, toDate)


def normalizedTargetValue(base=None, targetBase=None, fromDate=None):
    if base == None or targetBase == None or fromDate == None:
        raise Exception()

    fromYear = fromDate.split("-")[0]


    df_currency = pd.read_csv(legacy_path)
    df_baseRow = df_currency.loc[df_currency["Currency Code"] == base]
    df_targetRow = df_currency.loc[df_currency["Currency Code"] == targetBase]


    baseValue = df_baseRow[fromYear].values[0]
    normalizedTargetValue = df_targetRow[fromYear].values[0] / baseValue

    return normalizedTargetValue

def normalizedTargetSpan(base=None, targetBase=None, fromDate=None, toDate=None):
    if base == None or targetBase == None or fromDate == None or toDate == None:
        raise Exception()

    fromYear = int(fromDate.split("-")[0])
    toYear = int(toDate.split("-")[0])

    annualNormalizedValues = []

    for i in range(fromYear, (toYear+1)):
        annualNormalizedValues.append(normalizedTargetValue(base, targetBase, str(i)))

    print(annualNormalizedValues)
    
    '''
    prefix = getDateQualifier(fromDate, toDate)
    
    if not base == None:
        try:
            suffix = getBaseQualifier(base, targetBase)
        except AttributeError as ae:
            if "target" in str(ae) and isValidDate(targetBase):
                return getHistoricalRate(base, None, targetBase, fromDate)
            else:
                if isValidDate(base):
                    prefix = getDateQualifier(base, targetBase)
                    suffix = ''
        if "history?" in prefix:
            suffix = suffix.replace("?", "&", 1)
    else:
        suffix = ''

    url = url.format(prefix = prefix, suffix = suffix)
    
    return requests.get(url).content
    '''


def getBaseQualifier(base, targetBase=None):
    qualifier = "?base={pBase}{oBase}"

    if not isValidBase(base):
        raise AttributeError("Invalid base.")
    tBase = base.upper()

    if not targetBase == None:
        if not isValidBase(targetBase):
            raise AttributeError("Invalid target base. If you want to specify a date, use getHistoricalRate([base], None, [date1], [date2])")
        toBase="&symbols="+targetBase.upper()
    else:
        toBase=""
    
    qualifier = qualifier.format(pBase = tBase, oBase = toBase)
    return qualifier

def getDateQualifier(fromDate=None, toDate=None):
    if not fromDate == None:
        if not isValidDate(fromDate):
            raise Exception("Invalid date.")

        if not toDate == None:
            if not isValidDate(toDate):
                raise Exception("Invalid date.")
            date = "history?start_at={date1}&end_at={date2}".format(date1 = fromDate, date2 = toDate)
        else:
            date = fromDate
    else:
        date = "latest"
    return date