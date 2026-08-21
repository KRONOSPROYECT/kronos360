from __future__ import annotations
from datetime import datetime, timezone
from ..crypto.canonicalization import canonicalize
from ..crypto.hashing import sha3_512_hex
from ..crypto.signatures import Signer
from ..models.evidence import EvidenceRecord, SignatureRecord


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _signing_payload(content_hash: str, record_id: str, policy_version: str) -> bytes:
    return canonicalize({"record_id": record_id, "content_hash": content_hash, "policy_version": policy_version})


def issue_record(record_id: str, document: bytes, signer_pairs: list[tuple[str, str, Signer, str]], *, issued_at: str | None = None) -> EvidenceRecord:
    canonical_document = canonicalize({"media_type": "application/octet-stream", "bytes_hex": document.hex()})
    digest = sha3_512_hex(canonical_document)
    policy = "kronos-crypto-1.0"
    payload = _signing_payload(digest, record_id, policy)
    signatures = [
        SignatureRecord(algorithm=algorithm, key_id=key_id, signature=signer.sign(payload), status=status)
        for algorithm, key_id, signer, status in signer_pairs
    ]
    return EvidenceRecord(
        record_id=record_id,
        schema_version="1.0",
        content={"media_type": "application/octet-stream", "canonicalization": "kronos-c14n-1", "hash_algorithm": "SHA3-512", "hash": digest},
        signatures=signatures,
        issued_at=issued_at or utc_now(),
        policy_version=policy,
        audit_event_id=f"AUD-{record_id}",
    )


def verify_record(record: EvidenceRecord, document: bytes, signers: dict[str, Signer]) -> dict[str, bool]:
    canonical_document = canonicalize({"media_type": "application/octet-stream", "bytes_hex": document.hex()})
    digest = sha3_512_hex(canonical_document)
    payload = _signing_payload(digest, record.record_id, record.policy_version)
    result = {"content_hash_valid": digest == record.content["hash"]}
    for signature in record.signatures:
        signer = signers.get(signature.key_id)
        result[f"{signature.algorithm}.valid"] = bool(signer and signer.verify(payload, signature.signature))
    result["overall_valid"] = result["content_hash_valid"] and all(v for k, v in result.items() if k != "content_hash_valid")
    return result


def migrate_record(record: EvidenceRecord, signer_pairs: list[tuple[str, str, Signer]]) -> EvidenceRecord:
    """Create a new evidence record referencing the historical record."""
    payload_document = canonicalize({"historical_record_id": record.record_id, "historical_hash": record.content["hash"]})
    migrated = issue_record(f"MIG-{record.record_id}", payload_document, signer_pairs)
    migrated.migration_of = record.record_id
    return migrated
