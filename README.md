```markdown
<div align="center">

# 👻 GHOSTTRACE v2.0

### Advanced Network Routing • Proxy Chain Orchestration • Traffic Analysis

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-black?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/Version-v2.0-success?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Status-Active%20Development-orange?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge" alt="License">
</p>

<br>

<p>
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=3000&pause=1000&color=00FF88&center=true&vCenter=true&width=800&lines=%E2%96%BA+Dynamic+Multi-Hop+Proxy+Chaining;%E2%96%BA+Automated+Proxy+Discovery+%26+Validation;%E2%96%BA+Real-Time+Route+Visualization;%E2%96%BA+Identity+Rotation+%26+Fingerprint+Profiles;%E2%96%BA+Modular+Plugin+Architecture+with+REST+API" alt="Typing SVG">
</p>

</div>

---

### 🔍 What is GhostTrace?

GhostTrace is a **production‑ready framework** that turns complex proxy‑chain orchestration into an **observable, automated pipeline**.  
It collects, validates, chains and rotates network routes while giving you full visual and programmatic control.

Built for **security researchers, developers, network analysts and privacy professionals** who need reliable, measurable routing – not black‑box magic.

---

## 📑 Navigate

<div align="center">

| [🌍 Overview](#-what-is-ghosttrace) | [✨ Features](#-feature-radar) | [🏗 Architecture](#-system-blueprint) | [💾 Install](#-setup) |
|-------------------------------------|-------------------------------|--------------------------------------|-----------------------|
| [⚡ Quick Start](#-launch) | [📊 Dashboard](#-live-dashboard) | [🔧 Config](#-configuration-file) | [🧪 Test](#-test-suite) |
| [🗺 Roadmap](#-roadmap) | [🤝 Contribute](#-contribution-flow) | [⚠ Disclaimer](#-disclaimer) | [📜 License](#-license) |

</div>

---

## ✨ Feature Radar

GhostTrace is built around **six independent, composable domains**. Each domain solves a specific piece of the routing puzzle.

<table>
<tr>
<td width="50%">

### 🔗 Dynamic Routing Engine
- Build **multi‑hop chains** (2–4 hops) from live, validated endpoints  
- Automatic **failover** when a node becomes unreachable  
- **Latency‑aware** endpoint selection  
- Protocol support: `HTTP`, `HTTPS`, `SOCKS4`, `SOCKS5`

</td>
<td width="50%">

### 🌐 Proxy Harvesting
- Aggregate from **public lists, APIs, and custom URLs**  
- Deduplication and **anonymity scoring**  
- **Geographic filtering** (include/exclude by country)  
- Automatic periodic refresh

</td>
</tr>
<tr>
<td width="50%">

### 🧪 Validation Pipeline
- **Parallel health checks** (up to 50 concurrent)  
- Speed, connectivity, and **anonymity verification**  
- Configurable timeouts, retries and thresholds  
- Historical uptime tracking

</td>
<td width="50%">

### 🔄 Identity & Fingerprint Rotation
- **Time‑based** and **event‑driven** rotation strategies  
- Fingerprint profiles (Chrome, Firefox, custom) that rotate with the chain  
- Seamless session continuity across rotations  
- Full audit log

</td>
</tr>
<tr>
<td width="50%">

### 📊 Observability & API
- **Real‑time web dashboard** with live log streaming  
- Full **REST API** (FastAPI) + **WebSocket** endpoint  
- Export metrics to JSON, CSV, PDF  
- Rate‑limited, CORS‑configurable

</td>
<td width="50%">

### 🧩 Modular Plugins
- Isolated, replaceable components  
- Custom proxy sources, validators, and rotation strategies  
- Tor integration as an optional plugin  
- Clean interfaces for community extensions

</td>
</tr>
</table>

---

## 🏗 System Blueprint

<div align="center">
  <pre style="text-align: center; background: none; border: none; color: #00FF88; font-weight: bold;">
┌──────────────────────────────────────────────────────────────┐
│                   GHOSTTRACE CORE ENGINE                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│   │ ROUTING  │  │ SESSION  │  │FINGERPRNT│  │   TOR    │   │
│   │ MANAGER  │  │   CTRL   │  │ MANAGER  │  │  LAYER   │   │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│        │             │             │             │          │
│        └─────────────┼─────────────┼─────────────┘          │
│                      │             │                        │
│               ┌──────┴─────────────┴──────┐                 │
│               │   ORCHESTRATION BUS       │                 │
│               └──────┬─────────────┬──────┘                 │
│                      │             │                        │
│        ┌─────────────┼─────────────┼─────────────┐          │
│        │             │             │             │          │
│   ┌────┴────┐   ┌────┴────┐   ┌────┴────┐   ┌───┴────┐    │
│   │VALIDATE │   │ PROXY   │   │DASHBOARD│   │REPORTS │    │
│   │ ENGINE  │   │COLLECTOR│   │   API   │   │        │    │
│   └─────────┘   └─────────┘   └─────────┘   └────────┘    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
  </pre>
</div>

The architecture keeps concerns strictly separated. The **Orchestration Bus** connects all components without tight coupling, making it easy to swap or extend any module.

---

## 💾 Setup

### Prerequisites
- **Python 3.10+**
- **Git**
- **pip**
- Tor (optional – for onion routing)

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-org/ghosttrace.git
cd ghosttrace

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows

# 3. Install core dependencies
pip install -r requirements.txt

# 4. Verify installation
python ghost.py --version
```

### Core Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | REST API server |
| `uvicorn` | ASGI server |
| `aiohttp` | Async HTTP client |
| `requests` | Sync HTTP operations |
| `pysocks` | SOCKS proxy support |
| `pyyaml` | Configuration parsing |
| `rich` | Terminal output formatting |
| `websockets` | Real‑time dashboard streaming |
| `pydantic` | Data validation & settings |

---

## ⚡ Launch

<div align="center">

| Platform | Command |
|----------|---------|
| 🪟 Windows | `run.bat` |
| 🐧 Linux | `chmod +x run.sh && ./run.sh` |
| 🍎 macOS | `chmod +x run.sh && ./run.sh` |

</div>

### Common Commands

```bash
# Interactive mode
python ghost.py

# Build a quick 3-hop chain
python ghost.py --chain --hops 3

# Validate a custom proxy list
python ghost.py --validate proxies.txt

# Start dashboard only
python ghost.py --dashboard

# Full stack with 120s rotation interval
python ghost.py --full --rotation-interval 120
```

### REST API (FastAPI on port `8000`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/status` | System health & metrics |
| `GET` | `/api/proxies` | Available proxy pool |
| `POST` | `/api/chain` | Build new routing chain |
| `PUT` | `/api/rotate` | Trigger identity rotation |
| `GET` | `/api/sessions` | Active session list |
| `WS` | `/ws/live` | Real‑time log stream |

---

## 📊 Live Dashboard

The dashboard (default `http://127.0.0.1:5000`) gives you **total situational awareness** without touching the CLI.

<div align="center">
  <pre style="text-align: center; background: #0D1117; color: #C9D1D9; padding: 10px; border-radius: 6px;">
┌────────────────────────────────────────────┐
│         GHOSTTRACE DASHBOARD               │
│         http://127.0.0.1:5000              │
├────────────────────────────────────────────┤
│                                            │
│  📡 Runtime Status    🗺 Route Map         │
│  📈 Session Stats     🌐 Proxy Pool        │
│  🔍 Diagnostics       📝 Live Logs         │
│  ⚙️ Configuration     📊 Performance       │
│                                            │
└────────────────────────────────────────────┘
  </pre>
</div>

| Panel | What you see | Refresh |
|-------|---------------|---------|
| Status | Uptime, active chains, health | Real‑time |
| Route Map | Graphical multi‑hop path | On change |
| Proxy Pool | Live count & health of proxies | 30s |
| Logs | Streaming log viewer | Live |
| Metrics | Latency, throughput, errors | 10s |

---

## 🔧 Configuration File

All behaviour is driven by a single `config.yaml`. Below is a **fully annotated example**.

```yaml
system:
  log_level: INFO
  data_dir: ./data
  temp_dir: /tmp/ghost

routing:
  enabled: true
  default_protocol: socks5
  connection_timeout: 30
  max_retries: 3

proxy_chain:
  min_length: 2
  max_length: 4
  require_unique_countries: true
  exclude_countries: [CN, RU]

rotation:
  enabled: true
  interval: 60
  strategy: round_robin       # round_robin, random, weighted
  on_failure: fallback

validation:
  parallel_checks: 50
  test_urls:
    - https://httpbin.org/ip
    - https://api.ipify.org
  speed_threshold: 5000
  anonymity_checks: true

proxy_sources:
  enabled: [proxyscrape, proxy_list_download, free_proxy_list]
  custom_urls: []
  update_interval: 3600

tor:
  enabled: false
  control_port: 9051
  socks_port: 9050
  auto_renew_circuit: true

fingerprint:
  rotation_with_proxy: true
  profiles_dir: ./profiles
  default_profile: chrome_windows

dashboard:
  enabled: true
  host: 127.0.0.1
  port: 5000
  auth_required: false
  theme: dark

api:
  enabled: true
  host: 127.0.0.1
  port: 8000
  rate_limit: 100
  cors_origins: [http://localhost:5000]
```

---

## 🧪 Test Suite

Run the full suite to verify integrity after changes.

```bash
# All tests with verbose output
pytest tests/ -v --tb=long

# Specific module
pytest tests/test_routing.py -v

# Coverage report
pytest tests/ --cov=ghosttrace --cov-report=html

# Quick smoke test
python ghost.py --test
```

<div align="center">

| Module | Tests | Coverage |
|--------|-------|----------|
| Routing Engine | 45 | 94% |
| Proxy Collector | 32 | 91% |
| Validation | 28 | 96% |
| Session Manager | 21 | 89% |
| Dashboard API | 38 | 93% |
| Fingerprint Manager | 15 | 87% |

</div>

---

## 🗺 Roadmap

**v2.1** — *Q3 2026*
- [x] Advanced analytics with historical charts
- [x] PDF/HTML export templates
- [x] Additional validation providers (Whoer, IPQualityScore)
- [x] Docker Compose support

**v2.2** — *Q4 2026*
- [ ] Plugin marketplace with community submissions
- [ ] Distributed validation workers
- [ ] gRPC API endpoint
- [ ] Kubernetes manifests

**v2.3** — *Q1 2027*
- [ ] ML‑based proxy scoring
- [ ] Automatic chain optimization
- [ ] Desktop GUI (Electron)
- [ ] Cloud orchestration service

---

## 🤝 Contribution Flow

<div align="center">
  <pre style="text-align: center; background: none; border: none; font-weight: bold;">
1️⃣ Fork Repository
        ↓
2️⃣ Create Feature Branch
        ↓
3️⃣ Implement Changes
        ↓
4️⃣ Write/Update Tests
        ↓
5️⃣ Run Full Test Suite
        ↓
6️⃣ Submit Pull Request
  </pre>
</div>

**Rules of the road:**
- Follow existing code style and module boundaries
- Include tests for every new feature
- Keep commits atomic and use Conventional Commits
- Update documentation for any user‑facing change

---

## ⚠ Disclaimer

<div align="center">
  <pre style="text-align: center; background: none; border: 2px solid #FF5555; color: #FF5555; padding: 10px;">
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  GhostTrace is for AUTHORISED USE ONLY:                  ║
║  🔬 Security Research   📚 Education                     ║
║  🔧 Network Testing     ✅ Authorised Environments       ║
║                                                          ║
║  ⛔ UNAUTHORISED USE IS STRICTLY PROHIBITED              ║
║                                                          ║
║  You are fully responsible for compliance with all       ║
║  applicable laws. The developers assume NO LIABILITY     ║
║  for misuse.                                             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
  </pre>
</div>

---

## 📜 License

<div align="center">

```
MIT License

Copyright (c) 2026 GhostTrace Development Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction...
```

</div>

---

<div align="center">
  <pre style="text-align: center; background: none; border: none; color: #00FF88; font-size: 14px;">
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
██║  ███╗███████║██║   ██║███████╗   ██║
██║   ██║██╔══██║██║   ██║╚════██║   ██║
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝
  </pre>

**Routing excellence. Automated. Observable. Reliable.**

<sub>© 2026 GhostTrace Project • All Rights Reserved</sub>
</div>
```
