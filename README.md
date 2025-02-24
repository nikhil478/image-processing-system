```md
# Image Processing System

A image processing system.

## Setup

### 1. Check Python Version
Ensure Python is installed:  
```sh
python3 --version
```

### 2. Create and Activate Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Optional for development
```

### 4. Run the Development Server
```sh
uvicorn app.main:app --reload
```

### 5. Run in Production
```sh
gunicorn -k uvicorn.workers.UvicornWorker app.main:app --workers 4
```

## Notes
- Activate the virtual environment before running the project.
- Use `--reload` only in development.
- Gunicorn is recommended for production.


docker run --name redis-server -d -p 6379:6379 redis:latest
celery -A app.workers.celery.celery worker --loglevel=info


Autogenerate Migration Files
After defining or modifying SQLAlchemy models, create a migration script:

alembic revision --autogenerate -m "Describe the migration change"
Example:

alembic revision --autogenerate -m "Added new column to ProcessingRequest"

Apply the Migrations to Database
Run the migrations to update your PostgreSQL database:
alembic upgrade head

Check the Current Migration Version
Verify which migration is currently applied:
alembic current

Revert to a Previous Migration (If Needed)
Rollback to the previous version:
alembic downgrade -1