"""Deterministic serialization used before hashing/signing."""
from __future__ import annotations
import json
from typing import Any


def canonicalize(value: Any) -> bytes:
    """Return stable UTF-8 JSON bytes for protocol version kronos-c14n-1."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
