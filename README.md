# rick-morty-python-api

A simple Flask API that serves a random Rick and Morty quote from `quotes.json`.

## Requirements

You can run this project either with Docker (recommended) or directly with Python.

### Docker (recommended)

- Docker
- Docker Compose (v2)

### Local Python

- Python 3.10+
- pip

## Run With Docker

Build and run the container:

```bash
docker build -t rick-morty-python-api .
docker run --rm -p 5000:5000 rick-morty-python-api
```

Then call the API:

```bash
curl http://localhost:5000/
```

## Run With Docker Compose

```bash
docker compose up --build
```

Then call the API:

```bash
curl http://localhost:8888/
```

## Run Locally (Python)

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app/app.py
```

Then call the API:

```bash
curl http://localhost:5000/
```
