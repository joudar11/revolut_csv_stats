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
    '''
    Fetches sells and saves them in global sells list.
    '''
    for operation in operations:
        if operation[2] == "SELL - MARKET":
            if operation[6] == "USD":
                sells[0].append(Decimal(operation[5]))
            if operation[6] == "EUR":
                sells[1].append(Decimal(operation[5]))


def sum_sells() -> Decimal:
    '''
    Returns sum of sells in set currency.
    '''
    usd_s = sum(sells[0])*usd
    eur_s = sum(sells[1])*eur
    return usd_s+eur_s


def fetch_buys():
    '''
    Fetches buys and saves them in global buys list.
    '''
    for operation in operations:
        if operation[2] == "BUY - MARKET":
            if operation[6] == "USD":
                buys[0].append(Decimal(operation[5]))
            if operation[6] == "EUR":
                buys[1].append(Decimal(operation[5]))


def sum_buys() -> Decimal:
    '''
    Returns sum of buys in set currency.
    '''
    usd_b = sum(buys[0])*usd
    eur_b = sum(buys[1])*eur
    return usd_b+eur_b


def fetch_dividends():
    '''
    Fetches dividends and saves them in global dividends list.
    '''
    for operation in operations:
        if operation[2] == "DIVIDEND":
            if operation[6] == "USD":
                dividends[0].append(Decimal(operation[5]))
            if operation[6] == "EUR":
                dividends[1].append(Decimal(operation[5]))


def sum_dividends() -> Decimal:
    '''
    Returns sum of dividends in set currency.
    '''
    usd_d = sum(dividends[0])*usd
    eur_d = sum(dividends[1])*eur
    return usd_d+eur_d


def fetch_fees():
    '''
    Fetches fees and saves them in global fees list.
    '''
    for operation in operations:
        if operation[2] == "CUSTODY FEE":
            if operation[6] == "USD":
                fees[0].append(abs(Decimal(operation[5])))
            if operation[6] == "EUR":
                fees[1].append(abs(Decimal(operation[5])))


def sum_fees() -> Decimal:
    '''
    Returns sum of fees in set currency.
    '''
    usd_f = sum(fees[0])*usd
    eur_f = sum(fees[1])*eur
    return usd_f+eur_f


def fetch_year_sells(year: int) -> Decimal:
    '''
    Returns sum of sells in set currency in given year.
    '''
    sells_y = Decimal(0)
    for operation in operations:
        if operation[0].startswith(str(year)) and operation[2] == "SELL - MARKET":
            if operation[6] == "USD":
                sells_y += Decimal(operation[5])/Decimal(operation[7])
            elif operation[6] == "EUR":
                sells_y += Decimal(operation[5])/Decimal(operation[7])
    return sells_y


def fetch_year_buys(year: int) -> Decimal:
    '''
    Returns sum of buys in set currency in given year.
    '''
    buys_y = Decimal(0)
    for operation in operations:
        if operation[0].startswith(str(year)) and operation[2] == "BUY - MARKET":
            if operation[6] == "USD":
                buys_y += Decimal(operation[5])/Decimal(operation[7])
            elif operation[6] == "EUR":
                buys_y += Decimal(operation[5])/Decimal(operation[7])
    return buys_y
            

def fetch_year_topups(year: int) -> Decimal:
    '''
    Returns sum of topups in set currency in given year.
    '''
    topups_y = Decimal(0)
    for operation in operations:
        if operation[0].startswith(str(year)) and operation[2] == "CASH TOP-UP":
            if operation[6] == "USD":
                topups_y += Decimal(operation[5])/Decimal(operation[7])
            elif operation[6] == "EUR":
                topups_y += Decimal(operation[5])/Decimal(operation[7])
    return topups_y


def fetch_year_withdrawals(year: int) -> Decimal:
    '''
    Returns sum of withdrawals in set currency in given year.
    '''
    withdrawals_y = Decimal(0)
    for operation in operations:
        if operation[0].startswith(str(year)) and operation[2] == "CASH WITHDRAWAL":
            if operation[6] == "USD":
                withdrawals_y += Decimal(operation[5])/Decimal(operation[7])
            elif operation[6] == "EUR":
                withdrawals_y += Decimal(operation[5])/Decimal(operation[7])
    return withdrawals_y


def fetch_topups():
    '''
    Fetches topups and saves them in global topups list.
    '''
    for operation in operations:
        if operation[2] == "CASH TOP-UP":
            if operation[6] == "USD":
                topups[0].append(Decimal(operation[5])/Decimal(operation[7]))
            if operation[6] == "EUR":
                topups[1].append(Decimal(operation[5])/Decimal(operation[7]))


def sum_topups() -> Decimal:
    '''
    Returns sum of topups in set currency.
    '''
    usd_t = sum(topups[0])
    eur_t = sum(topups[1])
    return usd_t+eur_t


def fetch_withdrawals():
    '''
    Fetches withdrawals and saves them in global withdrawals list.
    '''
    for operation in operations:
        if operation[2] == "CASH WITHDRAWAL":
            if operation[6] == "USD":
                withdrawals[0].append(Decimal(operation[5])/Decimal(operation[7]))
            if operation[6] == "EUR":
                withdrawals[1].append(Decimal(operation[5])/Decimal(operation[7]))


def sum_withdrawals() -> Decimal():
    '''
    Returns sum of withdrawals in set currency.
    '''
    usd_w = sum(withdrawals[0])
    eur_w = sum(withdrawals[1])
    return usd_w+eur_w


def set_usd(rate: Decimal):
    '''
    sets global variable for USD - CZK rate
    '''
    global usd
    usd = rate


def set_eur(rate: Decimal):
    '''
    sets global variable for EUR - CZK rate
    '''
    global eur
    eur = rate


def set_currency(curren: str):
    '''
    sets the global variable currency to be referred in tell functions
    '''
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
    '''
    Tells various all-time stats
    '''

    print(f"{currency} [ALL TIME] Sells: {tell(sum_sells())}")
    print(f"{currency} [ALL TIME] Buys: {tell(sum_buys())}")
    print(f"{currency} [ALL TIME] Invested: {tell(sum_buys()-sum_sells())}")
    print(f"{currency} [ALL TIME] Dividends: {tell(sum_dividends())}")
    print(f"{currency} [ALL TIME] Fees: {tell(sum_fees())}")
    print(f"{currency} [ALL TIME] Topups: {tell(sum_topups())}")
    print(f"{currency} [ALL TIME] Withdrawals: {tell(sum_withdrawals())}")


def tell_nowinvested():
    '''
    Tells how much money is invested - sum of topups and withdrawals
    '''
    print(f"{currency} [NOW] Invested: {tell(sum_topups()+sum_withdrawals())}")
    print("    (Topups - withdrawals)")

def tell_year(year: int):
    '''
    Tells various stats for given year
    '''
    print(f"{currency} [{year}] Bought: {tell(fetch_year_buys(year))}")
    print(f"{currency} [{year}] Sold: {tell(fetch_year_sells(year))}")
    print(f"{currency} [{year}] Balance: {tell(fetch_year_buys(year)-fetch_year_sells(year))}")
    print(f"{currency} [{year}] Topups: {tell(fetch_year_topups(year))}")
    print(f"{currency} [{year}] Withdrawals: {tell(fetch_year_withdrawals(year))}")
    print(f"{currency} [{year}] Invested: {tell(fetch_year_topups(year)+fetch_year_withdrawals(year))}")


def fetch_eurrate() -> Decimal():
    """
    returns current fx rate for eur - czk pair
    """
    url = "https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/central-bank-exchange-rate-fixing/daily.txt"
    response = requests.get(url)
    data = response.text

    for line in data.splitlines():
        if "EUR" in line:
            parts = line.split("|")
            rate = Decimal(parts[4].replace(",", "."))
            return rate


def fetch_usdrate() -> Decimal():
    """
    returns current fx rate for usd - czk pair
    """
    url = "https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/central-bank-exchange-rate-fixing/daily.txt"
    response = requests.get(url)
    data = response.text

    for line in data.splitlines():
        if "USD" in line:
            parts = line.split("|")
            rate = Decimal(parts[4].replace(",", "."))
            return rate


def tell(number: Decimal) -> Decimal():
    """
    rounds the number to preferred decimals
    """
    return(round(number, decimals))


def run():
    global decimals
    s_currency = "CZK"
    s_eur = fetch_eurrate()
    s_usd = fetch_usdrate()
    file = "file.csv"
    decimals = 3

    # file = input(f"Enter .csv file name: ")
    divider = "="*40

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

    currentyear = datetime.now().year

    print(divider)
    print(f"EUR to CZK rate used: {fetch_eurrate()}")
    print(f"USD to CZK rate used: {fetch_usdrate()}")
    print(divider)
    tell_nowinvested()
    print(divider)
    tell_alltime()
    print(divider)
    for year in range(currentyear, fetch_startyear()-1, -1):
        tell_year(year)
        print(divider)
    

if __name__ == "__main__":
    run()