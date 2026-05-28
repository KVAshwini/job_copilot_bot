import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#./ -]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokens(text: str) -> set[str]:
    return set(normalize(text).split())


def read_text(path: Path, default: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else default


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    normalized = normalize(text)
    return sorted({keyword for keyword in keywords if normalize(keyword) in normalized})


def comma_list(values: list[str]) -> str:
    return ", ".join(values)
