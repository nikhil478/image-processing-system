# Image Processing System

A simple image processing system. Hosted Server will be up till 3 MARCH 2025 (http://54.204.88.148/docs)


Prerequisites

Ensure you have the following installed:

Docker

Docker Compose

Getting Started

1. Build and Start the Containers

Run the following command to build and start the services:

```sh
docker-compose up --build
```

This will start the API, worker, database, and other necessary services.

2. Stop and Remove Containers

To stop and remove the running containers, use:

```sh
docker-compose down
```

## Setup

### 1. Check Python Version
Ensure Python is installed:
```sh
python3 --version
```

### 2. Create and Activate Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### 4. Run the Server
Development:
```sh
uvicorn app.main:app --reload
```

Production:
```sh
gunicorn -k uvicorn.workers.UvicornWorker app.main:app --workers 4
```

## Background Services
Start Redis:
```sh
docker run --name redis-server -d -p 6379:6379 redis:latest
```
Start Celery worker:
```sh
celery -A app.workers.celery.celery worker --loglevel=info
```

## Database Migrations
Autogenerate migration files:
```sh
alembic revision --autogenerate -m "Migration description"
```
Example:
```sh
alembic revision --autogenerate -m "Added new column to ProcessingRequest"
```
Apply migrations:
```sh
alembic upgrade head
```
Check current migration version:
```sh
alembic current
```
Rollback migration:
```sh
alembic downgrade -1
```
