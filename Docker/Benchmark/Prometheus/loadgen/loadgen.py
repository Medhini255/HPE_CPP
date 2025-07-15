from prometheus_client import start_http_server, Gauge
import random
import time

# Use a single metric with labels to create high cardinality
metric = Gauge('custom_metric', 'High cardinality metric', ['region', 'instance', 'job', 'metric_id'])

# Generate 10,000 unique label combinations
label_sets = []
for metric_id in range(1000):  # 1000 distinct metric_ids
    for region in range(2):    # 2 regions
        for instance in range(5):  # 5 instances
            for job in range(1):  # 1 job
                label_sets.append({
                    'region': f'region_{region}',
                    'instance': f'inst_{instance}',
                    'job': f'job_{job}',
                    'metric_id': f'id_{metric_id}'
                })

def update_metrics():
    while True:
        for labels in label_sets:
            metric.labels(**labels).set(random.random())
        time.sleep(1)

if __name__ == "__main__":
    start_http_server(8000)
    print("Exporter running on http://localhost:8000/metrics with high cardinality")
    update_metrics()


#scrape_duration_seconds search this 
