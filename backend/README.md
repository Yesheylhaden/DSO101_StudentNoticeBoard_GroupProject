# Student Noticeboard Backend API

Flask REST API for the Student Noticeboard application. Supports full CRUD operations for announcements with PostgreSQL database.

## Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 14+
- pip

### Local Development

1. **Clone and navigate to backend:**
   ```bash
   cd DSO101_StudentNoticeBoard_GroupProject/backend
   ```

2. **Create PostgreSQL database:**
   ```bash
   createdb noticeboard
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your PostgreSQL credentials
   ```

5. **Run the server:**
   ```bash
   python3 app.py
   ```
   - API will be available at `http://localhost:5001`
   - Health check: `curl http://localhost:5001/health`

## API Endpoints

### GET /announcements
Retrieve all notices (sorted by newest first)

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
Create a new notice

**Request Body:**
```json
{
  "title": "Test Notice",
  "body": "This is a test",
  "category": "general",
  "author": "Kelden"
}
```

**Categories:** `general`, `academic`, `event`, `urgent`, `club`

### PUT /announcements/{id}
Update an existing notice

**Request Body:** (partial updates supported)
```json
{
  "title": "Updated Title",
  "body": "Updated body",
  "category": "academic",
  "author": "New Author"
}
```

### DELETE /announcements/{id}
Delete a notice by ID

---

## Docker Deployment

### ⭐ For Docker Team Instructions

**See the main README.md in the project root** for complete step-by-step Docker instructions including:
- How to create `Dockerfile`
- How to create `docker-compose.yml`
- How to build and test containers
- Troubleshooting guide
- Testing commands

👉 **Go to:** `/DSO101_StudentNoticeBoard_GroupProject/README.md` → "TODO for Docker Team" section

### Quick Reference

Key point: When using docker-compose, set `DB_HOST: db` (not localhost)

```yaml
services:
  backend:
    environment:
      DB_HOST: db  # ← This is the service name in docker-compose
```

---

## Database Schema

### notices table

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT |
| title | String(80) | NOT NULL |
| body | String(400) | NOT NULL |
| category | String(20) | NOT NULL, DEFAULT: 'general' |
| author | String(40) | NOT NULL |
| date | String(20) | NOT NULL |
| created_at | DateTime | AUTO TIMESTAMP |

---

## Environment Variables

```
DB_HOST=localhost          # PostgreSQL host
DB_PORT=5432              # PostgreSQL port
DB_NAME=noticeboard       # Database name
DB_USER=postgres          # Database user
DB_PASSWORD=postgres      # Database password
FLASK_ENV=development     # development or production
FLASK_DEBUG=True          # True for development, False for production
```

---

## Testing

**Health Check:**
```bash
curl http://localhost:5001/health
```

**Create Notice:**
```bash
curl -X POST http://localhost:5001/announcements \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test",
    "body": "Test body",
    "category": "general",
    "author": "Test Author"
  }'
```

**Get All:**
```bash
curl http://localhost:5001/announcements
```

**Update:**
```bash
curl -X PUT http://localhost:5001/announcements/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'
```

**Delete:**
```bash
curl -X DELETE http://localhost:5001/announcements/1
```

---

## Security Notes

- ✅ SQLAlchemy prevents SQL injection
- ✅ Input validation for all fields
- ✅ Category whitelist validation
- ⚠️ CORS configured for development (restrict in production)
- ⚠️ No authentication (add for production)
- ⚠️ Debug mode disabled in production

---

## Team Handoff Checklist

✅ **Kelden's Part (DONE):**
- [x] Backend API complete with full CRUD
- [x] PostgreSQL database schema created
- [x] Environment variables configured
- [x] Frontend connected to backend
- [x] All endpoints tested and verified
- [x] CORS configured for development
- [x] Full-stack integration tested

⏳ **Docker Team's Part (TODO):**
- [ ] Read main `README.md` - "TODO for Docker Team" section
- [ ] Create `Dockerfile` in backend folder (code provided)
- [ ] Create `docker-compose.yml` in project root (code provided)
- [ ] Run `docker-compose up --build`
- [ ] Test all endpoints in containers
- [ ] Verify data persistence

**Next Steps for Docker Team:**
1. Open the main `README.md` file (in project root, not this file)
2. Find the "📋 TODO for Docker Team" section
3. Follow Step 1-5 with provided code templates
4. All code is ready to copy-paste!

---

**Created by:** Kelden  
**Date:** 19 May 2026  
**Project:** DSO101 - Student Noticeboard
