"""Development-only signer interface.

Replace DemoSigner with reviewed implementations for production. The demo signer
exists to exercise record flow and deliberately is not a cryptographic signature.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import hmac


class Signer:
    algorithm: str

    def sign(self, payload: bytes) -> str:
        raise NotImplementedError

    def verify(self, payload: bytes, signature: str) -> bool:
        raise NotImplementedError


@dataclass
class DemoSigner(Signer):
    key: bytes
    algorithm: str = "DEMO-NOT-FOR-PRODUCTION"

    def sign(self, payload: bytes) -> str:
        return hmac.new(self.key, payload, hashlib.sha256).hexdigest()

    def verify(self, payload: bytes, signature: str) -> bool:
        expected = self.sign(payload)
        return hmac.compare_digest(expected, signature)
