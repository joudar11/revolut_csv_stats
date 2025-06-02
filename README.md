# Revolut Statement Analyzer (Python)

Tento projekt je **offline Python aplikace**, která slouží k analýze exportu investičního výpisu z Revolutu ve formátu `.csv`. Na základě transakcí (nákupy, prodeje, dividendy, poplatky atd.) vypočítá klíčové statistiky o vývoji investic.

## 🧩 Funkce

- Výpočet celkových nákupů, prodejů, dividend, poplatků, vkladů a výběrů
- Přepočet měn (USD/EUR → CZK) podle aktuálního kurzu ČNB
- Zobrazení statistik po jednotlivých letech
- Výpočet aktuální hodnoty portfolia podle kurzů z Yahoo Finance
- Výstraha při překročení prodejů nad 100 000 Kč (daňová povinnost)
- (některé funkce jsou "zbytečně" rozděleny na USD a EUR operace - počítá se s budoucí úpravou.)

## ✅ Požadavky

- Python 3.13
- Knihovny:
  - `requests`
  - `yfinance`
  - `decimal`
  - `csv`
  - `datetime`

Instalace závislostí:

```bash
pip install -r requirements.txt
```

## 📄 Použití

1. Umísti výpis z Revolutu (např. `statement.csv`) do stejné složky jako skript.
2. Spusť hlavní soubor:

```bash
python main.py
```

3. Program načte soubor, zpracuje data a zobrazí:
   - Přehled investic v CZK (aktuální hodnota, zisk/ztráta)
   - Souhrny za jednotlivé roky
   - Výpis jednotlivých tickerů a jejich vývoj

## 📊 Vzorec výpočtu

Přepočet do CZK probíhá podle aktuálního kurzu ČNB, který si program stáhne automaticky. Hodnoty z výpisu jsou čištěny od symbolů, čárek apod.

## 📁 Struktura projektu

```
projekt/
├── main.py               # hlavní analyzátor
├── requirements.txt      # seznam závislostí
├── statement.csv         # investiční výpis z Revolutu (není součástí repozitáře)
```

## ⚠️ Upozornění

- Tento nástroj je určen pouze pro **osobní analýzu investic**.
- Neprovádí žádné úřední daňové výpočty.
- Vždy ověř konečné hodnoty a legislativu s účetním.

## 👤 Autor

**Kryštof Klika**  
