from flask import Flask, Response
import subprocess

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    try:
        bridges = subprocess.check_output(["ovs-vsctl", "list-br"]).decode().splitlines()
        metric = f"# HELP ovsdb_bridge_count Number of OVS bridges\n"
        metric += f"# TYPE ovsdb_bridge_count gauge\n"
        metric += f"ovsdb_bridge_count {len(bridges)}\n"
        return Response(metric, mimetype="text/plain")
    except Exception as e:
        return Response(f"# Exporter error: {str(e)}\n", mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
