from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, Optional
from uuid import uuid4

from flask import Flask, g, request
from flask_restful import Api, Resource

from .quotes import QuoteLoadError, QuoteStore


def create_app(config: Optional[Dict[str, Any]] = None) -> Flask:
    app = Flask(__name__)
    api = Api(app)

    quotes_path = os.getenv("QUOTES_PATH", "quotes.json")
    auto_reload = os.getenv("QUOTES_AUTO_RELOAD", "false").lower() in {
        "1",
        "true",
        "yes",
    }

    app.config.update(
        {
            "QUOTES_PATH": quotes_path,
            "QUOTES_AUTO_RELOAD": auto_reload,
        }
    )
    if config:
        app.config.update(config)

    app.extensions["quote_store"] = QuoteStore(
        app.config["QUOTES_PATH"],
        auto_reload=app.config["QUOTES_AUTO_RELOAD"],
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    @app.before_request
    def assign_request_id() -> None:
        g.request_id = request.headers.get("X-Request-Id", str(uuid4()))
        g._start_time = time.perf_counter()

    @app.after_request
    def log_request(response):
        duration_ms = (time.perf_counter() - g._start_time) * 1000
        app.logger.info(
            "%s %s %s %.2fms request_id=%s",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
            g.request_id,
        )
        return response

    def with_meta(payload: Dict[str, Any]) -> Dict[str, Any]:
        payload.setdefault("source", "rick-morty")
        payload.setdefault("request_id", g.request_id)
        return payload

    class RandomQuote(Resource):
        @staticmethod
        def get():
            seed = request.args.get("seed")
            if seed is not None:
                try:
                    seed_int = int(seed)
                except ValueError:
                    return with_meta({"error": "seed must be an integer"}), 400
            else:
                seed_int = None

            store: QuoteStore = app.extensions["quote_store"]
            try:
                r_quote = store.get_random_quote(seed=seed_int)
                count = store.count
            except QuoteLoadError as exc:
                return with_meta({"error": str(exc)}), 500

            return with_meta({"quote": r_quote, "count": count})

    class Health(Resource):
        @staticmethod
        def get():
            return with_meta({"status": "ok"})

    class Reload(Resource):
        @staticmethod
        def post():
            store: QuoteStore = app.extensions["quote_store"]
            try:
                count = store.reload()
            except QuoteLoadError as exc:
                return with_meta({"error": str(exc)}), 500

            return with_meta({"status": "reloaded", "count": count})

    api.add_resource(RandomQuote, "/")
    api.add_resource(Health, "/health")
    api.add_resource(Reload, "/reload")
    return app


if __name__ == "__main__":
    debug = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes"}
    port = int(os.getenv("PORT", "5000"))
    create_app().run(debug=debug, host="0.0.0.0", port=port)
