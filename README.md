# 📌 Student Noticeboard - DSO101 Group Project

**Course:** DSO101 | **Date:** 02/04/2026  
**Team:** Phuntsho Namgyel · Kelden Phuntsho Dorji · Jigme Ngawang Chogyal · Yeshey Lhaden

A **full-stack, containerized web application** where students can post, browse, filter, and manage announcements. Demonstrates modern DevOps practices with complete CI/CD automation, Docker containerization, and security best practices.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Architecture](#-architecture)
3. [Technology Stack](#-technology-stack)
4. [Project Structure](#-project-structure)
5. [Quick Start - Local Development](#-quick-start---local-development)
6. [Docker & Docker Compose](#-docker--docker-compose)
7. [CI/CD Pipeline](#-cicd-pipeline)
8. [API Documentation](#-api-documentation)
9. [Testing](#-testing)
10. [Team Roles & Responsibilities](#-team-roles--responsibilities)
11. [Security & Best Practices](#-security--best-practices)
12. [Troubleshooting](#-troubleshooting)

---

## 🎯 Project Overview

### What Is It?
A **digital student notice board** – a full-stack web application that replaces traditional physical bulletin boards with an online platform where:
- Students can **post announcements** (with category, title, body, author)
- Browse all **notices in real-time**
- **Filter by category** (general, academic, event, urgent, club)
- **Search** announcements by keyword
- **Delete** their own notices
- All data **persists in PostgreSQL**

### Primary Aims
1. ✅ Build a **full-stack web application** with real database persistence
2. ✅ **Containerize** all services (frontend, backend, database) using Docker
3. ✅ Implement a **multi-stage CI/CD pipeline** (GitHub Actions)
4. ✅ Automate **build, test, security scanning, and deployment**
5. ✅ Follow **industry-standard security** practices (no hardcoded secrets, non-root users, environment variables)

### Success Criteria (Completed)
- ✅ Working 3-container app with full CRUD via browser
- ✅ Fully automated pipeline triggered on every push to `main`
- ✅ Versioned Docker images pushed to Docker Hub
- ✅ Unit tests with PostgreSQL test database
- ✅ Non-root containers with no hardcoded credentials
- ✅ Comprehensive documentation & README

---

## 🏗️ Architecture

### Three-Service Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     BROWSER / CLIENT                    │
│                (Renders HTML/CSS/JS UI)                 │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP Requests
                         ▼
        ┌────────────────────────────────┐
        │   FRONTEND CONTAINER (Nginx)   │
        │  - Serves HTML/CSS/JavaScript  │
        │  - Calls Backend REST API      │
        │  - Port: 8080 (public)         │
        └────────────────┬───────────────┘
                         │ REST API Calls (localhost:5001)
                         ▼
        ┌────────────────────────────────┐
        │   BACKEND CONTAINER (Flask)    │
        │  - Python Flask REST API       │
        │  - CORS enabled                │
        │  - Talks to Database           │
        │  - Port: 5000 (internal)       │
        │  - Port: 5001 (docker-compose) │
        └────────────────┬───────────────┘
                         │ SQL Queries
                         ▼
        ┌────────────────────────────────┐
        │  DATABASE CONTAINER (PostgreSQL)│
        │  - PostgreSQL 14               │
        │  - Database: noticeboard       │
        │  - Persistent Volume           │
        │  - Port: 5432                  │
        └────────────────────────────────┘
```

### Docker Compose Network
- **Service-to-service communication** via service names (e.g., `db`, `backend`, `frontend`)
- **Shared Docker network** (`docker-compose.yml` creates one automatically)
- **Health checks** ensure services are ready before dependencies start
- **Persistent volume** (`postgres_data`) stores database files even after container restart

### CI/CD Pipeline Flow

```
┌─────────────────────────────────────────────────────────┐
│  Code Push to GitHub (main branch)                      │
└────────────────────────┬────────────────────────────────┘
                         ▼
    ┌─────────────────────────────────────┐
    │ STAGE 1: Code Quality & Linting     │
    │  - Flake8 (Python linter)           │
    │  - Black (code formatter)           │
    └────────────────┬────────────────────┘
                     ▼
    ┌─────────────────────────────────────┐
    │ STAGE 2: Unit Tests                 │
    │  - Pytest framework                 │
    │  - PostgreSQL test database         │
    │  - Code coverage reports            │
    └────────────────┬────────────────────┘
                     ▼
    ┌─────────────────────────────────────┐
    │ STAGE 3: Build Docker Images        │
    │  - Backend (Python Flask)           │
    │  - Frontend (Nginx)                 │
    │  - Push to Docker Hub               │
    └────────────────┬────────────────────┘
                     ▼
    ┌─────────────────────────────────────┐
    │ STAGE 4: Security Scanning          │
    │  - Trivy vulnerability scanner      │
    │  - Upload results to GitHub         │
    └────────────────┬────────────────────┘
                     ▼
    ┌─────────────────────────────────────┐
    │ STAGE 5: Integration Tests          │
    │  - Docker Compose stack up          │
    │  - Test API endpoints               │
    │  - Health checks                    │
    └────────────────┬────────────────────┘
                     ▼
    ✅ Pipeline Complete - Ready for Deployment
```

---

## 🛠️ Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | HTML5 / CSS3 / JavaScript (Vanilla) | ES6+ | Responsive UI, API calls |
| **Backend** | Python Flask | 3.9 | REST API, business logic |
| **Database** | PostgreSQL | 14 | Persistent data storage |
| **Container** | Docker | Latest | Containerization |
| **Orchestration** | Docker Compose | 3.8 | Multi-container networking |
| **CI/CD** | GitHub Actions | Latest | Automated pipeline |
| **Registry** | Docker Hub | - | Image versioning & storage |
| **Security Scanning** | Trivy | Latest | Vulnerability detection |
| **Testing Framework** | Pytest | Latest | Unit testing |
| **Code Analysis** | Flake8, Black | Latest | Linting & formatting |

---

## 📁 Project Structure

```
DSO101_StudentNoticeBoard_GroupProject/
│
├── .github/
│   └── workflows/
│       └── ci-cd-pipeline.yml          ← GitHub Actions workflow (5 stages)
│
├── backend/
│   ├── app.py                          ← Flask REST API (CRUD endpoints)
│   ├── requirements.txt                 ← Python dependencies
│   ├── Dockerfile                       ← Backend container definition
│   ├── .env.example                     ← Template for environment variables
│   ├── .gitignore                       ← Prevent committing secrets
│   ├── README.md                        ← Backend API documentation
│   └── tests/
│       ├── __init__.py
│       └── test_app.py                  ← 14+ unit tests
│
├── frontend/
│   ├── noticeboard.html                 ← Main UI (single-page app)
│   ├── noticeboard.css                  ← Styling (responsive design)
│   ├── mega.webp                        ← CST logo
│   └── Dockerfile                       ← Generated by CI/CD pipeline
│
├── docker-compose.yml                   ← Orchestrate 3 services locally
│
├── README.md                            ← This file (project overview)
│
└── GITHUB_SECRETS_SETUP_FINAL-1.md      ← Instructions for CI/CD setup
```

---

## 🚀 Quick Start - Local Development

### Prerequisites
- **Python 3.9+** – [Download](https://www.python.org/downloads/)
- **PostgreSQL 14+** – [Download](https://www.postgresql.org/download/)
- **pip** – Usually comes with Python
- **Git** – For cloning the repo

### Step 1: Clone Repository

```bash
git clone https://github.com/Yesheylhaden/DSO101_StudentNoticeBoard_GroupProject.git
cd DSO101_StudentNoticeBoard_GroupProject
```

### Step 2: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create database (run once)
createdb noticeboard

# Copy environment template
cp .env.example .env

# Run Flask server
python3 app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * WARNING in app.py:...: This is a development server.
```

### Step 3: Open Frontend

```bash
# In a new terminal, navigate to project root
# Open in browser:
open frontend/noticeboard.html

# Or use a simple HTTP server:
cd frontend
python3 -m http.server 8000
# Then visit: http://localhost:8000
```

### Step 4: Test the API

```bash
# Health check
curl http://localhost:5001/health

# Get all notices
curl http://localhost:5001/announcements

# Create a notice
curl -X POST http://localhost:5001/announcements \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Welcome to Noticeboard",
    "body": "This is a test notice",
    "category": "general",
    "author": "Test User"
  }'
```

---

## 🐳 Docker & Docker Compose

### Why Docker?
- **Consistency**: Works the same on any machine (laptop, CI/CD, production)
- **Isolation**: Each service runs in its own container
- **Scalability**: Easy to replicate and manage services
- **Security**: Containers can run as non-root users

### Building Images Locally

```bash
# Build backend image
cd backend
docker build -t student-noticeboard-backend:latest .

# Build frontend image (simple Nginx)
cd ../frontend
docker build -t student-noticeboard-frontend:latest .
```

### Running with Docker Compose

```bash
# Start all 3 services (frontend, backend, database)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (database data)
docker-compose down -v
```

### Service Details

| Service | Image | Port | Network |
|---------|-------|------|---------|
| **db** | postgres:14 | 5432 | Internal only |
| **backend** | student-noticeboard-backend | 5000 → 5001 | 127.0.0.1:5001 |
| **frontend** | nginx:alpine | 80 → 8080 | 127.0.0.1:8080 |

### Environment Variables (docker-compose.yml)

```yaml
environment:
  DB_HOST: db              # Service name (not localhost!)
  DB_PORT: 5432            # PostgreSQL default port
  DB_NAME: noticeboard     # Database name
  DB_USER: postgres        # PostgreSQL user
  DB_PASSWORD: postgres    # PostgreSQL password
  FLASK_ENV: production    # Production mode
  FLASK_DEBUG: False       # Disable debug mode
```

---

## 🤖 CI/CD Pipeline

### What Does It Do?

Every time code is pushed to the **main** branch, the GitHub Actions pipeline automatically:

1. **Checks Code Quality** (Flake8, Black)
2. **Runs Unit Tests** (Pytest with PostgreSQL test database)
3. **Builds Docker Images** (backend + frontend)
4. **Scans for Vulnerabilities** (Trivy security scanner)
5. **Tests Integration** (Docker Compose stack with API tests)

### Setup GitHub Secrets

Store credentials securely:

```bash
# 1. Go to GitHub Repo → Settings → Secrets and variables → Actions
# 2. Click "New repository secret" for each:

Secret 1: DOCKER_USERNAME
Value: sevenkels

Secret 2: DOCKER_PASSWORD
Value: [Your Docker Personal Access Token]
```

**⚠️ Never commit credentials to Git!**

### Workflow File Location

```
.github/workflows/ci-cd-pipeline.yml
```

### Pipeline Stages

#### **STAGE 1: Code Quality & Linting** (2 min)
- Installs Python 3.11
- Runs Flake8 (error detection)
- Checks Black formatting

#### **STAGE 2: Unit Tests** (3 min)
- Starts PostgreSQL 14 test database
- Installs dependencies
- Runs 14+ Pytest tests
- Uploads coverage reports to Codecov

#### **STAGE 3: Build Docker Images** (5 min)
- Authenticates to Docker Hub
- Builds backend image
- Builds frontend image (Nginx)
- Tags with git branch, semantic version, commit SHA, latest
- Pushes to Docker Hub

#### **STAGE 4: Security Scanning** (3 min)
- Scans backend image with Trivy
- Scans frontend image with Trivy
- Uploads results to GitHub Security tab

#### **STAGE 5: Integration Tests** (4 min)
- Starts Docker Compose stack
- Tests `/health` endpoint
- Tests `GET /announcements`
- Tests `POST /announcements`
- Tears down stack

### Triggering Manually

```bash
# Just push to main
git add .
git commit -m "Your message"
git push origin main

# Check status: GitHub Repo → Actions tab
```

---

## 📡 API Documentation

### Base URL
- **Local**: `http://localhost:5001`
- **Docker**: `http://localhost:5001` (via docker-compose)
- **Production**: (Deployed via CI/CD)

### Endpoints

#### **1. Health Check**

```http
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

---

#### **2. Get All Notices**

```http
GET /announcements
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Welcome",
    "body": "This is a notice",
    "category": "general",
    "author": "Admin",
    "date": "02 Apr 2026"
  }
]
```

---

#### **3. Create Notice**

```http
POST /announcements
Content-Type: application/json

{
  "title": "New Notice",
  "body": "Description of the notice",
  "category": "academic",
  "author": "Your Name"
}
```

**Valid Categories:**
- `general` (default)
- `academic`
- `event`
- `urgent`
- `club`

**Response:** (HTTP 201)
```json
{
  "id": 2,
  "title": "New Notice",
  "body": "Description of the notice",
  "category": "academic",
  "author": "Your Name",
  "date": "02 Apr 2026"
}
```

**Error Response:** (HTTP 400)
```json
{
  "error": "title, body, and author are required"
}
```

---

#### **4. Delete Notice**

```http
DELETE /announcements/{id}
```

**Response:** (HTTP 200)
```json
{
  "message": "Notice deleted successfully"
}
```

---

### CORS Configuration

The API allows requests from any origin:
```python
CORS(app)  # In app.py
```

This enables the frontend to call the backend API from any domain.

---

## ✅ Testing

### Unit Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Test Coverage

File: `backend/tests/test_app.py`

**Test Classes:**

1. **TestHealth** – Tests `/health` endpoint
2. **TestNotices** – Tests all CRUD operations
   - Empty list test
   - Create notice (valid)
   - Create notice (missing fields)
   - Create notice (invalid category)
   - Get notices after creation
   - And more...

**Sample Test:**

```python
def test_create_announcement(self, client):
    """Test POST /announcements creates a new notice."""
    notice_data = {
        'title': 'Test Notice',
        'body': 'This is a test notice',
        'category': 'general',
        'author': 'Test Author'
    }
    response = client.post(
        '/announcements',
        json=notice_data,
        content_type='application/json'
    )
    assert response.status_code == 201
    assert response.json['title'] == 'Test Notice'
```

---

## 👥 Team Roles & Responsibilities

| Team Member | Role | Responsibilities |
|---|---|---|
| **Yeshey Lhaden** | Frontend Lead | • HTML/CSS/JavaScript UI<br/>• Responsive design<br/>• User interaction logic<br/>• API integration |
| **Kelden Phuntsho Dorji** | Backend & Docker Lead | • Flask REST API<br/>• PostgreSQL database design<br/>• Environment variables<br/>• Dockerfiles<br/>• Docker Compose setup |
| **Jigme Ngawang Chogyal** | Jenkins & CI Lead | • Jenkinsfile pipeline<br/>• Build automation<br/>• Test orchestration<br/>• Deployment scripting |
| **Phuntsho Namgyel** | GitHub Actions & DevOps Lead | • GitHub Actions workflow<br/>• Secrets management<br/>• Docker Hub integration<br/>• Security scanning setup |
| **All** | Security & Documentation | • Environment variable handling<br/>• Non-root container users<br/>• README & API docs<br/>• Presentation prep |

---

## 🔐 Security & Best Practices

### 1. Secrets Management

❌ **Never commit credentials:**
```bash
# BAD - Never do this!
DB_PASSWORD=postgres123
DOCKER_TOKEN=abc123xyz
```

✅ **Use environment variables:**
```bash
# Good - .env (not committed)
DB_PASSWORD=${DB_PASSWORD}

# Good - GitHub Secrets
Settings → Secrets and variables → Actions
```

✅ **Use .gitignore:**
```
.env
.env.local
*.pem
```

### 2. Non-Root Containers

```dockerfile
# In Dockerfile (best practice)
RUN useradd -m -u 1000 appuser
USER appuser
```

This prevents container escape attacks.

### 3. SQL Injection Protection

```python
# Good - SQLAlchemy ORM (parameterized queries)
notice = Notice.query.filter_by(id=id).first()

# Bad - String concatenation
query = f"SELECT * FROM notices WHERE id = {id}"  # ❌ VULNERABLE
```

### 4. Input Validation

```python
# Validate required fields
if not data or not data.get("title"):
    return jsonify({"error": "title is required"}), 400

# Validate enum values
valid_categories = ["general", "academic", "event", "urgent", "club"]
if category not in valid_categories:
    return jsonify({"error": f"Invalid category"}), 400
```

### 5. CORS Configuration

```python
# Allow frontend to call API
CORS(app)
```

### 6. Docker Security

✅ **Alpine base images** (smaller attack surface)
```dockerfile
FROM python:3.11-slim
```

✅ **Read-only file systems**
```yaml
# docker-compose.yml
volumes:
  - ./frontend:/usr/share/nginx/html:ro  # :ro = read-only
```

✅ **Health checks**
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 10s
  timeout: 5s
  retries: 5
```

---

## 🐛 Troubleshooting

### Frontend Can't Connect to Backend

**Problem:** `Failed to fetch http://localhost:5001/announcements`

**Solutions:**

1. Check backend is running:
```bash
curl http://localhost:5001/health
```

2. Check CORS is enabled in `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

3. Check backend port in frontend code:
```javascript
const API_URL = 'http://localhost:5001';  // Make sure port is 5001
```

---

### Docker Compose Services Won't Connect

**Problem:** `backend_1 | psycopg2.OperationalError: could not connect to server`

**Solutions:**

1. Use **service name**, not `localhost`:
```yaml
environment:
  DB_HOST: db     # ✅ Correct (service name)
  # NOT: localhost ❌
```

2. Check health checks:
```bash
docker-compose logs db
```

3. Rebuild images:
```bash
docker-compose down
docker-compose up --build
```

---

### Port Already in Use

**Problem:** `Error starting userland proxy: bind: address already in use`

**Solution:**

```bash
# Find process using port 5001
lsof -i :5001

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "5002:5000"  # Use 5002 instead
```

---

### Pipeline Fails on Docker Build

**Problem:** GitHub Actions build fails with auth error

**Solution:**

1. Check GitHub Secrets exist:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`

2. Generate new Docker token:
   - Docker Hub → Account Settings → Security → Personal Access Tokens

3. Update GitHub Secret:
   - GitHub Repo → Settings → Secrets → DOCKER_PASSWORD

---

### Pytest Fails: "PostgreSQL Connection Refused"

**Problem:** `psycopg2.OperationalError: could not connect to server`

**Solution:**

1. Make sure PostgreSQL is running:
```bash
# macOS
brew services start postgresql@14

# Linux
sudo systemctl start postgresql

# Or use Docker
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:14
```

2. Create test database:
```bash
createdb noticeboard_test
```

3. Run pytest:
```bash
pytest tests/ -v
```

---

## 📚 Additional Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

### Tools
- [Postman](https://www.postman.com/) – API testing
- [DBeaver](https://dbeaver.io/) – Database GUI
- [Docker Desktop](https://www.docker.com/products/docker-desktop) – Local Docker environment

### Monitoring
- [Docker Hub Dashboard](https://hub.docker.com/repositories) – View pushed images
- [GitHub Actions Tab](https://github.com/Yesheylhaden/DSO101_StudentNoticeBoard_GroupProject/actions) – Pipeline runs
- [GitHub Security Tab](https://github.com/Yesheylhaden/DSO101_StudentNoticeBoard_GroupProject/security) – Vulnerability reports

---

## 📝 Contributing

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes
# (Edit files, test locally)

# 3. Push to GitHub
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# 4. Create Pull Request on GitHub
# (CI/CD pipeline runs automatically)

# 5. Merge to main after approval
# (Triggers full deployment pipeline)
```

### Local Testing Before Push

```bash
# Run linting
flake8 backend/app.py

# Run tests
pytest backend/tests/ -v

# Test with Docker Compose
docker-compose up -d
curl http://localhost:5001/health
docker-compose down
```

---

## 📞 Support & Contact

For issues or questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Open a GitHub Issue in the repository
3. Contact the team via email

---

## 📄 License

This project is part of **DSO101 (College of Science and Technology)** coursework.

---

## 🎉 Acknowledgments

Built with ❤️ by the **DSO101 Group Project Team** as a demonstration of modern DevOps practices, containerization, and full-stack development.

**Special Thanks To:**
- Python & Flask community
- PostgreSQL community
- Docker & GitHub Actions teams
- All contributors and reviewers

---

**Last Updated:** May 24, 2026  
**Status:** ✅ Production Ready
