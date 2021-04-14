import pandas as pd
import pathlib, datetime

def __getAvgCPI__(year):
    global legacy_path
    legacy_path = pathlib.Path(__file__).parent.absolute().joinpath("../data/legacy/legacy_cpi_de.csv")

    cpi = pd.read_csv(legacy_path)

    return cpi.loc[cpi['Year'] == year].iat[0,1]

def __deflate__(amount, fromDate, toDate=None):
    
    if toDate == None:
        cD = datetime.datetime.now()
        toDate = str(str(cD.year) + "-" + str(cD.month) + "-" + str(cD.day))

    initialYear = int(fromDate.split("-")[0])
    currentYear = int(toDate.split("-")[0])

    finalCPI = __getAvgCPI__(currentYear)
    initialCPI = __getAvgCPI__(initialYear)

    adjustedAmount = (finalCPI/initialCPI) * amount

    return adjustedAmount

def deflateCurrency(amountInEuro, fromDate, toDate=None):
    if amountInEuro == None or fromDate == None:
        return None

    if type(amountInEuro) is list:
        res = []
        for i in amountInEuro:
            res.append(__deflate__(i, fromDate, toDate))
        return res
    else:
        try:
            amountInEuro = float(amountInEuro)
            return __deflate__(amountInEuro, fromDate, toDate)
        except Exception:
            print()