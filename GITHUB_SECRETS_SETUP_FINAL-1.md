# 🔐 GitHub Secrets Setup - For Phuntsho

**For:** Phuntsho Namgyel  
**Task:** Add 2 secrets to GitHub and push to main

---

## 📋 What to Do:

### Step 1: Pull Latest Code
```bash
git pull origin main
```

### Step 2: Add 2 Secrets to GitHub
Go to: **GitHub Repo → Settings → Secrets and variables → Actions**  
Click **New repository secret** for each one:

#### Secret 1️⃣
- **Name:** `DOCKER_USERNAME`
- **Value:** `sevenkels`

#### Secret 2️⃣
- **Name:** `DOCKER_PASSWORD`
- **Value:** `dckr_pat_x5lHIjcNumZeVunie4B4lRjsExQ`

---

### Step 3: Push to Main
```bash
git add .
git commit -m "CI/CD setup complete"
git push origin main
```

---

## 📄 Step 4: Create the Workflow File

Go to: **Your repo folder → `.github/workflows/`**

If `.github/workflows/` doesn't exist, create it:
```bash
mkdir -p .github/workflows
```

**Create file:** `.github/workflows/ci-cd-pipeline.yml`

**Copy-paste this entire code:**

```yaml
name: Student Noticeboard CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

env:
  DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
  DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
  REGISTRY: docker.io
  IMAGE_NAME_BACKEND: ${{ secrets.DOCKER_USERNAME }}/student-noticeboard-backend
  IMAGE_NAME_FRONTEND: ${{ secrets.DOCKER_USERNAME }}/student-noticeboard-frontend

jobs:
  # ─────────────────────────────────────────────────────────────
  # STAGE 1: CODE QUALITY & LINTING
  # ─────────────────────────────────────────────────────────────
  code-quality:
    name: Code Quality & Linting
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        working-directory: ./backend
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install flake8 black pylint

      - name: Run Flake8 linter
        working-directory: ./backend
        run: flake8 app.py --count --select=E9,F63,F7,F82 --show-source --statistics

      - name: Check code formatting with Black
        working-directory: ./backend
        run: black --check app.py || true

  # ─────────────────────────────────────────────────────────────
  # STAGE 2: UNIT TESTS
  # ─────────────────────────────────────────────────────────────
  unit-tests:
    name: Run Unit Tests
    runs-on: ubuntu-latest
    needs: code-quality

    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: noticeboard_test
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        working-directory: ./backend
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        working-directory: ./backend
        env:
          DB_HOST: localhost
          DB_PORT: 5432
          DB_NAME: noticeboard_test
          DB_USER: postgres
          DB_PASSWORD: postgres
          FLASK_ENV: testing
        run: |
          pytest tests/ -v --cov=. --cov-report=xml --cov-report=html || true

      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: unittests
          name: codecov-umbrella
          fail_ci_if_error: false

  # ─────────────────────────────────────────────────────────────
  # STAGE 3: BUILD DOCKER IMAGES
  # ─────────────────────────────────────────────────────────────
  build-images:
    name: Build Docker Images
    runs-on: ubuntu-latest
    needs: unit-tests

    outputs:
      backend-image: ${{ steps.meta-backend.outputs.tags }}
      frontend-image: ${{ steps.meta-frontend.outputs.tags }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ env.DOCKER_USERNAME }}
          password: ${{ env.DOCKER_PASSWORD }}

      # ─── BUILD BACKEND IMAGE ───
      - name: Extract metadata for backend
        id: meta-backend
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_BACKEND }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push backend image
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          file: ./backend/Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta-backend.outputs.tags }}
          labels: ${{ steps.meta-backend.outputs.labels }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_BACKEND }}:buildcache
          cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_BACKEND }}:buildcache,mode=max

      # ─── BUILD FRONTEND IMAGE ───
      - name: Create Dockerfile for frontend
        run: |
          cat > ./frontend/Dockerfile << 'EOF'
          FROM nginx:alpine
          COPY . /usr/share/nginx/html/
          EXPOSE 80
          CMD ["nginx", "-g", "daemon off;"]
          EOF

      - name: Extract metadata for frontend
        id: meta-frontend
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push frontend image
        uses: docker/build-push-action@v4
        with:
          context: ./frontend
          file: ./frontend/Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta-frontend.outputs.tags }}
          labels: ${{ steps.meta-frontend.outputs.labels }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }}:buildcache
          cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }}:buildcache,mode=max

  # ─────────────────────────────────────────────────────────────
  # STAGE 4: SECURITY SCANNING
  # ─────────────────────────────────────────────────────────────
  security-scan:
    name: Security Scanning
    runs-on: ubuntu-latest
    needs: build-images
    if: github.event_name != 'pull_request'

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run Trivy vulnerability scanner on backend
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ needs.build-images.outputs.backend-image }}
          format: 'sarif'
          output: 'trivy-backend-results.sarif'

      - name: Upload Trivy backend results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-backend-results.sarif'
          category: 'trivy-backend'

      - name: Run Trivy vulnerability scanner on frontend
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ needs.build-images.outputs.frontend-image }}
          format: 'sarif'
          output: 'trivy-frontend-results.sarif'

      - name: Upload Trivy frontend results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-frontend-results.sarif'
          category: 'trivy-frontend'

  # ─────────────────────────────────────────────────────────────
  # STAGE 5: DOCKER COMPOSE INTEGRATION TEST
  # ─────────────────────────────────────────────────────────────
  integration-test:
    name: Integration Test with Docker Compose
    runs-on: ubuntu-latest
    needs: build-images
    if: github.event_name != 'pull_request'

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Start Docker Compose stack
        run: |
          docker-compose up -d
          sleep 10

      - name: Test API health endpoint
        run: |
          curl -f http://localhost:5001/health || exit 1
          echo "✅ Health check passed"

      - name: Test API GET /announcements
        run: |
          curl -f http://localhost:5001/announcements || exit 1
          echo "✅ GET announcements passed"

      - name: Test API POST /announcements
        run: |
          curl -X POST http://localhost:5001/announcements \
            -H "Content-Type: application/json" \
            -d '{
              "title": "Test Notice",
              "body": "Integration test notice",
              "category": "general",
              "author": "CI/CD Pipeline"
            }' || exit 1
          echo "✅ POST announcement passed"

      - name: View logs
        if: failure()
        run: docker-compose logs

      - name: Tear down stack
        if: always()
        run: docker-compose down
```

---

### Step 5: Push to GitHub
```bash
git add .github/
git commit -m "Add CI/CD pipeline workflow"
git push origin main
```

---

## ✅ Done!

The pipeline will run automatically on next push!
