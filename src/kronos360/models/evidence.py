from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class SignatureRecord:
    algorithm: str
    key_id: str
    signature: str
    status: str


@dataclass
class EvidenceRecord:
    record_id: str
    schema_version: str
    content: dict[str, Any]
    signatures: list[SignatureRecord]
    issued_at: str
    policy_version: str
    audit_event_id: str
    migration_of: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
