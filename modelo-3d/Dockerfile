# Dockerfile del visor 3D
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /app/modelo-3d
CMD ["uvicorn", "visor:app", "--host", "0.0.0.0", "--port", "8000"]
