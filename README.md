<div align="center">

# 🚀 DevOps Deployment Gate & Health Monitor

### *Automated Pre-Flight Validation, Microservice Health Checks, and Incident Auditing for Modern CI/CD Pipelines*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/GOWTH4M-444/python_devops_project/actions)
[![Tests](https://img.shields.io/badge/Tests-25%20Passed-success?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org)
[![Coverage](https://img.shields.io/badge/Coverage-97%25-brightgreen?style=for-the-badge)](https://github.com/GOWTH4M-444/python_devops_project)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge)](https://github.com/psf/black)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

<br/>

**A lightweight, production-grade DevOps utility designed to safeguard release cycles by validating environment variables, auditing required configurations, probing API microservices, and enforcing automated pre-deployment quality gates.**

[Features](#-key-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start-in-60-seconds) • [CLI Usage](#-cli-commands--usage) • [Custom Projects](#-testing-any-custom-project) • [CI/CD](#-cicd-pipeline-integration)

</div>

---

## 📌 Problem & Solution

In modern continuous delivery (CI/CD) environments, broken deployments frequently occur because:
- **Missing Secrets & Keys**: Environment variables (e.g., database URLs, API tokens) are unset in the target cluster.
- **Missing Required Files**: SSL/TLS certificates, license keys, or configuration manifests are absent.
- **Offline Microservices**: Upstream dependencies, databases, or payment gateways are down or timing out.

**DevOps Deployment Gate & Health Monitor** solves this by acting as an **automated pre-flight checklist**. It validates the deployment environment, tests endpoint reachability with latency tracking, writes an audit trail to disk, and halts pipelines before bad code reaches production.

---

## ⚡ Key Features

- 🛡️ **Automated Deployment Gate**: Returns exit code `0` on success and `1` on failure, integrating seamlessly as a quality gate in CI/CD pipelines.
- ⚙️ **100% Configuration-Driven**: No hardcoded application logic. Test any service, microservice, or cloud endpoint simply by supplying a YAML manifest.
- 🔍 **Pre-Flight Environment Checks**: Validates environment variables (`.env`, system env) and critical filesystem assets before release execution.
- 🌐 **Deep HTTP Health Checking**: Inspects endpoints with custom HTTP headers, methods (`GET`, `POST`), status verification, and millisecond latency telemetry.
- 📜 **Dual Synchronous Audit Logging**: Simultaneous terminal streaming and structured persistent logging in `logs/app.log`.
- 📊 **Multi-Format Reporting**: Automatically exports machine-readable JSON (`reports/report.json`) for pipeline automation and formatted TXT summaries (`reports/report.txt`) for release managers.
- 🧪 **Enterprise Test Suite**: 25 unit tests with **97% code coverage**, full mock isolation, and strict PEP 8 linting.
- 🐳 **Container & Cloud Ready**: Includes lightweight `Dockerfile`, GitHub Actions CI workflow, and Jenkins declarative pipeline.

---

## 🏗️ Architecture

```text
                             ┌──────────────────────────────┐
                             │     configs/config.yaml      │
                             │  (Environment & Target URLs) │
                             └──────────────┬───────────────┘
                                            │
                                            ▼
                             ┌──────────────────────────────┐
                             │       app/cli.py (CLI)       │
                             │ (validate | check | report)  │
                             └──────────────┬───────────────┘
                                            │
               ┌────────────────────────────┼────────────────────────────┐
               ▼                            ▼                            ▼
      ┌──────────────────┐        ┌──────────────────┐         ┌──────────────────┐
      │ app/validator.py │        │app/healthcheck.py│         │ app/reporter.py  │
      │  - Env variables │        │ - HTTP status    │         │  - report.json   │
      │  - Filesystem    │        │ - Latency (ms)   │         │  - report.txt    │
      └────────┬─────────┘        └─────────┬────────┘         └─────────┬────────┘
               │                            │                            │
               └────────────────────────────┼────────────────────────────┘
                                            ▼
                             ┌──────────────────────────────┐
                             │        app/logger.py         │
                             │  (Console & logs/app.log)    │
                             └──────────────────────────────┘
```

---

## 📁 Project Structure

```text
python_devops_project/
│
├── app/
│   ├── __init__.py           # Package marker & version info
│   ├── main.py               # Top-level executable entry point
│   ├── cli.py                # Command-line interface dispatcher
│   ├── config.py             # YAML parser & automatic .env loader
│   ├── logger.py             # Dual console and file logger (logs/app.log)
│   ├── validator.py          # Environment variables & file existence checks
│   ├── healthcheck.py        # HTTP endpoint health checks with latency
│   ├── reporter.py           # JSON and TXT report generator
│   └── utils.py              # Filesystem and system telemetry helpers
│
├── configs/
│   ├── config.yaml           # Runtime deployment configuration
│   ├── .env.example          # Environment variables template
│   └── custom_project_example.yaml # Custom project template (real internet APIs)
│
├── tests/                    # 25 Automated Unit Tests (97% Coverage)
│   ├── test_cli.py           # CLI subcommands and error handling
│   ├── test_config.py        # Config loader unit tests
│   ├── test_healthcheck.py   # Health check and network mock tests
│   ├── test_main.py          # Entry point tests
│   ├── test_reporter.py      # Report generator tests
│   ├── test_utils.py         # Utility helper tests
│   └── test_validator.py     # Environment validation logic tests
│
├── reports/                  # Generated audit artifacts
│   ├── report.json           # Machine-readable report
│   └── report.txt            # Human-readable summary
│
├── logs/                     # Persistent execution logs
│   └── app.log               # Timestamped audit trail
│
├── .github/
│   └── workflows/
│       └── ci.yml            # Automated GitHub Actions CI/CD Pipeline
│
├── Dockerfile                # Production Docker container build
├── Jenkinsfile               # Jenkins declarative pipeline definition
├── mock_service.py           # Built-in mock HTTP service for local demos
├── requirements.txt          # Pinned dependencies
├── .gitignore                # Version control exclusions
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start in 60 Seconds

### 1. Clone & Set Up Environment
```bash
# Clone the repository
git clone https://github.com/GOWTH4M-444/python_devops_project.git
cd python_devops_project

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
# Copy example environment configuration
cp configs/.env.example configs/.env
```

### 3. Run Pre-Flight Validation
```bash
python -m app.main validate
```

---

## 💻 CLI Commands & Usage

The application features a clean CLI with dedicated subcommands:

| Command | Action | Primary Use Case |
| :--- | :--- | :--- |
| `python -m app.main validate` | Validates environment variables & required files | Pre-deployment sanity gate |
| `python -m app.main check` | Pings HTTP endpoints & checks status codes | API reachability & uptime verification |
| `python -m app.main report` | Generates structured JSON & TXT summaries | Release auditing & compliance records |
| `python -m app.main all` | Runs validation, checks, and generates reports | Complete end-to-end CI/CD gate |

### Command-Line Flags
- `--config <path>`: Specify a custom YAML configuration file (default: `configs/config.yaml`).

```bash
# Run complete validation using a custom configuration:
python -m app.main all --config configs/custom_project_example.yaml
```

---

## 🌐 Testing Any Custom Project

To use this utility for **your own application** (e.g., e-commerce backend, Node.js API, Django app, or external microservice):

1. Create a custom YAML file (e.g. `configs/my_app.yaml`):

```yaml
environment: production
application_name: my-cloud-backend

required_env_vars:
  - DATABASE_URL
  - STRIPE_SECRET_KEY

health_checks:
  - name: auth_service
    url: https://jsonplaceholder.typicode.com/posts/1
    expected_status: 200

  - name: payment_gateway
    url: https://httpbin.org/get
    expected_status: 200
    headers:
      Authorization: "Bearer your-token"

paths:
  logs_dir: logs
  reports_dir: reports

timeouts:
  request_timeout: 5
```

2. Run the tool against your configuration:
```bash
python -m app.main all --config configs/my_app.yaml
```

---

## 🧪 Testing & Code Quality

The project enforces high code quality through continuous automated testing:

```bash
# Run full unit test suite
python -m pytest -v

# Run with line-by-line coverage report
python -m pytest --cov=app --cov-report=term-missing

# Verify code formatting (Black)
python -m black --check app tests

# Run linter (Flake8)
python -m flake8 app tests --max-line-length=120
```

### Test Coverage Summary:
```text
Name                 Stmts   Miss  Cover
----------------------------------------
app/healthcheck.py      34      1    97%
app/logger.py           16      0   100%
app/reporter.py         41      0   100%
app/utils.py            14      0   100%
app/validator.py        24      0   100%
app/cli.py              40      2    95%
app/config.py           18      2    89%
----------------------------------------
TOTAL                  192      6    97%
```

---

## 🐳 Docker Deployment

Run the validation tool inside an isolated, containerized environment:

```bash
# Build the Docker image
docker build -t python-devops-project .

# Run the container with environment configuration
docker run --rm --env-file configs/.env python-devops-project

# Persist generated reports to host machine
docker run --rm --env-file configs/.env -v ${PWD}/reports:/project/reports python-devops-project
```

---

## 🔄 CI/CD Pipeline Integration

### GitHub Actions
The repository includes an automated workflow in `.github/workflows/ci.yml`:
1. **Quality Check**: Enforces `black` formatting and `flake8` lint rules.
2. **Automated Testing**: Executes the `pytest` test suite with coverage reporting.
3. **Pre-Flight Gate**: Boots a mock target server and runs `python -m app.main all`.
4. **Artifact Archival**: Automatically uploads `reports/` and `logs/` for download upon pipeline completion.

---

## 📄 Output Reports Preview

### Formatted TXT Report (`reports/report.txt`)
```text
============================================================
Deployment Environment Report
============================================================
Generated: 2026-10-12T04:53:37.923644+00:00
Overall Status: SUCCESS
Validation Passed: True
------------------------------------------------------------
Health Check Results:
  [PASS] homepage: URL=http://localhost:5000/ | Status Code=200 | Expected=200
  [PASS] health: URL=http://localhost:5000/health | Status Code=200 | Expected=200
============================================================
```

### Machine-Readable JSON (`reports/report.json`)
```json
{
    "timestamp": "2026-10-12T04:53:37.923644+00:00",
    "status": "SUCCESS",
    "validation_passed": true,
    "health_checks": [
        {
            "name": "homepage",
            "url": "http://localhost:5000/",
            "status_code": 200,
            "expected_status": 200,
            "response_time_ms": 1.42,
            "success": true
        }
    ],
    "summary": {
        "total_health_checks": 1,
        "passed_health_checks": 1,
        "failed_health_checks": 0
    }
}
```

---

## 👤 Author

**Gowtham P**  
- GitHub: [@GOWTH4M-444](https://github.com/GOWTH4M-444)  
- Project Repository: [python_devops_project](https://github.com/GOWTH4M-444/python_devops_project)

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
