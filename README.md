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

Optional query param:

```bash
curl "http://localhost:5000/?seed=123"
```

## Run With Docker Compose

```bash
docker compose up --build
```

Then call the API:

```bash
curl http://localhost:8888/
```

Optional query param:

```bash
curl "http://localhost:8888/?seed=123"
```

## Run Locally (Python)

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m app.app
```

Then call the API:

```bash
curl http://localhost:5000/
```

## Endpoints

- `GET /` returns a random quote
- `GET /health` returns a simple health check
- `POST /reload` reloads `quotes.json`

Examples:

```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/reload
```

## Quick Architecture

```
Client -> Flask API (src/app/app.py)
            |
            +-> QuoteStore (src/app/quotes.py)
                   |
                   +-> quotes.json
```

### Response Shape

All responses include:

- `source`: API identifier
- `request_id`: request correlation id

`GET /` also includes:

- `quote`: the quote text
- `count`: total quote count

Sample response:

```json
{
  "quote": "Wubba Lubba Dub-Dub!",
  "count": 42,
  "source": "rick-morty",
  "request_id": "6f5d2f9a-0c70-4c15-9c79-2a2a0b4f2e5f"
}
```

## Configuration

Environment variables:

- `QUOTES_PATH`: path to `quotes.json` (default: `quotes.json`)
- `QUOTES_AUTO_RELOAD`: auto-reload if file changes (`true`/`false`, default: `false`)
- `DEBUG`: Flask debug mode (`true`/`false`, default: `false`)
- `PORT`: server port (default: `5000`)

To set a custom request id, pass the `X-Request-Id` header.

## Project Layout

- `src/app`: Flask app package
- `tests`: pytest tests
- `quotes.json`: quote data

## Formatting And Linting

Configs are in `pyproject.toml`. Install tools if you want to run them locally:

```bash
python -m pip install black ruff
black src tests
ruff check src tests
```

## Testing

```bash
python -m pip install -r requirements.txt
pytest
```
