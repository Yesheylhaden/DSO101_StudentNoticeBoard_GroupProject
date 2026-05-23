FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Create non-root user and switch to it
RUN useradd -m appuser
USER appuser

EXPOSE 5001

CMD ["python", "app.py"]