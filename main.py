import csv


operations = []


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
    Removes the currency symbol for every line in global poerations list.
    """


def fetch_sells() -> float:
    pass


def fetch_buys() -> float:
    pass


def fetch_dividends() -> float:
    pass


def fetch_fees() -> float:
    pass


def run():
    file = "file.csv"
    load_csv(file)
    print(operations)


if __name__ == "__main__":
    run()