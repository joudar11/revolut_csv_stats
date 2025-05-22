import csv
import requests
from decimal import Decimal
from datetime import datetime
import os
import yfinance as yf

operations = []
#0 = usd, 1 = eur for the following
sells = [[], []]
buys = [[], []]
dividends = [[], []]
fees = [[], []]
topups = [[], []]
withdrawals = [[], []]
tickers = {}

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
    print(f"{currency} [ALL TIME] Balance: {tell(sum_buys()-sum_sells())}")
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


def fetch_tickers():
    """
    adds tickers information in global tickers dict. {ticker_name: [amount held, money spent]} 
    """
    global tickers
    tickers_set = set()
    for operation in operations:
        if operation[1]:
            tickers_set.add(operation[1])

    tickers_list = sorted(tickers_set)

    tickers = {ticker: [Decimal(0), Decimal(0)] for ticker in tickers_list}

    for operation in operations:
        if operation[3] and operation[5]:
            ticker = operation[1]
            amount = Decimal(operation[3])
            money = Decimal(operation[5])/Decimal(operation[7])
            if operation[2] in ("BUY - MARKET", "SELL - MARKET", "STOCK SPLIT"):
                if operation[2] == "BUY - MARKET":
                    tickers[ticker][0] += amount
                    tickers[ticker][1] += money
                if operation[2] == "SELL - MARKET":
                    tickers[ticker][0] -= amount
                    tickers[ticker][1] -= money
                if operation[2] == "STOCK SPLIT":
                    tickers[ticker][0] += amount
                    tickers[ticker][1] += money
     

def tell_tickers():
    print(f"Ticker summaries:")
    print(divider)
    for ticker, (amount, money) in tickers.items():
        if amount == 0:
            amount_print = int(0)
        else:
            amount_print = amount

        price = get_price(ticker)
        currency_ = get_currency(ticker)
        value = amount_print * price

        
        print(f"Ticker: {ticker}")
        print(f"Amount: {amount_print}")
        print(f"Current price per 1 share: {tell(price)} {currency_}")
        print(f"Current value: {tell(value)} {currency_}")

        if currency_ == "USD":
            print(f"SUM invested {currency}: {tell(money)}")
            print(f"Current value {currency}: {tell(value * usd)}")
            print(f"Profit/loss {currency}: {tell((value * usd) - money)}")
        elif currency_ == "EUR":
            print(f"SUM invested {currency}: {tell(money)}")
            print(f"Current value {currency}: {tell(value * eur)}")
            print(f"Profit/loss {currency}: {tell((value * eur) - money)}")
        else:
            print("ERROR.")
        print(divider)


def fix_ticker(ticker: str) -> str:
    corrections = {
        "BRK.B": "BRK-B",
        "BRK.A": "BRK-A",
        "RHM": "RHM.DE",
    }
    return corrections.get(ticker, ticker)


def get_price(ticker: str) -> Decimal:
    """
    Returns the current price of a given stock ticker using Yahoo Finance.
    """
    ticker = fix_ticker(ticker)
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        price = data["Close"].iloc[-1]
        return Decimal(price)
    except Exception as e:
        print(f"Error getting price {ticker}: {e}")
        return Decimal(0)


def get_currency(ticker: str) -> str:
    ticker = fix_ticker(ticker)
    try:
        stock = yf.Ticker(ticker)
        return stock.info.get("currency", "N/A")
    except:
        return "N/A"


def run():
    # how many decimals to be used in stats:
    global decimals
    decimals = 3
    # name of currency showns in stats (CZK)
    s_currency = "CZK"
    # name of the Revolut statement .csv file
    file = "statement.csv"
    if not file.endswith(".csv"):
        file += ".csv"
    # divider to be shown in report
    global divider
    divider = "="*40

    # check file exists
    if not os.path.exists(file):
        print(f'File not found. Put your Revolut statement named "{file}" in the same directory as this programme and run it again.')
        print("Terminating...")
        quit()

    # set currency name and fx rates
    s_eur = fetch_eurrate()
    s_usd = fetch_usdrate()
    set_eur(Decimal(s_eur))
    set_usd(Decimal(s_usd))
    set_currency(s_currency)

    load_csv(file)

    # process the file, save the values
    remove_symbols()
    fetch_sells()
    fetch_buys()
    fetch_dividends()
    fetch_fees()
    fetch_withdrawals()
    fetch_topups()
    fetch_tickers()

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
    tell_tickers()

if __name__ == "__main__":
    run()