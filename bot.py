import json
import yfinance as yf
from datetime import datetime
import random
import commands


def buyCommand(arg, arg2):
    arg = arg.upper()
    prefix = "(" + arg + ") - "
    ticker = yf.Ticker(arg)
    today = datetime.now().date().strftime("%Y-%m-%d")
    price = ticker.info["currentPrice"]
    outstandingShares = int(ticker.info["sharesOutstanding"])
    cost = float(price * int(arg2))
    
    if (commands.getAvailableMoney() >= cost):
        if (int(arg2) > outstandingShares):
            arg2 = ticker.info["sharesOutstanding"]
            print(prefix + "{:,}".format(int(arg2)) + " shares were bought for |", "{:,}".format(round(price * int(arg2)), 2), "$")

            # checkt, ob der gekaufte stock schon "vorhanden" ist und erhöht einfach den amount.
            isDuplicate = False
            for i in commands.getPortfolio():
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
                    commands.setAvailableMoney(commands.getAvailableMoney() - cost)
                    
            if isDuplicate == False:
                stock = {
                    "ticker": arg,
                    "amount": str(arg2),
                    "datePurchased": today,
                    "worthAtPurchase": str(price),
                    "availableShares": str(outstandingShares - int(arg2))
                }

                # öffnet die 'files/portfolio.json' und fügt den gekauften stock hinzu.
                with open("files/portfolio.json", "r") as f:
                    data = json.load(f)
                    temp = data["stocks"]
                    temp.append(stock)

                commands.writeToJson("portfolio", data)
                commands.setAvailableMoney(commands.getAvailableMoney() - cost)
        elif (commands.getAvailableMoney() >= cost):
            print(prefix + "{:,}".format(int(arg2)) + " shares were bought for |", "{:,}".format(round(price * int(arg2)), 2), "$")

            # checkt, ob der gekaufte stock schon "vorhanden" ist und erhöht einfach den amount.
            isDuplicate = False
            for i in commands.getPortfolio():
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
                    commands.setAvailableMoney(commands.getAvailableMoney() - cost)
                    
            if isDuplicate == False:
                stock = {
                    "ticker": arg,
                    "amount": str(arg2),
                    "datePurchased": today,
                    "worthAtPurchase": str(price),
                    "availableShares": str(outstandingShares - int(arg2))
                }

                # öffnet die 'files/portfolio.json' und fügt den gekauften stock hinzu.
                with open("files/portfolio.json", "r") as f:
                    data = json.load(f)
                    temp = data["stocks"]
                    temp.append(stock)

                
                commands.writeToJson("portfolio", data)
                commands.setAvailableMoney(commands.getAvailableMoney() - cost)
    else:
        print(prefix + " no shares were bought because of a lack of available shares or liquid money")

def getRandomStocks(amount):
    with open("files/trash/working_stocks.json", "r") as f:
        data = json.load(f)
        stocks = []
        for i in range(amount):
            x = random.randint(0, 9860)
            stocks.append(data["tickers"][x])
    return stocks

def botRandomInvest(agressivness):
    if agressivness == "low":
        pass
    elif agressivness == "high":
        for i in getRandomStocks(5):
            ticker = yf.Ticker(str(i))
            menge = random.randint(1,420)
            price = int(ticker.info["currentPrice"]) * menge
            print("(" + str(i).upper() + ") - BOT PURCHASE - (" + str(i).upper() + ")")
            buyCommand(str(i), menge)
        print("\n(BOT) - - - - - - - - - - - - - - - - - - - - - - - - - -")
    elif agressivness == "metin":
        pass
