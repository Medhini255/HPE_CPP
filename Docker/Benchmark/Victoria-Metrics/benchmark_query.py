import requests
import time

durations = []
for i in range(100):
    start = time.time()
    r = requests.get("http://localhost:8428/api/v1/query", params={
        "query": "rate(benchmark_metric[1m])"
    })
    durations.append(time.time() - start)

print(f"Average query latency: {sum(durations)/len(durations):.4f} sec") 
