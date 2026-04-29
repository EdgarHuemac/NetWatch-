# 📡 NetWatch — Network Presence Monitoring Tool

> *"Is anyone actually in the office right now?"*

NetWatch is a lightweight, non-invasive network presence monitoring tool built with **Python**, **Flask**, and **Nmap**. It continuously scans a local network to detect which devices are online, logs every scan to a database, and presents the data through a clean **MDB (Materialize Design Bootstrap)** web dashboard — letting you track the network presence of any host over time, in near real-time.

---

## 💡 The Idea

Every smartphone (and smartwatch, and laptop) in a modern office is connected to the Wi-Fi. Any machine on that same network can ping any other host and determine whether it's reachable. If a device is reachable, its owner is almost certainly within Wi-Fi range — and therefore physically present.

NetWatch exploits this simple fact:

- A lightweight **scanning agent** is deployed on any machine inside the network.
- The agent runs Nmap scans every few seconds and reports results to a central **Flask server**.
- The server stores every scan result and exposes an API + web dashboard to query historical presence data for any device by MAC address.
- No software needs to be installed on monitored devices. The only requirement is that target devices use a **static MAC address** (which most do by default).

A single agent can scan an entire `/24` network in ~6 seconds — that's up to **4,800 scans during an 8-hour workday**.

---

## 🗺️ Architecture

```
┌──────────────────────────────────────┐
│           Local Network (/24)        │
│                                      │
│  [Scanning Agent]  ──► HTTP POST ──► │──► [Flask Server]
│  python_scan_engine.py               │       app.py
│  (runs Nmap every N seconds)         │       data.db
│                                      │       administrator.db
└──────────────────────────────────────┘
                                            │
                                            ▼
                                    [Web Dashboard]
                                    MDB UI + Chart.js
                                    ┌──────────────┐
                                    │ Scans log    │
                                    │ Host activity│
                                    │ Presence %   │
                                    └──────────────┘
```

---

## ✨ Features

- **Continuous network scanning** using Nmap's ping scan (`-sP`) with configurable intervals
- **Centralized scan storage** in SQLite — every scan and every host seen is recorded
- **Per-device activity timeline** — visualize when any MAC address was online or offline over time
- **Network-wide activity chart** — see how many hosts were alive at each point in time
- **Administrator authentication** — session-based login system to protect the dashboard
- **User/host registration** — associate friendly names and MAC addresses for easy lookup
- **REST API endpoints** for programmatic access to scan data and activity history
- **Responsive UI** built with MDB (Materialize Design Bootstrap) and Chart.js

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask, Flask-Session |
| Scanner | python-nmap (Nmap wrapper) |
| Database | SQLite (via `sqlite3`) |
| Frontend | Jinja2 templates, MDB UI, jQuery, Chart.js |
| Charting | Chart.js with zoom/pan plugin |

---

## 📂 Project Structure

```
netwatch/
├── app.py                  # Flask server — routes, DB helpers, REST API
├── python_scan_engine.py   # Scanning agent — runs Nmap, POSTs results
├── init_db.py              # Database initializer — creates all tables
├── migrate_db.py           # DB migration helper
├── windows.py              # Windows firewall rule helper (optional)
├── data.db                 # Main SQLite database (scans, users, results)
├── administrator.db        # Admin credentials database
├── static/
│   ├── css/                # MDB stylesheets
│   ├── js/                 # MDB, jQuery, Chart.js, zoom plugin
│   └── img/                # Static assets
└── templates/
    ├── index.html          # User/host registration & list
    ├── scans.html          # Scan log with network activity chart
    ├── activity.html       # Per-device presence timeline
    ├── scan-results.html   # Detailed results for a single scan
    ├── login.html          # Admin login page
    ├── new-administrator.html  # Admin management
    └── navbar.html         # Shared navigation bar
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [Nmap](https://nmap.org/download.html) installed on the system and available in `PATH`
- `pip` packages: `flask`, `flask-session`, `python-nmap`, `requests`

```bash
pip install flask flask-session python-nmap requests
```

> ⚠️ Nmap ping scans require **root/administrator privileges**. Run the scanning agent with `sudo` on Linux/macOS or as Administrator on Windows.

---

### 1. Initialize the Database

```bash
python init_db.py
```

This creates `data.db` and `administrator.db` with the required schema.

---

### 2. Start the Flask Server

```bash
python app.py
```

The server starts on `http://0.0.0.0:5000` by default (debug mode enabled).

---

### 3. Create an Administrator Account

Navigate to the admin registration endpoint or use the `/new-administrator` page in the dashboard to create your first admin account.

---

### 4. Configure and Run the Scanning Agent

Edit `python_scan_engine.py` to point at your environment:

```python
SERVER  = 'http://<your-server-ip>:5000'   # Flask server address
NETWORK = '192.168.1.0/24'                 # Network range to scan
TIME_BETWEEN_SCANS = 3                     # Seconds between scans
```

Then run it (with appropriate privileges):

```bash
sudo python python_scan_engine.py
```

The agent will immediately begin scanning and sending data to the server.

---

### 5. Register Hosts to Monitor

Log in to the dashboard and navigate to the home page to register MAC addresses with friendly names. Once registered, you can click any MAC address to view its full activity timeline.

---

## 📊 Dashboard Pages

| Route | Description |
|---|---|
| `/` | Register and list monitored hosts |
| `/scans` | Full scan log with network-wide activity chart |
| `/activity?h=<mac>` | Per-device presence timeline chart |
| `/scan-results` | All individual host results across all scans |
| `/new-administrator` | Admin account management |
| `/login` | Authentication |

### API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/register-network-scan` | POST | Receive scan data from an agent |
| `/get-activity/<mac>` | GET | Get presence timeline for a MAC address |
| `/get-network-history` | GET | Get time-series data of alive host counts |
| `/scan-results-from-scan/<id>` | GET | Get all hosts seen in a specific scan |

---

## ⚙️ How the Activity Timeline Works

The `/get-activity/<mac>` endpoint cross-references two tables:

1. **SCAN** — every scan that was ever performed, identified by UUID and timestamp
2. **SCAN_RESULT** — every host seen in each scan, keyed by MAC address

For each scan in history, the API checks whether the target MAC appeared in that scan's results. The response is a time-series array of `{ time, state }` objects where `state` is `1` (present) or `0` (absent), which Chart.js renders as a binary presence graph.

---

## 🔒 Privacy & Ethical Considerations

This tool operates entirely within your own local network and requires no software installation on monitored devices. Even so:

- **Always obtain proper authorization** before monitoring any network you do not own or administer.
- Inform users if this tool is deployed in a workplace or shared environment, in accordance with applicable privacy laws (GDPR, CCPA, etc.).
- MAC address randomization (enabled by default on modern iOS and Android) can affect tracking accuracy.
- This project was built as a **proof of concept** and a learning exercise. Use responsibly.

---

## 🔮 Ideas for Future Work

- [ ] Support for multiple named scanning agents
- [ ] MAC address randomization detection / mitigation strategies
- [ ] Email or webhook alerts when a host goes offline or comes online
- [ ] Machine learning layer to predict arrival/departure patterns
- [ ] Docker setup for easy deployment
- [ ] HTTPS support + production-grade WSGI server (Gunicorn/uWSGI)
- [ ] Improved SQL injection protections and password hashing

---

## 📝 License

This project is released for educational purposes. Feel free to fork, extend, and experiment.
I created this project since 2022, only for fun, and just uploaded it to Github, and have not touched it much ever since. 

---

*Built with curiosity, Flask, and way too many Nmap scans. 🐍*
