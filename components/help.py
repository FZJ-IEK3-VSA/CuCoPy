import datetime

validBases = ["EUR", "USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF", "ISK", "NOK", "HRK", "RUB", "TRY", "AUD", "BRL", "CAD", "CNY", "HKD", "IDR", "ILS", "INR", "KRW", "MXN", "MYR", "NZD", "PHP", "SGD", "THB", "ZAR", "L-ATS", "L-BEF", "L-FIM", "L-FRF", "L-CYP", "L-DEM", "L-GRD", "L-IEP", "L-ITL", "L-LVL", "L-LTL", "L-LUF", "L-MTL", "L-NLG", "L-PTE", "L-SML", "L-SKK", "L-SIT", "L-ESP", "L-ECS", "L-SVC"]

def oneArgs(args):
    arg1 = None
    arg3 = None
    if not isValidBase(args[0]) and not isValidDate(args[0]):
        error("Invalid argument: Expected base or date (YYYY-mm-dd)")
    elif isValidBase(args[0]):
        arg1 = args[0]
    elif isValidDate(args[0]):
        arg3 = args[0]
    
    return [arg1, None, arg3, None]


def twoArgs(args):
    arg1 = None
    arg2 = None
    arg3 = None
    arg4 = None

    if isValidBase(args[0]):
        arg1 = args[0]
        if isValidBase(args[1]):
            arg2 = args[1]
        elif isValidDate(args[1]):
            arg3 = args[1]
        else:
            error("Invalid 2nd argument: Expected base or date (YYYY-mm-dd)")
    elif isValidDate(args[0]):
        arg3 = args[0]
        if isValidDate(args[1]):
            arg4 = args[1]
            success("Passed Date and Date")
        else:
            error("Invalid arguments")
    else:
        error("Invalid 1st argument: Expected base or date")
    return [arg1, arg2, arg3, arg4]

def threeArgs(args):
    arg1 = None
    arg2 = None
    arg3 = None
    arg4 = None

    if isValidBase(args[0]):
        arg1 = args[0]
        if isValidBase(args[1]):
            arg2 = args[1]
            if isValidDate(args[2]):
                arg3 = args[2]
                success("Passed Base and Base and Date")
            else:
                error("Invalid 3rd argument: Expected date (YYYY-mm-dd)")

        elif isValidDate(args[1]):
            arg3 = args[1]
            if isValidDate(args[2]):
                arg4 = args[2]
                success("Passed Base and Date and Date")
            else:
                error("Invalid 3rd argument: Expected date (YYYY-mm-dd)")
        else:
            error("Invalid 2nd argument: Expected base")
    else:
        error("Invalid 1st argument: Expected base")

    return [arg1, arg2, arg3, arg4]

def fourArgs(args):
    if not isValidBase(args[0]) or not isValidBase(args[1]) or not isValidDate(args[2]) or not isValidDate(args[3]):
        error("At least one argument is invalid: Expected base base date date")
    success("Passed Base and Date and Date")
    return args[:4]

def isValidBase(base):
    if "," in base:
        bases = base.split(",")
        for b in bases:
            if not isValidBase(b):
                return False
    else:
        if base in validBases:
            return True
        else:
            return False
    return True


def isValidDate(date):
    if not date == None:
        isCorrectDate = None
        date = date.split("-")
        try:
            date = datetime.datetime(int(date[0]),int(date[1]),int(date[2]))
            isCorrectDate = True
        except ValueError:
            isCorrectDate = False
        return isCorrectDate
    else:
        return False

def error(msg):
    raise Exception("[ERROR]",msg)

def success(msg):
    print("[SUCCESS]",msg)

def getExchangeSortedArgs(args):
    if len(args) == 0:
        return [None, None, None, None]

    elif len(args) == 1:
        return oneArgs(args)

    elif len(args) == 2:
        return twoArgs(args)

    elif len(args) == 3:
        return threeArgs(args)

    elif len(args) == 4:
        return fourArgs(args)

    else:
        error("You must specify at least one and at most 4 arguments")


def getInflationSortedArgs(args):
    if len(args) == 0 or len(args) == 1 or len(args) >= 4:
        return [None, None, None]

    if len(args) == 2:
        return twoArgsInf(args)

    if len(args) == 3:
        return threeArgsInf(args)

def twoArgsInf(args):
    arg1 = args[0]
    arg2 = None

    if isValidDate(args[1]):
        arg2 = args[1]
    else:
        error("Invalid 2nd argument: Expected date(YYYY-mm-dd)")

    return [arg1, arg2]

def threeArgsInf(args):
    arg1 = args[0]
    arg2 = None
    arg3 = None

    if isValidDate(args[1]):
        arg2 = args[1]
        if isValidDate(args[2]):
            arg3 = args[2]
        else:
            error("Invalid 3rd argument: Expected date (YYYY-mm-dd)")
    else:
        error("Invalid 2nd argument: Expected date (YYYY-mm-dd)")

    return [arg1, arg2, arg3]