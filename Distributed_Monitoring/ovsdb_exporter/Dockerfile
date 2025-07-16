FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y openvswitch-switch sudo && \
    pip install prometheus_client

COPY exporter.py /exporter.py

CMD ["python", "/exporter.py"]
