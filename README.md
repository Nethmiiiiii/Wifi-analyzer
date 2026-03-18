# 🛜 Wi-Fi Security Analyzer

A Python-based terminal tool that scans your Wi-Fi network for security vulnerabilities, detects unauthorized devices, and gives you an actionable security score.

> ⚠️ **Legal Notice:** Only use this tool on networks you own or have explicit written permission to test. Unauthorized network scanning may violate local laws.

---

## 📸 Features

- 🔍 **Network Info Scanner** — Reads your connected Wi-Fi's SSID, BSSID, signal strength, and encryption type
- 🔐 **Encryption Checker** — Detects WEP, WPA, WPA2, and WPA3 protocols and flags outdated ones
- 💻 **Device Discovery** — Lists all devices connected to your network (IP, MAC, hostname)
- ⚠️ **Evil Twin Detection** — Identifies potential rogue access point attacks
- 📊 **Security Score** — Rates your network from 0–100 with color-coded results
- 📄 **Report Export** — Saves a full text report with a timestamp

---

## 🗂️ Project Structure

```
wifi_analyzer/
│
├── main.py          # Entry point — coordinates all modules
├── scanner.py       # Gathers live network data
├── analyzer.py      # Analyzes data for vulnerabilities
├── reporter.py      # Displays results with color formatting
└── utils.py         # Helper functions (OS detection, admin check, etc.)
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Scapy | Packet-level network analysis |
| Colorama | Color-coded terminal output |
| Tabulate | Structured table display |
| Subprocess / ARP | Live device discovery |
| Socket | Hostname resolution |

---

## ⚙️ Installation

### Prerequisites

**Windows**
- Python 3.10+ — [python.org](https://python.org) *(check "Add to PATH")*
- Npcap — [npcap.com](https://npcap.com) *(check "WinPcap API-compatible Mode")*

**Linux**
```bash
sudo apt update && sudo apt install python3 python3-pip wireless-tools net-tools
```

**macOS**
```bash
brew install python3
```

---

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Nethmiiiiii/Wifi-analyzer.git
cd Wifi-analyzer

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install scapy psutil colorama tabulate requests
```

---

## 🚀 Usage

> Run as **Administrator** (Windows) or **sudo** (Linux/Mac) for full functionality.

**Windows** — Open terminal as Administrator:
```bash
python main.py
```

**Linux / macOS:**
```bash
sudo python3 main.py
```

**VS Code** — Press `F5` (with the provided launch config)

---

## 📊 Sample Output

```
╔══════════════════════════════════════════════╗
║        🛜  Wi-Fi Security Analyzer           ║
║        Scan · Detect · Protect               ║
╚══════════════════════════════════════════════╝

📡 Connected Network Info
╭────────────┬────────────────────╮
│ SSID       │ MyHomeNetwork      │
│ SECURITY   │ WPA2-Personal      │
│ SIGNAL     │ 78%                │
│ CHANNEL    │ 6                  │
╰────────────┴────────────────────╯

💻 Devices on Network (3 found)
╭─────────────────┬───────────────────┬──────────────╮
│ IP Address      │ MAC Address       │ Hostname     │
├─────────────────┼───────────────────┼──────────────┤
│ 192.168.1.1     │ aa:bb:cc:dd:ee:ff │ router       │
│ 192.168.1.105   │ 11:22:33:44:55:66 │ Johns-iPhone │
╰─────────────────┴───────────────────┴──────────────╯

🔍 Vulnerability Report
  [INFO] WPA2-AES Detected
  🔧 Fix: Consider upgrading to WPA3

🔐 Security Score: 90/100 — GOOD
```

---

## 🔍 What It Detects

| Issue | Severity |
|---|---|
| Open network (no encryption) | 🔴 CRITICAL |
| WEP encryption (broken) | 🔴 CRITICAL |
| WPA with TKIP (outdated) | 🟠 HIGH |
| Evil Twin / Rogue AP | 🟠 HIGH |
| Suspicious MAC addresses | 🟠 HIGH |
| WPA2 with TKIP cipher | 🟡 MEDIUM |
| Weak signal strength | 🟡 MEDIUM |
| WPA2-AES (acceptable) | 🟢 INFO |
| WPA3 (best) | 🟢 INFO |

---

## 🗒️ Generated Report

When you choose to save, a report file is created automatically:

```
wifi_report_20260318_174500.txt
```

It contains the full network info, device list, all issues found, and your security score.

---

## 🧰 Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: scapy` | Run `pip install scapy` inside activated venv |
| No network info returned | Run as Administrator / sudo |
| Empty device list | Run as root/admin; try `sudo arp -n` on Linux |
| Npcap error on Windows | Reinstall Npcap with WinPcap compatibility checked |
| Permission denied | Add `sudo` before `python3 main.py` |

---

## 📁 .gitignore

```
venv/
__pycache__/
*.pyc
*.pyo
wifi_report_*.txt
.env
```

---

## 👤 Author

**Nethmi** — [@Nethmiiiiii](https://github.com/Nethmiiiiii)

---

## 📜 License

This project is for **educational purposes only.**
Use responsibly and only on networks you own or have permission to test.
