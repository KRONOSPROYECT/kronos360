from __future__ import annotations
import hashlib


def sha3_512_hex(payload: bytes) -> str:
    return hashlib.sha3_512(payload).hexdigest()
