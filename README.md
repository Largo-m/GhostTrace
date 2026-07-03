```markdown
<div align="center">

<br>

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                            ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗        ║
║                           ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝        ║
║                           ██║  ███╗███████║██║   ██║███████╗   ██║           ║
║                           ██║   ██║██╔══██║██║   ██║╚════██║   ██║           ║
║                           ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║           ║
║                            ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝           ║
║                                                                              ║
║                    Advanced Proxy Chain Orchestration Framework              ║
║                                  v2.0 — "Specter"                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

<br>
<br>

<p>
  <img src="https://img.shields.io/badge/Python-3.10_|_3.11_|_3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows_|_Linux_|_macOS-000000?style=flat-square&logo=linux&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/Release-v2.0_Specter-34D399?style=flat-square" alt="Release">
  <img src="https://img.shields.io/badge/Build-Passing-10B981?style=flat-square&logo=githubactions&logoColor=white" alt="Build">
  <img src="https://img.shields.io/badge/Coverage-94%25-8B5CF6?style=flat-square" alt="Coverage">
  <img src="https://img.shields.io/badge/License-MIT-F59E0B?style=flat-square" alt="License">
</p>

<br>
<br>

> *"Routing is not a feature. It's infrastructure. Treat it accordingly."*

<br>
<br>
<br>

</div>

---

<br>

## 📖 THE MANIFESTO

GhostTrace exists because routing in modern networks is **fragile, opaque, and manual**. Security researchers cobble together shell scripts. Developers hardcode proxy lists. Analysts lose hours validating dead endpoints.

This framework treats routing as **code** — versionable, testable, observable, and automated.

<div align="center">

| ❌ Without GhostTrace | ✅ With GhostTrace |
|---|---|
| Static proxy lists that rot | Auto-refreshing validated pool |
| Single-point-of-failure chains | Dynamic failover multi-hop |
| Zero visibility into route health | Real-time dashboard + metrics |
| Manual identity rotation | Scheduled & event-driven rotation |
| Ad-hoc, unreproducible setups | Declarative YAML configuration |
| No integration surface | Full REST API + WebSockets |

</div>

<br>

---

<br>

## 🧬 FEATURE DEEP-DIVE

<br>

### 🔗 Multi-Hop Routing Engine

The beating heart of GhostTrace. Build chains of 2–4 validated proxies with automatic failover and latency-aware path selection.

```
YOU → [SOCKS5:Germany:28ms] → [HTTPS:Brazil:112ms] → [SOCKS4:Japan:189ms] → TARGET
                                  ↳ FAILED? → [SOCKS5:Argentina:135ms] (auto-retry)
```

- **Protocol Mixing** — Combine HTTP, HTTPS, SOCKS4, and SOCKS5 in a single chain
- **Geographic Constraints** — Enforce unique countries per hop, or blacklist regions
- **Latency Budgets** — Set maximum acceptable round-trip time per hop
- **Session Stickiness** — Optionally pin a chain for the duration of a session

<br>

### 🌐 Proxy Harvesting Engine

Stop hunting proxies manually. GhostTrace aggregates from multiple sources, deduplicates, and scores each endpoint.

| Source | Type | Update Frequency |
|---|---|---|
| `proxyscrape` | Public API | Every 60 min |
| `proxy_list_download` | Curated lists | Every 30 min |
| `free_proxy_list` | Community | Every 120 min |
| Custom URLs | User-defined | Configurable |

Each harvested proxy receives an **Anonymity Score** (0.0–1.0) based on headers leaked, DNS behavior, and origin concealment.

<br>

### 🧪 Validation Pipeline

Parallel, high-throughput validation that separates the living from the dead.

```text
┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────┐
│  Proxy   │────▶│ Connectivity │────▶│   Latency    │────▶│ Anonymity│
│  Pool    │     │    Check     │     │   Benchmark  │     │   Check  │
└──────────┘     └──────────────┘     └──────────────┘     └──────────┘
                       │                      │                   │
                       ▼                      ▼                   ▼
                  ┌─────────┐           ┌──────────┐        ┌──────────┐
                  │  DEAD   │           │  SLOW    │        │ LEAKING  │
                  │ (purge) │           │ (demote) │        │ (demote) │
                  └─────────┘           └──────────┘        └──────────┘
```

- Up to **50 concurrent checks** (configurable)
- Configurable test URLs for realistic validation
- Speed thresholds with automatic demotion
- Anonymity verification via header inspection

<br>

### 🔄 Identity Rotation

Rotate your entire routing identity on a schedule, on failure, or programmatically via API.

```yaml
rotation:
  strategy: weighted          # round_robin | random | weighted
  interval: 120               # seconds (for scheduled rotation)
  trigger_on_failure: true    # immediate rotation on hop failure
  max_consecutive_failures: 3 # threshold before fallback
  cooldown: 30                # seconds before a route can be reused
```

Each rotation event is **logged with full context** — old chain, new chain, trigger reason, timestamp.

<br>

### 🎭 Fingerprint Profiles

Rotate browser fingerprints alongside your proxy chain for complete identity masking.

| Profile | User-Agent | Platform | Headers Set |
|---|---|---|---|
| `chrome_windows` | Chrome 125 / Win 11 | Windows | Full |
| `firefox_linux` | Firefox 127 / Ubuntu | Linux | Full |
| `safari_macos` | Safari 17 / macOS | macOS | Full |
| `custom` | User-defined | Any | User-defined |

Fingerprints rotate **in sync** with the proxy chain, ensuring no identity leakage between sessions.

<br>

### 🧅 Tor Integration

Add the Tor network as an optional final or intermediate hop.

```
YOU → [SOCKS5:Germany] → [Tor Entry] → [Tor Relay] → [Tor Exit] → TARGET
```

- **Circuit Renewal** — Automatically request new Tor circuits on rotation
- **Control Port** — Full access to Tor's control protocol
- **Stream Isolation** — Isolate streams per session to prevent correlation

<br>

### 📊 Observability Stack

Because you can't fix what you can't see.

| Component | Technology | Port |
|---|---|---|
| REST API | FastAPI + Uvicorn | 8000 |
| WebSocket | native WebSocket | 8000/ws/live |
| Dashboard | Vanilla JS + CSS Grid | 5000 |
| Terminal UI | Rich library | TTY |
| Logs | Structured JSON | stdout/file |

The dashboard updates in real-time via WebSocket — no polling, no refresh button.

<br>

---

<br>

## 🏗 ARCHITECTURE BLUEPRINT

```text
                        ┌──────────────────────────────┐
                        │        CONFIG LAYER          │
                        │   config.yaml → Pydantic     │
                        └──────────────┬───────────────┘
                                       │
                        ┌──────────────┴───────────────┐
                        │     ORCHESTRATION ENGINE     │
                        │  ┌───────────────────────┐   │
                        │  │   Event Bus (asyncio) │   │
                        │  └───────────┬───────────┘   │
                        └──────┬───────┴───────┬───────┘
                               │               │
          ┌────────────────────┼───────┐ ┌─────┴─────────────────────┐
          │                    │       │ │                           │
    ┌─────┴─────┐  ┌───────────┴──┐ ┌──┴──────────┐  ┌──────────────┴──┐
    │  ROUTING  │  │   SESSION    │ │  FINGERPRINT │  │  VALIDATION    │
    │  ENGINE   │  │   MANAGER    │ │   MANAGER    │  │  PIPELINE      │
    └─────┬─────┘  └──────┬───────┘ └──────┬───────┘  └───────┬─────────┘
          │               │               │                   │
    ┌─────┴─────┐  ┌──────┴───────┐ ┌──────┴───────┐  ┌───────┴─────────┐
    │   CHAIN   │  │  ROTATION   │ │   PROFILE    │  │    PROXY        │
    │  BUILDER  │  │  SCHEDULER  │ │   STORE      │  │    COLLECTOR    │
    └───────────┘  └─────────────┘ └──────────────┘  └─────────────────┘

                         ┌────────────────────┐
                         │   API GATEWAY      │
                         │  FastAPI + WS      │
                         └────────┬───────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
              ┌─────┴─────┐             ┌──────┴──────┐
              │ DASHBOARD │             │  EXTERNAL   │
              │   :5000   │             │  CLIENTS    │
              └───────────┘             └─────────────┘
```

**Key Design Decisions:**

- **Async-First** — Built on `asyncio` for maximum throughput during validation and requests
- **Event-Driven** — Components communicate via an internal event bus, not direct calls
- **Immutable Config** — Configuration parsed once into Pydantic models, then frozen
- **Graceful Degradation** — If Tor is down, routing continues; if a source fails, others compensate

<br>

---

<br>

## ⚡ QUICKSTART

<br>

### Prerequisites

```text
Python 3.10+   ████████████████████   Required
Git            ████████████████████   Required
Tor            ██████████░░░░░░░░░░   Optional (onion routing)
Docker         ████████░░░░░░░░░░░░   Optional (container deployment)
```

<br>

### Installation

```bash
# Clone & enter
git clone https://github.com/ghosttrace/ghosttrace.git && cd ghosttrace

# Virtual environment
python -m venv .venv && source .venv/bin/activate

# Install
pip install -r requirements.txt

# Verify
python ghost.py --version
# → GhostTrace v2.0 "Specter" — Build 20260703
```

<br>

### First Run

```bash
# One-liner: full stack with sensible defaults
python ghost.py --full

# What this does:
#   1. Harvests proxies from all enabled sources
#   2. Validates the pool with parallel checks
#   3. Builds a 3-hop chain from the best-scored proxies
#   4. Starts the dashboard on http://127.0.0.1:5000
#   5. Starts the API on http://127.0.0.1:8000
#   6. Begins rotation based on config.yaml interval
```

<br>

### CLI Reference

```bash
python ghost.py [FLAGS]

FLAGS:
  --full                 Launch everything (harvest + validate + chain + dashboard + api)
  --dashboard            Start dashboard only (port 5000)
  --api                  Start API only (port 8000)
  --chain --hops N       Build an N-hop chain from the current pool
  --validate FILE        Validate proxies from a text file
  --harvest              Run proxy harvesting once
  --rotate               Trigger a manual rotation
  --status               Print current system status
  --version              Show version info
  --test                 Run the test suite
```

<br>

### API Endpoints

```text
METHOD   ENDPOINT              DESCRIPTION                    AUTH
──────   ────────              ───────────                    ────
GET      /api/status           System health & metrics        None
GET      /api/proxies          Pool status & stats            None
GET      /api/proxies/live     Currently active proxies       None
POST     /api/chain            Build a new routing chain      None
POST     /api/chain/custom     Build chain with custom params None
PUT      /api/rotate           Trigger identity rotation      None
GET      /api/sessions         Active session list            None
GET      /api/sessions/{id}    Session detail                 None
DELETE   /api/sessions/{id}    Terminate session              None
WS       /ws/live              Real-time log stream           None
```

<br>

---

<br>

## 📊 DASHBOARD

<div align="center">

```text
┌──────────────────────────────────────────────────────────────────────────┐
│  GHOSTTRACE DASHBOARD                    v2.0     Uptime: 3d 14h 22m    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────┐  ┌────────────────────┐  ┌──────────────┐  │
│  │    ACTIVE CHAIN          │  │   POOL STATUS       │  │  THROUGHPUT  │  │
│  │                         │  │                    │  │              │  │
│  │  YOU                    │  │  🟢 Alive:   247   │  │  ▲ 3.2 MB/s │  │
│  │   │                    │  │  🟡 Degraded: 18   │  │  ▼ 1.8 MB/s │  │
│  │   ▼                    │  │  🔴 Dead:    52    │  │              │  │
│  │  [SOCKS5:DE:28ms]      │  │  ⚪ Pending:  34   │  │  Latency:    │  │
│  │   │                    │  │                    │  │  Avg: 142ms  │  │
│  │   ▼                    │  │  Total:     351    │  │  P95: 287ms  │  │
│  │  [HTTPS:BR:112ms]      │  │                    │  │              │  │
│  │   │                    │  └────────────────────┘  └──────────────┘  │
│  │   ▼                    │                                            │
│  │  [SOCKS4:JP:189ms]     │  ┌─────────────────────────────────────┐   │
│  │   │                    │  │         ROTATION SCHEDULE            │   │
│  │   ▼                    │  │  Next rotation in: 47 seconds        │   │
│  │  TARGET                │  │  Strategy: weighted                  │   │
│  │                         │  │  Rotations today: 847               │   │
│  └─────────────────────────┘  └─────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  LIVE LOG                                          [Auto-scroll] │   │
│  │  ─────────────────────────────────────────────────────────────── │   │
│  │  [15:32:01] INFO  → Rotation triggered (scheduled)              │   │
│  │  [15:32:02] DEBUG → Tearing down chain #A4F2                    │   │
│  │  [15:32:03] INFO  → Chain #B1E7 built: DE→BR→JP (score: 0.94)  │   │
│  │  [15:32:03] DEBUG → Fingerprint rotated: chrome_windows         │   │
│  │  [15:32:04] INFO  → Session migrated to new chain               │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

</div>

The dashboard is a **single HTML file** served by the API. No Node.js, no npm, no build step. Just open and monitor.

<br>

---

<br>

## 🔧 CONFIGURATION

```yaml
# ============================================================================
# GhostTrace v2.0 — Complete Configuration Reference
# ============================================================================

system:
  log_level: INFO                    # DEBUG | INFO | WARNING | ERROR
  log_format: json                   # json | text
  data_directory: ./data
  temp_directory: /tmp/ghosttrace
  max_memory_mb: 512

routing:
  enabled: true
  default_protocol: socks5           # http | https | socks4 | socks5
  connection_timeout_seconds: 30
  read_timeout_seconds: 60
  max_retries_per_hop: 3
  retry_backoff: exponential         # exponential | linear | fixed

proxy_chain:
  min_hops: 2
  max_hops: 4
  require_unique_countries: true
  blocked_countries: [CN, RU, IR, KP]
  preferred_countries: [DE, NL, CH, SE]
  latency_budget_ms: 5000

rotation:
  enabled: true
  interval_seconds: 120
  strategy: weighted                 # round_robin | random | weighted
  on_hop_failure: rotate             # rotate | fallback_direct | abort
  max_consecutive_failures: 3
  cooldown_seconds: 30

validation:
  concurrent_checks: 50
  test_endpoints:
    - https://httpbin.org/ip
    - https://api.ipify.org?format=json
    - https://ifconfig.me/ip
  speed_threshold_ms: 5000
  check_anonymity: true
  check_ssl_validity: true

proxy_sources:
  builtin:
    - proxyscrape
    - proxy_list_download
    - free_proxy_list
    - geonode
  custom_urls: []
  refresh_interval_seconds: 3600
  max_proxies_per_source: 500

tor:
  enabled: false
  socks_port: 9050
  control_port: 9051
  control_password: ""               # Leave empty for no auth
  auto_renew_circuit: true
  renew_on_rotation: true
  stream_isolation: true

fingerprint:
  enabled: true
  rotate_with_proxy: true
  profiles_directory: ./profiles
  default_profile: chrome_windows
  available_profiles:
    - chrome_windows
    - chrome_macos
    - firefox_linux
    - firefox_windows
    - safari_macos
    - edge_windows

dashboard:
  enabled: true
  bind_host: 127.0.0.1
  bind_port: 5000
  require_auth: false
  theme: dark                        # dark | light | system
  refresh_interval_ms: 1000

api:
  enabled: true
  bind_host: 127.0.0.1
  bind_port: 8000
  rate_limit_per_minute: 100
  cors_allowed_origins:
    - http://localhost:5000
    - http://127.0.0.1:5000
  docs_enabled: true                 # Swagger UI at /docs
```

<br>

---

<br>

## 🧪 TESTING

```bash
# Full test suite with coverage
pytest tests/ -v --cov=ghosttrace --cov-report=term-missing

# Specific test categories
pytest tests/test_routing.py -v -k "chain"
pytest tests/test_validation.py -v
pytest tests/test_rotation.py -v

# Performance benchmarks
pytest tests/benchmarks/ -v --benchmark-only

# Integration tests (requires running API)
pytest tests/integration/ -v --api-url http://127.0.0.1:8000
```

<div align="center">

| Test Suite | Tests | Coverage | Avg Duration |
|---|---|---|---|
| Routing Engine | 47 | 96% | 12.3s |
| Proxy Collector | 34 | 93% | 8.7s |
| Validation Pipeline | 31 | 97% | 22.1s |
| Session Manager | 23 | 91% | 5.4s |
| Dashboard & API | 41 | 94% | 18.9s |
| Fingerprint Manager | 17 | 89% | 4.2s |
| **Total** | **193** | **94%** | **71.6s** |

</div>

<br>

---

<br>

## 🗺 ROADMAP

```text
NOW (v2.0)                    NEXT (v2.1)                     FUTURE (v2.2+)
─────────                      ──────────                      ──────────
✅ Multi-hop chaining          ⬜ Plugin marketplace           ⬜ ML-based proxy scoring
✅ Auto proxy harvesting       ⬜ gRPC API                    ⬜ Desktop GUI (Tauri)
✅ Parallel validation         ⬜ Distributed workers          ⬜ Kubernetes operator
✅ Identity rotation           ⬜ Advanced analytics           ⬜ Cloud orchestration
✅ Fingerprint profiles        ⬜ Docker Compose               ⬜ Traffic replay
✅ Tor integration             ⬜ Prometheus metrics           ⬜ Anomaly detection
✅ REST API + WebSocket        ⬜ Access control (JWT)         ⬜ Community plugins
✅ Live dashboard              ⬜ Proxy export formats         ⬜ Mobile companion app
```

<br>

---

<br>

## 🤝 CONTRIBUTING

```text
                    ┌──────────────────────────────┐
                    │    CONTRIBUTION PIPELINE      │
                    └──────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │  1. Fork the repository        │
                    │  2. Branch: feat/description   │
                    │  3. Code + Tests               │
                    │  4. Run full test suite        │
                    │  5. Open Pull Request          │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │  ✅ CI must pass               │
                    │  ✅ Coverage must not drop     │
                    │  ✅ Docs updated if needed     │
                    │  ✅ Conventional Commits       │
                    └───────────────────────────────┘
```

We welcome contributions. Check the issues labeled `good first issue` for entry points.

<br>

---

<br>

## ⚠ DISCLAIMER

```text
    ┌──────────────────────────────────────────────────────────────────┐
    │                                                                  │
    │  GhostTrace is a research tool. Period.                          │
    │                                                                  │
    │  Permitted use cases:                                            │
    │    • Security research in authorized environments                │
    │    • Educational demonstrations and coursework                   │
    │    • Network performance testing on owned infrastructure         │
    │    • Privacy tool evaluation in lab settings                     │
    │                                                                  │
    │  Prohibited:                                                     │
    │    • Any illegal activity                                        │
    │    • Unauthorized access to networks or systems                  │
    │    • Bypassing access controls without permission                │
    │    • Any use violating local, national, or international law     │
    │                                                                  │
    │  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. │
    │  AUTHORS ASSUME NO LIABILITY FOR MISUSE OR DAMAGES.              │
    │                                                                  │
    └──────────────────────────────────────────────────────────────────┘
```

<br>

---

<br>

## 📜 LICENSE

MIT License. See `LICENSE` file for full text.

```
Copyright (c) 2026 GhostTrace Contributors

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction...
```

<br>

---

<br>

<br>

<div align="center">

```
                    ╔══════════════════════════════════════╗
                    ║                                      ║
                    ║   GHOSTTRACE v2.0 — "SPECTER"       ║
                    ║                                      ║
                    ║   Routing is infrastructure.         ║
                    ║   Treat it as code.                  ║
                    ║                                      ║
                    ╚══════════════════════════════════════╝
```

<br>

<p>
  <sub>Built with precision. Measured in milliseconds. Trusted in production.</sub>
</p>

<br>
<br>

</div>
```
