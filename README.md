# 📌 Student Noticeboard - DSO101 Group Project

A containerized full-stack application for managing student announcements. Features a Flask REST API backed by PostgreSQL, served via Nginx frontend, with full CI/CD automation using GitHub Actions.

**Team:** Phuntsho Namgyel - Kelden Phuntsho Dorji - Jigme Ngawang Chogyal - Yeshey Lhaden

**Live Backend:** https://student-noticeboard-backend.onrender.com

![App UI](screenshots/app-ui.png)

## Architecture

```
Frontend (Nginx, port 8080)
  ↓ REST API
Backend (Flask, port 5001)
  ↓ SQL
Database (PostgreSQL 14, port 5432)
```

All services run via Docker Compose with health checks and automatic dependency management.

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python Flask, SQLAlchemy |
| Database | PostgreSQL 14 |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Deployment | Render |

## Project Structure

```
├── .github/workflows/
│   └── ci-cd-pipeline.yml
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/test_app.py
├── frontend/
│   ├── noticeboard.html
│   ├── noticeboard.css
│   └── mega.webp
├── docker-compose.yml
└── README.md
```

## Quick Start

### Local Development (with Docker)

```bash
git clone https://github.com/Yesheylhaden/DSO101_StudentNoticeBoard_GroupProject.git
cd DSO101_StudentNoticeBoard_GroupProject

docker-compose up -d
```

| Service | URL |
|---|---|
| Frontend | http://localhost:8080/noticeboard.html |
| Backend | http://localhost:5001 |

### Local Development (without Docker)

```bash
cd backend
pip install -r requirements.txt
createdb noticeboard
python3 app.py
```

Then open frontend:
```bash
cd frontend && python3 -m http.server 8000
# Visit http://localhost:8000/noticeboard.html
```

## API Reference

**Local:** `http://localhost:5001`  
**Live:** `https://student-noticeboard-backend.onrender.com`

![Backend Live](screenshots/backend-live.png)
![API Health](screenshots/api-health.png)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/announcements` | Get all notices |
| POST | `/announcements` | Create notice |
| PUT | `/announcements/{id}` | Update notice |
| DELETE | `/announcements/{id}` | Delete notice |

### Create/Update Notice

```json
{
  "title": "Notice Title",
  "body": "Description",
  "category": "general",
  "author": "Author Name"
}
```

Required fields: `title`, `body`, `author`  
Valid categories: `general`, `academic`, `event`, `urgent`, `club`

## CI/CD Pipeline

GitHub Actions workflow triggers on push to `main`:

1. **Code Quality** – Flake8 linting, Black formatting
2. **Unit Tests** – Pytest against PostgreSQL test database
3. **Build Images** – Docker images built and pushed to Docker Hub
4. **Security Checks** – Hardcoded credential scanning
5. **Integration Tests** – Full Docker Compose stack validation

![Pipeline Success](screenshots/pipeline-success.png)

All images tagged with branch name, commit SHA, and `latest`.

![Docker Hub Images](screenshots/dockerhub-images.png)

### GitHub Secrets Required

- `DOCKER_USERNAME` – Docker Hub username
- `DOCKER_PASSWORD` – Docker Hub personal access token

## Testing

```bash
cd backend

pytest tests/ -v                          # run all tests
pytest tests/ -v --cov=. --cov-report=html  # with coverage
```

## Security

- **Non-root containers** – Dedicated app user prevents privilege escalation
- **No hardcoded secrets** – All credentials via environment variables or GitHub Secrets
- **SQL injection protection** – SQLAlchemy ORM with parameterized queries
- **Input validation** – Required fields and category enforcement
- **Read-only filesystem** – Frontend volume mounted as read-only
- **CORS enabled** – Cross-origin requests allowed for frontend-backend communication

## Deployment

The backend is deployed on Render as a Docker web service, auto-deployed on push to `main`. Free tier instances spin down after inactivity and may take up to 50 seconds to wake.

Frontend runs locally via Docker Compose or direct HTTP server during development.

## Build Locally

```bash
# Build backend image
docker build -t student-noticeboard-backend:latest ./backend

# Build frontend image
docker build -t student-noticeboard-frontend:latest ./frontend
```

## Cleanup

```bash
docker-compose down           # stop services
docker-compose down -v        # stop services and remove volumes
```
