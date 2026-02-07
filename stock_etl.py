import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def make_graph(stock_data, revenue_data, stock):
    """
    Saves historical stock price and revenue data as a PNG image.
    """
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    # Plot Stock Price
    axes[0].plot(pd.to_datetime(stock_data_specific.Date), stock_data_specific.Close.astype("float"), label="Share Price", color="blue")
    axes[0].set_ylabel("Price ($US)")
    axes[0].set_title(f"{stock} - Historical Share Price")
    axes[0].legend()
    axes[0].grid(True)

    # Plot Revenue
    axes[1].plot(pd.to_datetime(revenue_data_specific.Date), revenue_data_specific.Revenue.astype("float"), label="Revenue", color="green")
    axes[1].set_ylabel("Revenue ($US Millions)")
    axes[1].set_xlabel("Date")
    axes[1].set_title(f"{stock} - Historical Revenue")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    
    # SAVE instead of SHOW
    filename = f"{stock}_dashboard.png"
    plt.savefig(filename)
    print(f"[SUCCESS] Graph saved: {filename}")
    plt.close()

def extract_stock_data(ticker_symbol):
    print(f"\n[EXTRACT] Fetching stock data for: {ticker_symbol}...")
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="max")
    data.reset_index(inplace=True)
    return data

def extract_revenue_data(url):
    print(f"[EXTRACT] Scraping revenue data from: {url}...")
    html_data = requests.get(url).text
    soup = BeautifulSoup(html_data, 'html.parser')
    
    tables = soup.find_all("tbody")
    if len(tables) > 1:
        target_table = tables[1]
    else:
        target_table = tables[0]

    data = []
    for row in target_table.find_all("tr"):
        col = row.find_all("td")
        if col:
            date = col[0].text.strip()
            revenue = col[1].text.strip()
            data.append({"Date": date, "Revenue": revenue})
            
    return pd.DataFrame(data, columns=['Date', 'Revenue'])

def clean_revenue_data(df):
    print("[TRANSFORM] Cleaning revenue data...")
    df["Revenue"] = df['Revenue'].str.replace(',|\\$', "", regex=True)
    df.dropna(inplace=True)
    df = df[df['Revenue'] != ""]
    return df

def main():
    # --- PROCESS TESLA ---
    tesla_data = extract_stock_data("TSLA")
    tesla_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
    tesla_revenue = extract_revenue_data(tesla_url)
    tesla_revenue = clean_revenue_data(tesla_revenue)
    
    # Save Tesla Data to CSV
    tesla_revenue.to_csv("tesla_revenue_data.csv", index=False)
    print("[SUCCESS] Table saved: tesla_revenue_data.csv")
    
    # --- PROCESS GAMESTOP ---
    gme_data = extract_stock_data("GME")
    gme_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
    gme_revenue = extract_revenue_data(gme_url)
    gme_revenue = clean_revenue_data(gme_revenue)
    
    # Save GameStop Data to CSV
    gme_revenue.to_csv("gme_revenue_data.csv", index=False)
    print("[SUCCESS] Table saved: gme_revenue_data.csv")
    
    # --- VISUALIZE ---
    make_graph(tesla_data, tesla_revenue, 'Tesla')
    make_graph(gme_data, gme_revenue, 'GameStop')

if __name__ == "__main__":
    main()