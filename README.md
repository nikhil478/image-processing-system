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
uvicorn app:app --reload
```

### 5. Run in Production
```sh
gunicorn -k uvicorn.workers.UvicornWorker app:app --workers 4
```

## Notes
- Activate the virtual environment before running the project.
- Use `--reload` only in development.
- Gunicorn is recommended for production.