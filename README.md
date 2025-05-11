<h1 align="center">🛡️ Phishing Analyzer</h1>

<p align="center">
  A web-based phishing email and URL analyzer with VirusTotal integration, PCAP capture, and log history.
</p>

<p align="center">
  <img src="https://github.com/maxcheung89/phishing-analyzer/blob/main/51_20%20PM.png?raw=true" width="700" alt="Lincense & All right received by $Maxcheung89">
</p>

---
## License

All rights reserved. This project is the sole work of @maxcheung89, and unauthorized use, copying, or distribution is strictly prohibited without express written permission.

## 🚀 Features

- 📎 Upload `.eml` files or paste phishing URLs
- 🔍 Extract embedded links from emails
- 🧪 Analyze headers with `curl` and scan with VirusTotal
- 🐚 Scan files with ClamAV
- 🧠 Generate PCAP files using `tshark`
- 📥 Download logs and PCAPs from the browser
- 📊 View historical scan results via SQLite
- 🐳 Docker-powered & self-contained

---

## 🧰 Prerequisites

- [Docker](https://www.docker.com/)
- A [VirusTotal API Key](https://www.virustotal.com/gui/join-us)

---

## 📦 Installation

```bash
git clone https://github.com/maxcheung89/phishing-analyzer.git
cd phishing-analyzer
```

---

## 🔐 Configuration

Create a `.env` file:

```bash
touch .env
echo "VT_API_KEY=your_virustotal_api_key" >> .env
```

> ⚠️ Keep `.env` private and **never commit** it to GitHub.

---

## 🔧 Run It (Two Options)

### 🔹 Option 1: Makefile

```bash
make build     # Build the Docker image
make run       # Start the container at http://localhost:5000
```

### 🔹 Option 2: Bash Script

```bash
chmod +x run.sh
./run.sh
```

---

## 🌐 Usage

Go to [http://localhost:5000](http://localhost:5000):

- Paste a suspicious URL **OR**
- Upload a `.eml` phishing email

You'll get:

- ✅ VirusTotal scan results
- 📝 Downloadable analysis logs
- 📡 PCAPs of network capture
- ⏱️ SQLite-backed scan history

---

## 📂 Project Structure

```text
phishing-analyzer/
├── backend/
│   ├── app.py             ← Flask Web App
│   ├── analyzer.py        ← Analysis Functions (tshark, curl, clamav)
│   ├── vt.py              ← VirusTotal API Integration
│   ├── db.py              ← SQLite Log Recorder
│   └── static/results/    ← Output Folder
│
├── templates/
│   ├── index.html         ← UI Form
│   └── history.html       ← Log History Table
│
├── .env                   ← 🔐 VirusTotal API Key
├── Dockerfile             ← Docker Image Definition
├── requirements.txt       ← Python Dependencies
├── Makefile               ← Build & Run Helpers
└── run.sh                 ← All-in-One Launcher
```

---

## 🐛 Known Issues

- PCAP may fail if container lacks `NET_ADMIN` capability  
- tshark logs warning: _“cap_set_proc() fail return: Operation not permitted”_ → safe to ignore  
- Ensure `curl`, `clamav`, and `tshark` are installed in container

---

## 🛠️ TODO (Open Contributions!)

- 🧠 Threat Scoring System
- 🌍 WHOIS or GeoIP integration
- 🔁 Periodic re-scan scheduler
- 📊 Visual charts (charts.js / Plotly)

---

## 📜 License

MIT License

Copyright (c) 2025 @maxcheung89

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED...


---

## 📣 Like this project?

🌟 Star it on [GitHub](https://github.com/yourusername/phishing-analyzer)  
