import csv
import requests
from decimal import Decimal
from datetime import datetime
import os

operations = []
#0 = usd, 1 = eur for the following
sells = [[], []]
buys = [[], []]
dividends = [[], []]
fees = [[], []]
topups = [[], []]
withdrawals = [[], []]

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
            

def fetch_year_topups(year: int) -> Decimal:
    topups_y = Decimal(0)
    for operation in operations:
        if operation[0].startswith(str(year)) and operation[2] == "CASH TOP-UP":
            if operation[6] == "USD":
                topups_y += Decimal(operation[5])*usd
            elif operation[6] == "EUR":
                topups_y += Decimal(operation[5])*eur
    return topups_y


def fetch_year_withdrawals(year: int) -> Decimal:
    withdrawals_y = Decimal(0)
    for operation in operations:
        if operation[0].startswith(str(year)) and operation[2] == "CASH WITHDRAWAL":
            if operation[6] == "USD":
                withdrawals_y += Decimal(operation[5])*usd
            elif operation[6] == "EUR":
                withdrawals_y += Decimal(operation[5])*eur
    return withdrawals_y


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


def set_usd(rate: Decimal):
    global usd
    usd = rate


def set_eur(rate: Decimal):
    global eur
    eur = rate


def set_currency(curren: str):
    global currency
    currency = curren


def fetch_startyear() -> int:
    """
    returns the year of the first financial operation
    """
    years = set()
    for operation in operations:
        years.add(int(operation[0][:4]))
    startingyear = int(10000)
    for year in years:
        if year < startingyear:
            startingyear = year
    return startingyear


def tell_alltime():

    print(f"{currency} [ALL TIME] Sells: {round(sum_sells(), 2)}")
    print(f"{currency} [ALL TIME] Buys: {round(sum_buys(), 2)}")
    print(f"{currency} [ALL TIME] Dividends: {round(sum_dividends(), 2)}")
    print(f"{currency} [ALL TIME] Fees: {round(sum_fees(), 2)}")
    print(f"{currency} [ALL TIME] Topups: {round(sum_topups(), 2)}")
    print(f"{currency} [ALL TIME] Withdrawals: {round(sum_withdrawals(), 2)}")
    print(f"{currency} [ALL TIME] Balance: {round(sum_topups()-abs(sum_withdrawals()), 2)}")


def tell_nowinvested():
    print(f"{currency} [NOW] Invested: {round(sum_buys()-sum_sells(), 2)}")


def tell_year(year: int):
    print(f"{currency} [{year}] Sold: {round(fetch_year_sells(year), 2)}")
    print(f"{currency} [{year}] Bought: {round(fetch_year_buys(year), 2)}")
    print(f"{currency} [{year}] Balance: {round(fetch_year_buys(year)-fetch_year_sells(year), 2)}")
    print(f"{currency} [{year}] Topups: {round(fetch_year_topups(year), 2)}")
    print(f"{currency} [{year}] Withdrawals: {round(fetch_year_withdrawals(year), 2)}")


def fetch_eurrate():
    url = "https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/central-bank-exchange-rate-fixing/daily.txt"
    response = requests.get(url)
    data = response.text

    for line in data.splitlines():
        if "EUR" in line:
            parts = line.split("|")
            rate = Decimal(parts[4].replace(",", "."))
            return rate


def fetch_usdrate():
    url = "https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/central-bank-exchange-rate-fixing/daily.txt"
    response = requests.get(url)
    data = response.text

    for line in data.splitlines():
        if "USD" in line:
            parts = line.split("|")
            rate = Decimal(parts[4].replace(",", "."))
            return rate


def run():
    s_currency = "CZK"
    s_eur = fetch_eurrate()
    s_usd = fetch_usdrate()
    file = "file.csv"
    # file = input(f"Enter .csv file name: ")

    if not os.path.exists(file):
        print(f'File not found. Put your Revolut statement named "{file}" in the same directory as this programme and run it again.')
        print("Terminating...")
        quit()

    set_eur(Decimal(s_eur))
    set_usd(Decimal(s_usd))
    set_currency(s_currency)

    load_csv(file)

    remove_symbols()
    fetch_sells()
    fetch_buys()
    fetch_dividends()
    fetch_fees()
    fetch_withdrawals()
    fetch_topups()

    year = datetime.now().year

    print("="*30)
    print(f"EUR to CZK rate used: {fetch_eurrate()}")
    print(f"USD to CZK rate used: {fetch_usdrate()}")
    print("="*30)
    tell_alltime()
    print("="*30)
    tell_nowinvested()
    print("="*30)
    tell_year(year)
    print("="*30)
    fetch_startyear()
    

if __name__ == "__main__":
    run()