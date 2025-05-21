import csv
import math
from decimal import Decimal

operations = []
#0 = usd, 1 = eur for the following
sells = [[], []]
sells_sum = Decimal(0)
buys = [[], []]
buys_sum = Decimal(0)
dividends = [[], []]
dividends_sum = Decimal(0)
fees = [[], []]
fees_sum = Decimal(0)
topups = [[], []]
topups_sum = Decimal(0)
withdrawals = [[], []]
withdrawals_sum = Decimal(0)

usd = Decimal(21.97)
eur = Decimal(24.9)
currency = "CZK"

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
                sells[0].append(Decimal(operation[5]))
            if operation[6] == "EUR":
                sells[1].append(Decimal(operation[5]))


def sum_sells() -> Decimal:
    usd_s = sum(sells[0])*usd
    eur_s = sum(sells[1])*eur
    return usd_s+eur_s


def fetch_buys():
    for operation in operations:
        if operation[2] == "BUY - MARKET":
            if operation[6] == "USD":
                buys[0].append(Decimal(operation[5]))
            if operation[6] == "EUR":
                buys[1].append(Decimal(operation[5]))


def sum_buys() -> Decimal:
    usd_b = sum(buys[0])*usd
    eur_b = sum(buys[1])*eur
    return usd_b+eur_b


def fetch_dividends():
    for operation in operations:
        if operation[2] == "DIVIDEND":
            if operation[6] == "USD":
                dividends[0].append(Decimal(operation[5]))
            if operation[6] == "EUR":
                dividends[1].append(Decimal(operation[5]))


def sum_dividends() -> Decimal:
    usd_d = sum(dividends[0])*usd
    eur_d = sum(dividends[1])*eur
    return usd_d+eur_d


def fetch_fees():
    for operation in operations:
        if operation[2] == "CUSTODY FEE":
            if operation[6] == "USD":
                fees[0].append(abs(Decimal(operation[5])))
            if operation[6] == "EUR":
                fees[1].append(abs(Decimal(operation[5])))


def sum_fees() -> Decimal:
    usd_f = sum(fees[0])*usd
    eur_f = sum(fees[1])*eur
    return usd_f+eur_f


def fetch_year_sells(year: int) -> Decimal:
    sells_y = Decimal(0)
    for operation in operations:
        if operation[0].startswith(str(year)) and operation[2] == "SELL - MARKET":
            if operation[6] == "USD":
                sells_y += Decimal(operation[5])*usd
            elif operation[6] == "EUR":
                sells_y += Decimal(operation[5])*eur
    return sells_y


def fetch_year_buys(year: int) -> Decimal:
    buys_y = Decimal(0)
    for operation in operations:
        if operation[0].startswith(str(year)) and operation[2] == "BUY - MARKET":
            if operation[6] == "USD":
                buys_y += Decimal(operation[5])*usd
            elif operation[6] == "EUR":
                buys_y += Decimal(operation[5])*eur
    return buys_y
            

def fetch_ticker_stats():
    #to be added
    pass


def fetch_topups():
    for operation in operations:
        if operation[2] == "CASH TOP-UP":
            if operation[6] == "USD":
                topups[0].append(Decimal(operation[5]))
            if operation[6] == "EUR":
                topups[1].append(Decimal(operation[5]))


def sum_topups() -> Decimal:
    usd_t = sum(topups[0])*usd
    eur_t = sum(topups[1])*eur
    return usd_t+eur_t


def fetch_withdrawals():
    for operation in operations:
        if operation[2] == "CASH WITHDRAWAL":
            if operation[6] == "USD":
                withdrawals[0].append(Decimal(operation[5]))
            if operation[6] == "EUR":
                withdrawals[1].append(Decimal(operation[5]))


def sum_withdrawals() -> Decimal():
    usd_w = sum(withdrawals[0])*usd
    eur_w = sum(withdrawals[1])*eur
    return usd_w+eur_w

def run():
    file = "file.csv"
    load_csv(file)
    remove_symbols()
    fetch_sells()
    fetch_buys()
    fetch_dividends()
    fetch_fees()
    fetch_withdrawals()
    fetch_topups()
    year = 2025

    sells_sum = sum_sells()
    buys_sum = sum_buys()
    dividends_sum = sum_dividends()
    sells_year = fetch_year_sells(year)
    buys_year = fetch_year_buys(year)
    fees_sum = sum_fees()
    withdrawals_sum = sum_withdrawals()
    topups_sum = sum_topups()

    print("="*30)
    print(f"{currency} [ALL TIME] Sells: {round(sells_sum, 2)}")
    print(f"{currency} [ALL TIME] Buys: {round(buys_sum, 2)}")
    print(f"{currency} [ALL TIME] Dividends: {round(dividends_sum, 2)}")
    print(f"{currency} [ALL TIME] Fees: {round(fees_sum, 2)}")
    print(f"{currency} [ALL TIME] Topups: {round(topups_sum, 2)}")
    print(f"{currency} [ALL TIME] Withdrawals: {round(withdrawals_sum, 2)}")
    print(f"{currency} [NOW] Invested: {round(buys_sum-sells_sum, 2)}")
    print("="*30)
    print(f"{currency} [{year}] Sold: {round(sells_year, 2)}")
    print(f"{currency} [{year}] Bought: {round(buys_year, 2)}")
    print(f"{currency} [{year}] Balance: {round(buys_year-sells_year, 2)}")
    print("="*30)

    

if __name__ == "__main__":
    run()