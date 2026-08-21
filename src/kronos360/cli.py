from __future__ import annotations
import argparse
import json
from .crypto.signatures import DemoSigner
from .services.evidence import issue_record, migrate_record, verify_record


def main() -> None:
    parser = argparse.ArgumentParser(prog="kronos360")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo")
    args = parser.parse_args()
    if args.command == "demo":
        classic = DemoSigner(b"development-classical")
        pqc = DemoSigner(b"development-pqc")
        pairs = [("ECDSA-P256-DEMO", "key-classical-dev", classic, "transition"), ("ML-DSA-DEMO", "key-pqc-dev", pqc, "post_quantum")]
        record = issue_record("KRONOS-000001", b"hello KRONOS", pairs, issued_at="2026-08-21T20:00:00Z")
        verification = verify_record(record, b"hello KRONOS", {"key-classical-dev": classic, "key-pqc-dev": pqc})
        migrated = migrate_record(record, pairs)
        print(json.dumps({"record": record.to_dict(), "verification": verification, "migration": migrated.to_dict()}, indent=2))


if __name__ == "__main__":
    main()
