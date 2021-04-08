from components import help as helper, inflation as infl, exchange as ex

def main():
    args = ["EUR", "INR", "2008-01-12", "2019-01-12"]
    
    try:
        sortedArgs = helper.getSortedArgs(args)
        ex.getHistoricalRate(*sortedArgs)
    except Exception as e:
        print(e)

main()
