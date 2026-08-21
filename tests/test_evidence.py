import pytest
from kronos360.crypto.canonicalization import canonicalize
from kronos360.crypto.hashing import sha3_512_hex
from kronos360.crypto.signatures import DemoSigner
from kronos360.services.evidence import issue_record, migrate_record, verify_record


def pairs():
    return [
        ("ECDSA-P256-DEMO", "classic", DemoSigner(b"classic"), "transition"),
        ("ML-DSA-DEMO", "pqc", DemoSigner(b"pqc"), "post_quantum"),
    ]


def test_canonicalization_is_deterministic():
    assert canonicalize({"b": 2, "a": 1}) == canonicalize({"a": 1, "b": 2})


def test_sha3_512_is_stable():
    assert sha3_512_hex(b"abc") == sha3_512_hex(b"abc")
    assert sha3_512_hex(b"abc") != sha3_512_hex(b"abd")


def test_issue_and_verify_hybrid_record():
    ps = pairs()
    record = issue_record("R-1", b"document", ps, issued_at="2026-01-01T00:00:00Z")
    result = verify_record(record, b"document", {"classic": ps[0][2], "pqc": ps[1][2]})
    assert result["overall_valid"] is True
    assert result["ECDSA-P256-DEMO.valid"] is True
    assert result["ML-DSA-DEMO.valid"] is True


def test_tampering_fails_hash_verification():
    ps = pairs()
    record = issue_record("R-2", b"document", ps)
    result = verify_record(record, b"tampered", {"classic": ps[0][2], "pqc": ps[1][2]})
    assert result["content_hash_valid"] is False
    assert result["overall_valid"] is False


def test_migration_does_not_overwrite_historical_record():
    ps = pairs()
    original = issue_record("R-3", b"document", ps)
    migrated = migrate_record(original, ps)
    assert original.record_id == "R-3"
    assert migrated.migration_of == original.record_id
    assert migrated.record_id != original.record_id
