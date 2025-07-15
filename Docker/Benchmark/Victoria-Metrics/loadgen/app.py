import requests
import time
import logging
from http.client import HTTPConnection

# Enable verbose HTTP logging (debug only)
HTTPConnection.debuglevel = 1

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
VICTORIA_METRICS_URL = "http://victoria-metrics:8428/write"

SEND_INTERVAL = 0.01  # 100 writes per second
METRIC_NAME = "benchmark_metric"
TAG = "host=loadgen"

def send_metric(value):
    try:
        ts = int(time.time() * 1000)  # milliseconds precision
        data = f"{METRIC_NAME},{TAG} value={value} {ts}"
        
        response = requests.post(
            VICTORIA_METRICS_URL,
            data=data,
            headers={'Content-Type': 'application/octet-stream'},
            timeout=1
        )
        
        if response.status_code != 204:
            logger.warning(f"Unexpected response: {response.status_code} - {response.text}")
        
    except Exception as e:
        logger.error(f"Error sending metric: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting VictoriaMetrics load generator")
    logger.info(f"Target: {VICTORIA_METRICS_URL}")
    logger.info(f"Interval: {SEND_INTERVAL} seconds")

    counter = 0
    try:
        while True:
            send_metric(counter % 100)  # Send values 0-99
            counter += 1
            time.sleep(SEND_INTERVAL)
    except KeyboardInterrupt:
        logger.info(f"Stopped after sending {counter} metrics")
