FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY stock_etl.py .

CMD ["python","stock_etl.py"]

