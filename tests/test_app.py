import json
from pathlib import Path

from app.app import create_app


def test_random_quote_endpoint():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 200
    payload = response.get_json()
    assert "quote" in payload
    assert "count" in payload
    assert payload["source"] == "rick-morty"
    assert "request_id" in payload
    assert isinstance(payload["quote"], str)


def test_seeded_quote_is_deterministic():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        first = client.get("/?seed=123").get_json()["quote"]
        second = client.get("/?seed=123").get_json()["quote"]

    assert first == second


def test_seed_must_be_integer():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.get("/?seed=abc")

    assert response.status_code == 400


def test_health_endpoint():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_reload_endpoint(tmp_path: Path):
    quotes_path = tmp_path / "quotes.json"
    quotes_path.write_text(json.dumps(["hello", "world"]), encoding="utf-8")

    app = create_app({"QUOTES_PATH": str(quotes_path)})
    app.testing = True

    with app.test_client() as client:
        response = client.post("/reload")

    assert response.status_code == 200
    assert response.get_json()["count"] == 2


def test_missing_quotes_file_returns_error(tmp_path: Path):
    app = create_app({"QUOTES_PATH": str(tmp_path / "missing.json")})
    app.testing = True

    with app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 500
    assert "error" in response.get_json()


def test_invalid_quotes_file_returns_error(tmp_path: Path):
    quotes_path = tmp_path / "quotes.json"
    quotes_path.write_text("{not json", encoding="utf-8")

    app = create_app({"QUOTES_PATH": str(quotes_path)})
    app.testing = True

    with app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 500
    assert "error" in response.get_json()
