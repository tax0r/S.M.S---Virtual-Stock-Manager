from zoneinfo import available_timezones
import yfinance as yf
from datetime import datetime
import json

def calcStonks(ticker):   
    open = round(float(str(ticker.history(period="1d")["Open"]).split(" ")[5].split("\n")[0]), 2)
    close = round(float(str(ticker.history(period="1d")["Close"]).split(" ")[5].split("\n")[0]), 2)
    tmp1 = close - open
    growth = round(tmp1 / open, 3)
    
    stonksDict = {
        "open": str(open),
        "close": str(close),
        "growth": str(growth)
    }
    return stonksDict

def writeToJson(filename, data):
    with open("files/" + filename + ".json", "w") as f:
        json.dump(data, f, indent=4)

def getAvailableShares(ticker):
    with open("files/portfolio.json", "r") as f:
        data = json.load(f)
        for i in data['stocks']:
            if(str(i["ticker"]) == ticker):
                return int(i["availableShares"])
        return -1

def getAvailableMoney():
    with open("files/config.json", "r") as f:
        data = json.load(f)
    return float(data["liquid_money"])

def setAvailableMoney(money):
    with open("files/config.json", "r") as inFile:
        data = json.load(inFile)
        data["liquid_money"] = round(money,3)
    with open("files/config.json", "w") as outFile:
        #outFile.write(json.dumps(data))
        json.dump(data, outFile, indent=4)

def getMoneyInStocks():
    with open("files/portfolio.json", "r") as f:
        data = json.load(f)
        invested_money = 0
        for i in data["stocks"]:
            #print(i["amount"])
            invested_money += int(i["amount"]) * float(i["worthAtPurchase"])
    return round(invested_money, 2)

def getPortfolio():
    with open("files/portfolio.json", "r") as f:
        data = json.load(f)
        portfolio = []
        for i in data["stocks"]:
            portfolio.append(i["ticker"] + " " + i["amount"] + " " + i["worthAtPurchase"])
    return portfolio

def editPortfolio(ticker, amount):
    with open("files/portfolio.json", "r") as inFile:
        data = json.load(inFile)
        for i in data["stocks"]:
            if ticker in str(i):
                i["amount"] = str(int(i["amount"]) - int(amount))
    with open("files/portfolio.json", "w") as outFile:
        json.dump(data, outFile, indent=4)

def executeCmdOne(cmd, arg):

    prefix = "(" + arg + ") - "
    if cmd == "info":
        ticker = yf.Ticker(arg)
        stonksDict = calcStonks(ticker)
        print(prefix + "price per share | ", round(ticker.info["currentPrice"], 2), "$")
        print(prefix + "price at open | ", round(float(stonksDict["open"]), 2), "$")
        print(prefix + "price at close | ", round(float(stonksDict["close"]), 2), "$")
        print(prefix + "increase in '%' for one day | ", round(float(stonksDict["growth"]), 2), "%")
        print("\n" + prefix + "- - - - - - - - - - - - - - - - - - - - - - - - - -")
        print(prefix + "shares that are available to purchase | ", "{:,}".format(ticker.info["sharesOutstanding"]))
        print(prefix + "country of residence | ", ticker.info["country"])
        print("\n" + prefix + "- - - - - - - - - - - - - - - - - - - - - - - - - -")
        print(ticker.info["longBusinessSummary"])
    if cmd == "portfolio":
        for i in getPortfolio():
            if int(i.split(" ")[1]) is not 0:
                invested_money = round(int(i.split(" ")[1]) * float(i.split(" ")[2]), 2)
                ticker = yf.Ticker(i.split(" ")[0])
                currentPrice = round(ticker.info["currentPrice"], 2)
                # calculates % growth since purchase
                tmp1 = currentPrice * int(i.split(" ")[1])
                tmp2 = tmp1 - invested_money
                growth = round(tmp2 / invested_money, 2) * 100
                
                print("(" + str(i.split(" ")[0]) + ") you have invested", "{:,}".format(invested_money), "$ in", i.split(" ")[1], "share(s) =>", "{:,}".format(round(currentPrice * int(i.split(" ")[1]), 2)), "$", growth, "% growth.")
        
        print("\n(portfolio) - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("(portfolio) you have this much money invested in stocks:","{:,}".format(getMoneyInStocks()), "$")
        print("(portfolio) you have this much money left to invest:","{:,}".format(getAvailableMoney()), "$")
        print("(portfolio) - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

def executeCmdTwo(cmd, arg, arg2):
    prefix = "(" + arg + ") - "
    if cmd == "buy":
        ticker = yf.Ticker(arg)
        today = datetime.now().date().strftime("%Y-%m-%d")
        price = ticker.info["currentPrice"]
        outstandingShares = int(ticker.info["sharesOutstanding"])
        cost = float(price * int(arg2))

        if(getAvailableMoney() >= cost):
            if(int(arg2) > outstandingShares):
                arg2 = ticker.info["sharesOutstanding"]
                print(prefix + "{:,}".format(int(arg2)) + " shares were bought for |", "{:,}".format(round(price * int(arg2)), 2), "$")
                
                # checkt, ob der gekaufte stock schon "vorhanden" ist und erhöht einfach den amount.
                isDuplicate = False
                for i in getPortfolio():
                    if arg in i:
                        isDuplicate = True
                        with open("files/portfolio.json", "r") as inFile:
                            data = json.load(inFile)
                            for i in data["stocks"]:
                                if arg in str(i):
                                    i["amount"] = str(int(i["amount"]) + int(arg2))
                                    i["worthAtPurchase"] = str(price)
                        with open("files/portfolio.json", "w") as outFile:
                            json.dump(data, outFile, indent=4)
                        setAvailableMoney(getAvailableMoney() - cost)
                if isDuplicate == False:
                    stock = {
                    "ticker": arg,
                    "amount": arg2,
                    "datePurchased": today,
                    "worthAtPurchase" : str(price),
                    "availableShares": str(outstandingShares - int(arg2) )
                    }
                    
                    # öffnet die 'files/portfolio.json' und fügt den gekauften stock hinzu.
                    with open("files/portfolio.json", "r") as f:
                        data = json.load(f)
                        temp = data["stocks"]
                        temp.append(stock)

                    writeToJson("portfolio", data)
                    setAvailableMoney(getAvailableMoney() - cost)
            elif(getAvailableMoney() >= cost):
                print(prefix + "{:,}".format(int(arg2)) + " shares were bought for |", "{:,}".format(round(price * int(arg2)), 2), "$")

                # checkt, ob der gekaufte stock schon "vorhanden" ist und erhöht einfach den amount.
                isDuplicate = False
                for i in getPortfolio():
                    if arg in i:
                        isDuplicate = True
                        with open("files/portfolio.json", "r") as inFile:
                            data = json.load(inFile)
                            for i in data["stocks"]:
                                if arg in str(i):
                                    i["amount"] = str(int(i["amount"]) + int(arg2))
                                    i["worthAtPurchase"] = str(round(price, 2))
                        with open("files/portfolio.json", "w") as outFile:
                            json.dump(data, outFile, indent=4)
                        setAvailableMoney(getAvailableMoney() - cost)
                if isDuplicate == False:
                    stock = {
                    "ticker": arg,
                    "amount": arg2,
                    "datePurchased": today,
                    "worthAtPurchase" : str(price),
                    "availableShares": str(outstandingShares - int(arg2) )
                    }
                    
                    # öffnet die 'files/portfolio.json' und fügt den gekauften stock hinzu.
                    with open("files/portfolio.json", "r") as f:
                        data = json.load(f)
                        temp = data["stocks"]
                        temp.append(stock)

                    writeToJson("portfolio", data)
                    setAvailableMoney(getAvailableMoney() - cost)
        else:
            print(prefix + " no shares were bought because of a lack of available shares or liquid money")
    if cmd == "sell":
        ticker = yf.Ticker(arg)
        price = ticker.info["currentPrice"]
        cost = float(price * int(arg2))
        for i in getPortfolio():
            if arg in i:
                #print("ticker:", i.split(" ")[0])
                #print("menge:", i.split(" ")[1])
                #print("wert:", i.split(" ")[2])
                if int(arg2) <= int(i.split(" ")[1]):
                    print(prefix + "{:,}".format(int(arg2)) + " shares were sold for |", "{:,}".format(price * int(arg2)), "$")
                    print("(balance) - available money =>", "{:,}".format(getAvailableMoney()), "$")
                    setAvailableMoney(getAvailableMoney() + round(cost, 2))
                    editPortfolio(arg, arg2)
                else:
                    print(prefix + "you can't sell more stocks than you own! owned =>", i.split(" ")[1])
