"""Authoring/verification harness for evals/field-debug/case-023 -- NOT
agent-visible (lives outside cases/case-023/, and the harness protocol
described in RESULTS.md only ever copies a case's own cases/case-0NN/
directory into a tested agent's sandbox).

Two things this proves mechanically, both cited in RESULTS.md and the PR
description rather than merely asserted:

1. The three-stage failure sequence (401 -> 422 -> 429 -> success) is
   real and deterministic against the actual fulfillco_client.py /
   fulfillco_sandbox.py code -- not a scripted narrative. Each stage is
   produced by applying exactly the fix a correct investigation would
   apply, one at a time, then re-running the real code.
2. The case's OWN agent-visible static files (context.md,
   partner_migration_notice.md, sync_log_so_far.md) never mention the
   stage-2 or stage-3 failure signatures ahead of time -- the only way to
   see them is to actually run the code after applying the prior stage's
   fix, which is exactly the discipline the grading key requires.

Run: python3 evals/field-debug/scripts/verify_case_023_progression.py
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CASE_DIR = REPO / "evals" / "field-debug" / "cases" / "case-023"

STAGE2_SIGNATURE = "missing required field"
STAGE3_SIGNATURE = "rate_limited"


def run(pyfile: Path, workdir: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(pyfile.name)],
        cwd=workdir,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout + result.stderr


def check_no_early_leakage():
    for name in ("context.md", "partner_migration_notice.md", "sync_log_so_far.md"):
        text = (CASE_DIR / name).read_text().lower()
        for sig in (STAGE2_SIGNATURE, STAGE3_SIGNATURE):
            assert sig not in text, f"leak: {name} mentions stage-2/3 signature {sig!r}"
    print("OK: no static agent-visible file mentions the stage-2/3 failure signatures")


def apply_auth_fix(client_src: str) -> str:
    fixed = client_src.replace(
        "import threading\nimport warnings",
        "import hashlib\nimport hmac\nimport threading\nimport warnings",
    ).replace(
        'API_KEY = "legacy-key-88214-DEPRECATED"',
        'HMAC_SECRET = "fc_live_secret_7f3a9c2e"',
    ).replace(
        "def build_headers(payload):\n    return {\"Authorization\": f\"Bearer {API_KEY}\"}",
        (
            "def build_headers(payload):\n"
            "    payload_hash = hashlib.sha256(str(payload).encode()).hexdigest()\n"
            "    sig = hmac.new(HMAC_SECRET.encode(), payload_hash.encode(), hashlib.sha256).hexdigest()\n"
            "    return {\"X-Fulfillco-Signature\": sig, \"X-Fulfillco-Payload-Hash\": payload_hash}"
        ),
    )
    assert fixed != client_src, "auth fix pattern did not match fulfillco_client.py"
    return fixed


def apply_schema_fix(client_src: str) -> str:
    fixed = client_src.replace('"line_items": order["items"],', '"items": order["items"],')
    assert fixed != client_src, "schema fix pattern did not match fulfillco_client.py"
    return fixed


def apply_concurrency_fix(client_src: str) -> str:
    fixed = client_src.replace(
        (
            "def sync_one(order, results):\n"
            "    warnings.warn(\n"
            "        \"fulfillco_sdk_compat: falling back to legacy TLS cipher list for this host\",\n"
            "        DeprecationWarning,\n"
            "        stacklevel=2,\n"
            "    )\n"
            "    payload = build_payload(order)\n"
            "    headers = build_headers(payload)\n"
            "    resp = submit_order(payload, headers)\n"
            "    results[order[\"order_id\"]] = resp\n"
            "\n"
            "\n"
            "def sync_batch(orders):\n"
            "    \"\"\"Fires the whole batch at once -- historically fine at our old,\n"
            "    much smaller nightly order volume.\"\"\"\n"
            "    results = {}\n"
            "    threads = [threading.Thread(target=sync_one, args=(o, results)) for o in orders]\n"
            "    for t in threads:\n"
            "        t.start()\n"
            "    for t in threads:\n"
            "        t.join()\n"
            "    return results"
        ),
        (
            "MAX_CONCURRENT_REQUESTS = 15  # stay under Fulfillco's documented 20-in-flight cap\n"
            "\n"
            "\n"
            "def sync_one(order, results, sem):\n"
            "    with sem:\n"
            "        warnings.warn(\n"
            "            \"fulfillco_sdk_compat: falling back to legacy TLS cipher list for this host\",\n"
            "            DeprecationWarning,\n"
            "            stacklevel=2,\n"
            "        )\n"
            "        payload = build_payload(order)\n"
            "        headers = build_headers(payload)\n"
            "        resp = submit_order(payload, headers)\n"
            "        results[order[\"order_id\"]] = resp\n"
            "\n"
            "\n"
            "def sync_batch(orders):\n"
            "    results = {}\n"
            "    sem = threading.Semaphore(MAX_CONCURRENT_REQUESTS)\n"
            "    threads = [threading.Thread(target=sync_one, args=(o, results, sem)) for o in orders]\n"
            "    for t in threads:\n"
            "        t.start()\n"
            "    for t in threads:\n"
            "        t.join()\n"
            "    return results"
        ),
    )
    assert fixed != client_src, "concurrency fix pattern did not match fulfillco_client.py"
    return fixed


def main():
    check_no_early_leakage()

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        for name in ("fulfillco_client.py", "fulfillco_sandbox.py", "run_sync.py"):
            shutil.copy(CASE_DIR / name, workdir / name)

        client_path = workdir / "fulfillco_client.py"

        # Stage 1: unmodified -- expect 100% 401.
        out = run(workdir / "run_sync.py", workdir)
        assert "401: 25 orders" in out, f"stage 1 did not reproduce as expected:\n{out}"
        assert "422" not in out and "429" not in out, f"stage-2/3 leaked into stage 1 output:\n{out}"
        print("OK: stage 1 (unmodified) -> 25/25 401, no 422/429 present")

        # Stage 2: apply the auth fix only -- expect 100% 422.
        src = client_path.read_text()
        client_path.write_text(apply_auth_fix(src))
        out = run(workdir / "run_sync.py", workdir)
        assert "422: 25 orders" in out, f"stage 2 did not reproduce after the auth fix:\n{out}"
        assert "401" not in out and "429" not in out, f"stage 1/3 leaked into stage 2 output:\n{out}"
        print("OK: stage 2 (auth fixed) -> 25/25 422, no 401/429 present")

        # Stage 3: also apply the schema fix -- expect a 20/5 200/429 split.
        src = client_path.read_text()
        client_path.write_text(apply_schema_fix(src))
        out = run(workdir / "run_sync.py", workdir)
        assert "200: 20 orders" in out and "429: 5 orders" in out, f"stage 3 did not reproduce after the schema fix:\n{out}"
        assert "401" not in out and "422" not in out, f"stage 1/2 leaked into stage 3 output:\n{out}"
        print("OK: stage 3 (auth + schema fixed) -> 20/25 accepted, 5/25 429, no 401/422 present")

        # Final: also apply the concurrency fix -- expect 100% success.
        src = client_path.read_text()
        client_path.write_text(apply_concurrency_fix(src))
        out = run(workdir / "run_sync.py", workdir)
        assert "200: 25 orders" in out, f"final fix did not resolve fully:\n{out}"
        print("OK: all three fixes applied -> 25/25 accepted")

    print("\nverify_case_023_progression: PASS")


if __name__ == "__main__":
    main()
