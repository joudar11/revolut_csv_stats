import csv
import math
from decimal import Decimal

operations = []
#0 = usd, 1 = eur for the following
sells = [[], []]
sells_sum = float(0)
buys = [[], []]
buys_sum = float(0)
dividends = [[], []]
dividends_sum = float(0)
fees = [[], []]
fees_sum = float(0)

usd = 21.97
eur = 24.9

def load_csv(filename: str):
    """
    Loads the Revolut .csv and saves all the lines except for the header in global operations list.
    """
    # Date,Ticker,Type,Quantity,Price per share,Total Amount,Currency,FX Rate

    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) #skip header
        for row in reader:
            operations.append(list(row))


def remove_symbols():
    """
    Removes the currency symbol and divider for every line in global poerations list.
    """
    for operation in operations:
        operation[4] = operation[4].replace("$", "")
        operation[5] = operation[5].replace("$", "")
        operation[4] = operation[4].replace("â\x82¬", "")
        operation[5] = operation[5].replace("â\x82¬", "")
        operation[4] = operation[4].replace(",", "")
        operation[5] = operation[5].replace(",", "")


def fetch_sells():
    for operation in operations:
        if operation[2] == "SELL - MARKET":
            if operation[6] == "USD":
                sells[0].append(float(operation[5]))
            if operation[6] == "EUR":
                sells[1].append(float(operation[5]))


def sum_sells() -> float:
    usd_s = math.fsum(sells[0])*usd
    eur_s = math.fsum(sells[1])*eur
    return usd_s+eur_s


def fetch_buys():
    for operation in operations:
        if operation[2] == "BUY - MARKET":
            if operation[6] == "USD":
                buys[0].append(float(operation[5]))
            if operation[6] == "EUR":
                buys[1].append(float(operation[5]))


def sum_buys() -> float:
    usd_b = math.fsum(buys[0])*usd
    eur_b = math.fsum(buys[1])*eur
    return usd_b+eur_b


def fetch_dividends():
    for operation in operations:
        if operation[2] == "DIVIDEND":
            if operation[6] == "USD":
                dividends[0].append(float(operation[5]))
            if operation[6] == "EUR":
                dividends[1].append(float(operation[5]))


def sum_dividends() -> float:
    usd_d = math.fsum(dividends[0])*usd
    eur_d = math.fsum(dividends[1])*eur
    return usd_d+eur_d


def fetch_fees():
    for operation in operations:
        if operation[2] == "CUSTODY FEE":
            if operation[6] == "USD":
                fees[0].append(abs(float(operation[5])))
            if operation[6] == "EUR":
                fees[1].append(abs(float(operation[5])))


def sum_fees() -> float:
    usd_f = math.fsum(fees[0])*usd
    eur_f = math.fsum(fees[1])*eur
    return usd_f+eur_f


def fetch_year_sells():
    sells = float(0)
    for operation in operations:
        if operation[0].startswith("2025") and operation[2] == "SELL - MARKET":
            if operation[6] == "USD":
                sells += float(operation[5])*usd
            elif operation[6] == "EUR":
                sells += float(operation[5])*eur
    return sells
            

def fetch_ticker_stats():
    #to be added
    pass


def run():
    file = "file.csv"
    load_csv(file)
    remove_symbols()
    fetch_sells()
    fetch_buys()
    fetch_dividends()
    fetch_fees()

    sells_sum = sum_sells()
    buys_sum = sum_buys()
    dividends_sum = sum_dividends()
    sells_year = fetch_year_sells()
    fees_sum = sum_fees()

    print("="*30)
    print(f"CZK [ALL TIME] Sells: {round(sells_sum, 2)}")
    print(f"CZK [ALL TIME] Buys: {round(buys_sum, 2)}")
    print(f"CZK [ALL TIME] Dividends: {round(dividends_sum, 2)}")
    print(f"CZK [ALL TIME] Fees: {round(fees_sum, 2)}")
    print(f"CZK [NOW] Invested: {round(buys_sum-sells_sum, 2)}")
    print(f"CZK [THIS YEAR] Sold: {round(sells_year, 2)}")
    print("="*30)

    

if __name__ == "__main__":
    run()