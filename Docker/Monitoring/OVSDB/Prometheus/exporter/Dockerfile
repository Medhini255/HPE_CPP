FROM python:3.10-slim

# Install ovs-vsctl
RUN apt-get update && \
    apt-get install -y openvswitch-switch && \
    apt-get clean

# Set up app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "ovsdb_exporter.py"]
