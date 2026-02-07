# Stock & Revenue ETL Pipeline 📈

A containerized ETL project that extracts financial data for Tesla and GameStop, transforms it, and generates historical dashboards.

## Tech Stack
* **Python:** yfinance, Pandas, BeautifulSoup
* **Containerization:** Docker
* **Visualization:** Matplotlib

## How to Run
1.  Build the image: `docker build -t stock-etl .`
2.  Run the container: `docker run -v ${PWD}:/app stock-etl`
