# 🔐 DevSecOps CI/CD Pipeline with Security Scanning

> **MCA Final Year Project** — A production-grade DevSecOps pipeline integrating automated security scanning at every stage of CI/CD using GitHub Actions, Semgrep, OWASP Dependency-Check, and Trivy.

---

## 📌 Project Overview

This project demonstrates the **"Shift-Left Security"** approach — embedding security checks early in the software development lifecycle (SDLC) rather than treating security as an afterthought at the end.

The pipeline automatically runs on every `git push` and `pull request`, enforcing security gates before code reaches production.

---

## 🏗️ Architecture

```
Developer Push
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GitHub Actions Pipeline                       │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────────────┐  │
│  │  Stage 1 │   │  Stage 2 │   │  Stage 3 │   │  Stage 4   │  │
│  │  🧪 Test │──▶│ 🔍 SAST  │   │ 📦 SCA  │──▶│ 🐳 Build  │  │
│  │  pytest  │   │ Semgrep  │   │   OWASP  │   │   Docker   │  │
│  └──────────┘   └──────────┘   └──────────┘   └────────────┘  │
│                                                       │         │
│                                               ┌───────▼──────┐ │
│                                               │   Stage 5    │ │
│                                               │ 🛡️ Container │ │
│                                               │    Trivy     │ │
│                                               └───────┬──────┘ │
│                                                       │         │
│                                               ┌───────▼──────┐ │
│                                               │   Stage 6    │ │
│                                               │ 🚀 Deploy    │ │
│                                               │   Staging    │ │
│                                               └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Application** | Python 3.12, Flask 3.0, Gunicorn |
| **Containerization** | Docker (multi-stage build) |
| **CI/CD** | GitHub Actions |
| **SAST** | Semgrep (Python, Flask, OWASP Top 10 rules) |
| **SCA** | OWASP Dependency-Check, pip-audit |
| **Container Scanning** | Trivy (Aqua Security) |
| **Testing** | pytest, pytest-cov |

---

## 📁 Project Structure

```
devsecops-pipeline/
├── .github/
│   └── workflows/
│       └── devsecops-pipeline.yml   ← Main CI/CD pipeline
├── app/
│   └── main.py                      ← Flask REST API application
├── tests/
│   └── test_app.py                  ← pytest unit tests
├── Dockerfile                       ← Multi-stage Docker build
├── requirements.txt                 ← Python dependencies
├── .semgrep.yml                     ← Custom SAST rules
├── .gitignore
└── README.md
```

---

## 🔄 Pipeline Stages Explained

### Stage 1 — 🧪 Unit Tests (`pytest`)
- Runs all unit tests with code coverage reporting
- Generates `coverage.xml` uploaded as an artifact
- **Gate:** Pipeline stops if tests fail

### Stage 2 — 🔍 SAST: Static Application Security Testing (`Semgrep`)
- Scans source code for security vulnerabilities **without running it**
- Rules applied: Python security, Flask-specific, OWASP Top 10, Secrets detection
- Results uploaded to **GitHub Security tab** in SARIF format
- **Detects:** SQL injection, XSS, hardcoded secrets, insecure configs

### Stage 3 — 📦 SCA: Software Composition Analysis (`OWASP Dependency-Check` + `pip-audit`)
- Scans `requirements.txt` dependencies against the **National Vulnerability Database (NVD)**
- Identifies known CVEs in third-party libraries
- **Gate:** Fails pipeline if any dependency has CVSS score ≥ 9.0 (Critical)

### Stage 4 — 🐳 Build Docker Image
- Builds a **multi-stage Docker image** (builder + minimal runtime)
- Non-root user for container security
- Health check built into the image

### Stage 5 — 🛡️ Container Scanning (`Trivy`)
- Scans the built Docker image for OS-level and library vulnerabilities
- Results uploaded to **GitHub Security tab**
- **Gate:** Hard fail on any **CRITICAL** unfixed CVE

### Stage 6 — 🚀 Deploy to Staging
- Deploys the container to a staging environment
- Runs automated **smoke tests** against live endpoints
- Only runs after ALL security gates pass

### Stage 7 — 📊 Security Summary
- Generates a consolidated summary in the GitHub Actions run

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Docker
- GitHub account (for pipeline execution)

### Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/devsecops-pipeline.git
cd devsecops-pipeline

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app/main.py

# Run tests
pytest tests/ -v --cov=app
```

### Run with Docker

```bash
# Build the image
docker build -t devsecops-demo-app .

# Run the container
docker run -p 5000:5000 devsecops-demo-app

# Test it
curl http://localhost:5000/health
curl http://localhost:5000/users
```

---

## 🔑 GitHub Secrets Required

Set these in your repo → **Settings → Secrets and variables → Actions**:

| Secret | Description |
|--------|-------------|
| `SEMGREP_APP_TOKEN` | Get from [semgrep.dev](https://semgrep.dev) (free account) |

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API info |
| `GET` | `/health` | Health check |
| `GET` | `/users` | List all users |
| `GET` | `/users/<id>` | Get user by ID |
| `POST` | `/users` | Create new user |

---

## 🔐 Security Features Implemented

- **Non-root Docker user** — container runs as `appuser`, not root
- **Multi-stage Docker build** — minimal attack surface in runtime image
- **Health check** — Docker monitors app liveness
- **No debug mode** — Flask debug disabled in production
- **Dependency pinning** — exact versions in `requirements.txt`
- **Automated CVE scanning** — every build scanned against NVD

---

## 📊 Sample Security Report

```
┌─────────────────────────────────────┐
│       Security Scan Results         │
├───────────┬─────────────┬───────────┤
│ Tool      │ Issues Found│ Severity  │
├───────────┼─────────────┼───────────┤
│ Semgrep   │ 0           │ -         │
│ pip-audit │ 0           │ -         │
│ Trivy     │ 0 Critical  │ PASS ✅   │
└───────────┴─────────────┴───────────┘
```

---

## 📚 Key Concepts

**DevSecOps** = Development + Security + Operations — integrating security practices within the DevOps process.

**Shift-Left Security** = Moving security testing earlier in the pipeline (left on the timeline), making it cheaper and faster to fix vulnerabilities.

**SAST** (Static Application Security Testing) = Analyzing source code for vulnerabilities without executing it.

**SCA** (Software Composition Analysis) = Identifying vulnerabilities in open-source dependencies.

**Container Scanning** = Checking Docker images for known CVEs in OS packages and installed libraries.

---

## 👤 Author

**MCA Final Year Project**  
Department of Computer Applications

---

## 📄 License

MIT License — free to use for educational purposes.
