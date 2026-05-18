# 📌 Student Noticeboard - DSO101 Group Project

A full-stack web application for posting, browsing, and managing student announcements. Built with Flask (backend), PostgreSQL (database), and vanilla HTML/CSS/JS (frontend).

**Team:** Phuntsho Namgyel · Kelden Phuntsho · Jigme Ngawang · Yeshey Lhaden  
**Date:** 19 May 2026

---

## 🏗️ Project Structure

```
DSO101_StudentNoticeBoard_GroupProject/
├── frontend/
│   ├── noticeboard.html      ← Main UI (calls backend API)
│   ├── noticeboard.css       ← Styling
│   └── mega.webp             ← Logo
├── backend/
│   ├── app.py                ← Flask REST API
│   ├── requirements.txt       ← Python dependencies
│   ├── .env                  ← Database credentials (local)
│   ├── .env.example          ← Template for team
│   ├── .gitignore            ← Prevent committing secrets
│   └── README.md             ← Backend API docs
├── README.md                 ← This file
└── docker-compose.yml        ← (To be created by Docker team)
```

---

## ✅ What's DONE (Backend - Kelden)

### Backend API (Flask)
- ✅ **GET /announcements** - Retrieve all notices
- ✅ **POST /announcements** - Create new notice
- ✅ **PUT /announcements/{id}** - Update notice
- ✅ **DELETE /announcements/{id}** - Delete notice
- ✅ **GET /health** - Health check endpoint

### Database (PostgreSQL)
- ✅ Database: `noticeboard` (created)
- ✅ Table: `notices` (auto-created by Flask)
- ✅ Data persistence verified
- ✅ Running on `localhost:5432`

### Frontend Integration
- ✅ Updated to call backend API
- ✅ No more localStorage - uses real database
- ✅ Full CRUD UI working
- ✅ Category filtering, search, delete working

### Security & Configuration
- ✅ Environment variables for credentials
- ✅ SQL injection protection (SQLAlchemy)
- ✅ Input validation on all endpoints
- ✅ CORS configured
- ✅ .gitignore prevents sensitive file commits

### Testing
- ✅ All endpoints tested and working
- ✅ Data verified in PostgreSQL
- ✅ API running on port 5001

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9+
- PostgreSQL 14+
- pip

### Setup Backend

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Create database (if not exists)
createdb noticeboard

# Run Flask server
python3 app.py
```

Server will run at: `http://localhost:5001`

### Test API

```bash
# Health check
curl http://localhost:5001/health

# Get all notices
curl http://localhost:5001/announcements

# Create a notice
curl -X POST http://localhost:5001/announcements \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Notice",
    "body": "Test body",
    "category": "general",
    "author": "Your Name"
  }'
```

### Open Frontend

1. Open `frontend/noticeboard.html` in a web browser
2. API should auto-connect to `http://localhost:5001`
3. Click "+ Post Notice" to create
4. Notices appear from database

---

## 📋 TODO for Docker Team (Phuntsho, Jigme, Yeshey)

### ⭐ KEY POINT: Zero Database Setup Required!

When you run `docker-compose up --build`:
- ✅ PostgreSQL container starts automatically
- ✅ Database `noticeboard` is created automatically
- ✅ Table `notices` is created automatically
- ✅ All credentials are pre-configured in docker-compose.yml
- ✅ **You do nothing!** Just run the command.

**No need to:**
- ❌ Install PostgreSQL locally
- ❌ Create databases manually
- ❌ Set credentials
- ❌ Run any SQL commands

Everything is automated!

### Tasks:
1. **Create Dockerfile** in `backend/` folder
2. **Create docker-compose.yml** in project root
3. **Build and test containers**

### Step 1: Create `backend/Dockerfile`

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY .env.example .env

EXPOSE 5000

CMD ["python", "app.py"]
```

**How to create it:**
```bash
cd backend
nano Dockerfile  # or use your editor
# Paste the Dockerfile content above
# Save and exit
```

### Step 2: Create `docker-compose.yml` (in project root)

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: noticeboard
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    ports:
      - "5001:5000"
    environment:
      DB_HOST: db          # ⭐ IMPORTANT: Use 'db' (service name), NOT localhost
      DB_PORT: 5432
      DB_NAME: noticeboard
      DB_USER: postgres
      DB_PASSWORD: postgres
      FLASK_ENV: production
      FLASK_DEBUG: False
    depends_on:
      db:
        condition: service_healthy
    command: python app.py

  frontend:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./frontend:/usr/share/nginx/html:ro
    depends_on:
      - backend

volumes:
  postgres_data:
```

**How to create it:**
```bash
cd ..  # Go to project root (DSO101_StudentNoticeBoard_GroupProject)
nano docker-compose.yml
# Paste the docker-compose content above
# Save and exit
```

### Step 3: Build and Run

```bash
# From project root directory
docker-compose up --build
```

**What this does automatically:**
1. ✅ Builds the Flask backend image from `backend/Dockerfile`
2. ✅ Creates PostgreSQL container (no setup needed!)
3. ✅ Creates Nginx frontend container
4. ✅ All containers are linked together
5. ✅ **Database auto-creates** with tables when Flask starts
6. ✅ Data persists in `postgres_data` volume

**No manual database setup needed!** Everything is automatic.

**Access the app:**
- Frontend: `http://localhost:8080`
- API: `http://localhost:5001`
- PostgreSQL: `localhost:5432`

### Step 4: Test the Full Stack

**In a new terminal (while docker-compose is running):**

```bash
# Test health check
curl http://localhost:5001/health

# Create a notice
curl -X POST http://localhost:5001/announcements \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Docker Test",
    "body": "Testing in container",
    "category": "general",
    "author": "Team"
  }'

# Get all notices
curl http://localhost:5001/announcements

# Open frontend in browser
open http://localhost:8080
# or
firefox http://localhost:8080
```

### Step 5: Verify Everything Works

**Checklist:**
- [ ] Containers started without errors
- [ ] Frontend loads at http://localhost:8080
- [ ] Can create notices from frontend
- [ ] Notices appear in database
- [ ] Data persists after refresh
- [ ] Can delete notices
- [ ] API responds to curl requests

### Troubleshooting

**Containers won't start?**
```bash
# Check Docker is running
docker --version

# Check for port conflicts
lsof -i :5001
lsof -i :8080
lsof -i :5432

# View logs
docker-compose logs backend
docker-compose logs db
```

**Database connection error?**
```bash
# Wait for database to be ready
docker-compose logs db

# Rebuild without cache
docker-compose up --build --no-cache
```

**Can't access frontend?**
```bash
# Check if nginx container is running
docker ps

# Check nginx logs
docker-compose logs frontend

# Verify frontend files exist
ls -la frontend/
```

**Need to restart?**
```bash
# Stop all containers
docker-compose down

# Remove volumes (clears data)
docker-compose down -v

# Start fresh
docker-compose up --build
```

### Important Notes for Your Team

1. **DB_HOST must be 'db'** - This is the service name in docker-compose, NOT localhost
2. **Don't commit .env** - It's in .gitignore, use .env.example template
3. **Volume persistence** - Database data persists even after stopping containers
4. **Port mapping** - `5001:5000` means: external:internal (backend internally runs on 5000)
5. **Nginx serves frontend** - Static HTML/CSS/JS served by Nginx on port 8080

---

## 📊 API Endpoints Reference

### GET /announcements
**Get all notices**
```bash
curl http://localhost:5001/announcements
```
**Response:**
```json
[
  {
    "id": 1,
    "title": "Test Notice",
    "body": "This is a test",
    "category": "general",
    "author": "Kelden",
    "date": "18 May 2026"
  }
]
```

### POST /announcements
**Create a new notice**
```bash
curl -X POST http://localhost:5001/announcements \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Notice",
    "body": "Notice body (max 400 chars)",
    "category": "academic",
    "author": "Your Name"
  }'
```
**Valid Categories:** `general`, `academic`, `event`, `urgent`, `club`

### PUT /announcements/{id}
**Update a notice**
```bash
curl -X PUT http://localhost:5001/announcements/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "body": "Updated body"
  }'
```

### DELETE /announcements/{id}
**Delete a notice**
```bash
curl -X DELETE http://localhost:5001/announcements/1
```

---

## 🗄️ Database Schema

### notices table
```sql
CREATE TABLE notices (
  id SERIAL PRIMARY KEY,
  title VARCHAR(80) NOT NULL,
  body VARCHAR(400) NOT NULL,
  category VARCHAR(20) NOT NULL DEFAULT 'general',
  author VARCHAR(40) NOT NULL,
  date VARCHAR(20) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Security Features

- ✅ **SQL Injection Protection** - SQLAlchemy parameterized queries
- ✅ **Input Validation** - Required fields, category whitelist
- ✅ **Environment Variables** - Credentials NOT hardcoded
- ✅ **CORS Configured** - Allows all origins for development
- ⚠️ **No Authentication** - Add authentication layer if needed for production

---

## 📝 Environment Variables

### Local Development (.env)
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=noticeboard
DB_USER=keldendrac
DB_PASSWORD=
FLASK_ENV=development
FLASK_DEBUG=True
```

### Docker Deployment (docker-compose)
```
DB_HOST=db                  # Service name in docker-compose
DB_PORT=5432
DB_NAME=noticeboard
DB_USER=postgres
DB_PASSWORD=postgres
FLASK_ENV=production
FLASK_DEBUG=False
```

---

## 🧪 Testing Checklist

- [x] Backend runs without errors
- [x] PostgreSQL connects successfully
- [x] GET /health returns 200
- [x] POST creates notices in DB
- [x] GET retrieves from database
- [x] PUT updates notices
- [x] DELETE removes notices
- [x] Frontend connects to backend
- [x] CORS fixed (all origins allowed for dev)
- [x] Full-stack integration tested
- [ ] Docker build works (Docker team)
- [ ] docker-compose runs all services (Docker team)

---

## 📚 Additional Resources

- **Backend API Docs:** See `backend/README.md`
- **Flask SQLAlchemy:** https://flask-sqlalchemy.palletsprojects.com/
- **PostgreSQL Docs:** https://www.postgresql.org/docs/
- **Docker Docs:** https://docs.docker.com/

---

## 👥 Team Roles

| Name | Task | Status |
|------|------|--------|
| Kelden | Backend API + PostgreSQL | ✅ DONE |
| Phuntsho | Dockerfile + docker-compose | ⏳ TODO |
| Jigme | Dockerfile + docker-compose | ⏳ TODO |
| Yeshey | Dockerfile + docker-compose | ⏳ TODO |

---

## 🚀 Deployment Checklist

- [x] Backend API complete
- [x] Database working
- [x] Frontend connected
- [x] Local testing passed
- [ ] Dockerfile created
- [ ] docker-compose.yml created
- [ ] Containers built successfully
- [ ] All services running
- [ ] API accessible from containers
- [ ] Data persists in PostgreSQL container

---

## ⚡ Quick Commands

```bash
# Backend
cd backend && python3 app.py

# Test API
curl http://localhost:5001/health

# Check database
psql -d noticeboard -c "SELECT * FROM notices;"

# Docker (when ready)
docker-compose up --build
docker-compose down
```

---

## 📞 Troubleshooting

**Port 5001 already in use?**
```bash
lsof -ti:5001 | xargs kill -9
```

**Database connection error?**
```bash
# Make sure PostgreSQL is running
brew services start postgresql@14
# Create database
createdb noticeboard
```

**API not responding?**
- Check `.env` file has correct credentials
- Verify PostgreSQL is running: `psql -l`
- Check backend logs: `python3 app.py`

---

## 📄 License

School Project - CST (College of Science and Technology), Phuntsholing

---

**Last Updated:** 19 May 2026  
**Status:** ✅ Backend Complete & Tested | ⏳ Docker Team - Ready for Containerization

---

## 📞 Quick Contact

**Kelden (Backend):** Backend is DONE and tested with frontend ✅  
**Team (Docker):** Follow the TODO section above - all code provided!

**Backend is production-ready. Docker team can start immediately with the code templates provided.**
