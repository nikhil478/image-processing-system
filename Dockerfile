FROM python:3.10

WORKDIR /app

COPY . .

RUN mkdir -p /app/uploads /app/static/images

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--workers", "4", "--bind", "0.0.0.0:8000"]