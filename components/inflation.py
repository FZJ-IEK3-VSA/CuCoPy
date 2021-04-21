import pandas as pd
import pathlib, datetime

def __getAvgCPI__(country : str, year):
    global legacy_path
    legacy_path = pathlib.Path(__file__).parent.absolute().joinpath("../data/legacy/legacy_cpi_all.csv")

    cpi = pd.read_csv(legacy_path)

    return cpi.loc[cpi['Currency Code'] == country][str(year)].values[0]

def __deflate__(amount, country, fromDate, toDate=None):
    print(amount, country, fromDate)
    if toDate == None:
        cD = datetime.datetime.now()
        toDate = str(str(cD.year) + "-" + str(cD.month) + "-" + str(cD.day))

    if "-" in fromDate:
        initialYear = int(fromDate.split("-")[0])
    else:
        initialYear = int(fromDate)

    if "-" in toDate:
        currentYear = int(toDate.split("-")[0])
    else:
        currentYear = int(toDate)

    finalCPI = float(__getAvgCPI__(country, currentYear))
    initialCPI = float(__getAvgCPI__(country, initialYear))

    adjustedAmount = (finalCPI/initialCPI) * amount

    return adjustedAmount

def deflateCurrency(amount, country, fromDate, toDate=None):
    if amount == None or fromDate == None:
        return None

    if type(amount) is list:
        res = []
        for i in amount:
            res.append(__deflate__(i, country, fromDate, toDate))
        return res
    else:
        try:
            amount = float(amount)
            return __deflate__(amount, country, fromDate, toDate)
        except Exception:
            print()