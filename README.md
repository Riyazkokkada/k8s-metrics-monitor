# 📊 Flask Prometheus Dashboard

A lightweight, real-time web dashboard built with **Flask**, **Prometheus**, and **Kubernetes** to monitor **CPU and Memory usage** of your nodes. Features include auto-refresh, visual usage indicators, average metrics, and responsive UI powered by Bootstrap.

![image](https://github.com/user-attachments/assets/ddc35b3a-ad10-4a69-b70f-d4f917b8294f)



---

## 🚀 Features

- 🔌 Auto port-forward to Prometheus inside your Kubernetes cluster
- 📈 Real-time CPU and Memory usage with PromQL queries
- 🎯 Visual indicators for each node (with high usage warnings)
- ⏱ Auto-refresh control (5s, 10s, 30s, 1min)
- 🌐 Displays both server and IST timezones
- 💡 Simple and clean UI with Bootstrap 5

---

## 🖥 Live Demo

> Add a GIF or image showing a working version, or deploy it to GitHub Pages/Heroku and link it.

---

## 🧰 Requirements

- Python 3.7+
- `kubectl` installed & access to Prometheus in Kubernetes
- Prometheus server running inside Kubernetes (namespace: `prometheus`)
- Python packages: `flask`, `requests`, `pytz`

---

## 🛠️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourusername/flask-prometheus-dashboard.git
cd flask-prometheus-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open your browser at: [http://localhost:8090](http://localhost:8090)

---

## 📦 Folder Structure

```
├── app.py                  # Flask backend
├── templates/
│   └── index.html          # Frontend HTML
├── static/
│   ├── style.css           # Custom styling
│   ├── script.js           # Auto-refresh script
│   └── demo_screenshot.png # Screenshot for README
├── requirements.txt
```

---

## 📊 Prometheus Queries Used

- **CPU Usage (%):**  
  ```promql
  100 * (1 - avg by(instance, job) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
  ```

- **Memory Usage (%):**  
  ```promql
  100 * (1 - avg by(instance, job) (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
  ```

---

## 🧠 Ideas for Future Enhancements

- Add email or Slack alerts for high CPU/memory
- Add support for multiple namespaces or pods
- Integrate with Grafana or InfluxDB
- Real-time streaming with WebSockets

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please open issues or PRs for suggestions and improvements.

---

## 🙌 Acknowledgments

- [Prometheus](https://prometheus.io/)
- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap 5](https://getbootstrap.com/)
