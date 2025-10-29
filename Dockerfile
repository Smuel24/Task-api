FROM python:3.12.6
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.infrastructure.http.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]