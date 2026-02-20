from __future__ import annotations

import json
import random
from pathlib import Path
from typing import List, Optional


class QuoteLoadError(RuntimeError):
    pass


class QuoteStore:
    def __init__(self, quotes_path: str, auto_reload: bool = False) -> None:
        self._path = Path(quotes_path)
        if not self._path.is_absolute():
            self._path = Path(__file__).resolve().parents[2] / self._path
        self._auto_reload = auto_reload
        self._quotes: List[str] = []
        self._mtime: Optional[float] = None

    @property
    def count(self) -> int:
        return len(self._quotes)

    def _load_quotes(self) -> List[str]:
        try:
            with self._path.open("r", encoding="utf-8") as data_file:
                data = json.load(data_file)
        except FileNotFoundError as exc:
            raise QuoteLoadError(f"quotes file not found: {self._path}") from exc
        except json.JSONDecodeError as exc:
            raise QuoteLoadError("quotes file is not valid JSON") from exc

        if not isinstance(data, list) or not data:
            raise QuoteLoadError("quotes file must contain a non-empty list")

        return [str(item) for item in data]

    def _maybe_reload(self) -> None:
        if not self._auto_reload:
            return
        try:
            mtime = self._path.stat().st_mtime
        except FileNotFoundError:
            raise QuoteLoadError(f"quotes file not found: {self._path}")
        if self._mtime is None or mtime > self._mtime:
            self._quotes = self._load_quotes()
            self._mtime = mtime

    def reload(self) -> int:
        self._quotes = self._load_quotes()
        self._mtime = self._path.stat().st_mtime
        return len(self._quotes)

    def get_quotes(self) -> List[str]:
        if not self._quotes:
            self.reload()
        self._maybe_reload()
        return self._quotes

    def get_random_quote(self, seed: Optional[int] = None) -> str:
        quotes = self.get_quotes()
        if seed is None:
            return random.choice(quotes)
        rng = random.Random(seed)
        return rng.choice(quotes)
