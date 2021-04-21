from components import help as helper, inflation as infl, exchange as ex

def main():
    args = ["USD", "NOK", "2003"]
    toDate = "2004"
    
    try:
        sortedArgs = helper.getExchangeSortedArgs(args)
        historicalRates = ex.getHistoricalRate(*sortedArgs)
        print(historicalRates)

        inflationArgs = [historicalRates, args[1], args[2], toDate]

        try:
            inflationArgs.append(args[3])
        except Exception:
            print()

        print(inflationArgs)
        adjustedForInflation = infl.deflateCurrency(*inflationArgs)

        print(adjustedForInflation)
    except Exception as e:
        print(e)

main()
