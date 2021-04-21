import pandas as pd
import pathlib

def getHistoricalRate(base=None, targetBase=None, fromDate=None, toDate=None, ):
    print(base, targetBase, fromDate, toDate)

    global legacy_path
    legacy_path = pathlib.Path(__file__).parent.absolute().joinpath("../data/legacy/legacy_fcrf.csv")

    df_currency = pd.read_csv(legacy_path)

    if not base == None and not targetBase == None and not fromDate == None and toDate == None:
        return normalizedTargetValue(base, targetBase, fromDate)

    if not base == None and not targetBase == None and not fromDate == None and not toDate == None:
        return normalizedTargetSpan(base, targetBase, fromDate, toDate)


def normalizedTargetValue(base=None, targetBase=None, fromDate=None):
    if base == None or targetBase == None or fromDate == None:
        raise Exception()

    if "-" in fromDate:
        fromYear = fromDate.split("-")[0]
    else:
        fromYear = fromDate

    df_currency = pd.read_csv(legacy_path)
    df_baseRow = df_currency.loc[df_currency["Currency Code"] == base]
    df_targetRow = df_currency.loc[df_currency["Currency Code"] == targetBase]

    baseValue = df_baseRow[fromYear].values[0]
    normalizedTargetValue = df_targetRow[fromYear].values[0] / baseValue

    return normalizedTargetValue

def normalizedTargetSpan(base=None, targetBase=None, fromDate=None, toDate=None):
    if base == None or targetBase == None or fromDate == None or toDate == None:
        raise Exception()

    if "-" in fromDate:
        fromYear = int(fromDate.split("-")[0])
    else:
        fromYear = int(fromDate)

    if "-" in toDate:
        toYear = int(toDate.split("-")[0])
    else:
        toYear = int(toDate)

    annualNormalizedValues = []

    for i in range(fromYear, (toYear+1)):
        annualNormalizedValues.append(normalizedTargetValue(base, targetBase, str(i)))
    
    return annualNormalizedValues