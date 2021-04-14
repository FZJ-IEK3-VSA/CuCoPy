from components import help as helper, inflation as infl, exchange as ex

def main():
    args = ["USD", "EUR", "2003-12-10"]
    
    try:
        sortedArgs = helper.getExchangeSortedArgs(args)
        historicalRates = ex.getHistoricalRate(*sortedArgs)
        print(historicalRates)

        inflationArgs = [historicalRates, args[2]]

        try:
            inflationArgs.append(args[3])
        except Exception:
            print()

        inflationArgs = helper.getInflationSortedArgs(inflationArgs)
        adjustedForInflation = infl.deflateCurrency(*inflationArgs)

        print(adjustedForInflation)
    except Exception as e:
        print(e)

main()
