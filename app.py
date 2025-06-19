import subprocess
import signal
import sys
import requests
from flask import Flask, request, render_template
from datetime import datetime
import pytz

app = Flask(__name__)

# Start kubectl port-forward subprocess in background
def start_port_forward():
    cmd = ["kubectl", "port-forward", "-n", "prometheus", "svc/prometheus-server", "9090:80"]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

port_forward_proc = start_port_forward()

def cleanup(signum, frame):
    print("Shutting down port-forward...")
    if port_forward_proc and port_forward_proc.poll() is None:
        port_forward_proc.terminate()
        try:
            port_forward_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            port_forward_proc.kill()
    print("Exiting app.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

def query_prometheus(promql):
    try:
        r = requests.get(PROMETHEUS_URL, params={"query": promql}, timeout=5)
        r.raise_for_status()
        result = r.json()
        if result["status"] != "success":
            return []
        return result["data"]["result"]
    except Exception as e:
        print(f"Error querying Prometheus: {e}")
        return []

@app.route("/")
def home():
    refresh = request.args.get("refresh", default="10")
    try:
        refresh = int(refresh)
    except:
        refresh = 10

    cpu_query = '100 * (1 - avg by(instance, job) (rate(node_cpu_seconds_total{mode="idle"}[5m])))'
    mem_query = '100 * (1 - avg by(instance, job) (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))'

    cpu_results = query_prometheus(cpu_query)
    mem_results = query_prometheus(mem_query)

    instances = {}

    for res in cpu_results:
        labels = res["metric"]
        key = (labels.get("instance", "N/A"), labels.get("job", "N/A"))
        usage = float(res["value"][1])
        if key not in instances:
            instances[key] = {"instance": key[0], "job": key[1], "cpu_usage": usage, "mem_usage": None}
        else:
            instances[key]["cpu_usage"] = usage

    for res in mem_results:
        labels = res["metric"]
        key = (labels.get("instance", "N/A"), labels.get("job", "N/A"))
        usage = float(res["value"][1])
        if key not in instances:
            instances[key] = {"instance": key[0], "job": key[1], "cpu_usage": None, "mem_usage": usage}
        else:
            instances[key]["mem_usage"] = usage

    # Filter out None values by replacing with 0
    for key, val in instances.items():
        if val["cpu_usage"] is None:
            val["cpu_usage"] = 0
        if val["mem_usage"] is None:
            val["mem_usage"] = 0

    cpu_avg = round(sum(i["cpu_usage"] for i in instances.values()) / (len(instances) or 1), 2)
    mem_avg = round(sum(i["mem_usage"] for i in instances.values()) / (len(instances) or 1), 2)

    # Times
    server_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ist = pytz.timezone("Asia/Kolkata")
    ist_time = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

    return render_template(
        "index.html",
        cpu_avg=cpu_avg,
        mem_avg=mem_avg,
        instances=instances.values(),
        refresh=refresh,
        server_time=server_time,
        ist_time=ist_time
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=True)

