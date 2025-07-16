FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY benchmark_queries.py .

CMD ["python", "benchmark_queries.py"]
