from flask import Response, Flask
from prometheus_client import Gauge, generate_latest
import random, time

app = Flask(__name__)
metric = Gauge('simulated_metric', 'Simulated Metric', ['label'])

@app.route('/metrics')
def metrics():
    for i in range(1000):  # Simulate high cardinality
        metric.labels(label=f'label_{i}').set(random.random())
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 
