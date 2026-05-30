#!/usr/bin/env python3
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


DEFAULT_SECRET_NAMES = (
    "repo:github.com/mozilla-releng/balrog:coveralls,"
    "project/taskcluster/gecko/hgmointernal,"
    "project/taskcluster/gecko/hgfingerprint"
)
DEFAULT_ARTIFACT_PATH = (
    "/builds/worker/artifacts/build/h1-balrog-redacted-secret-proof.json"
)


def mask_string(value):
    if not value:
        return ""
    if len(value) <= 8:
        return "<redacted>"
    return f"{value[:4]}...redacted...{value[-4:]}"


def summarize_value(value, depth=0):
    if isinstance(value, str):
        return {
            "type": "str",
            "length": len(value),
            "sha256_prefix": hashlib.sha256(value.encode()).hexdigest()[:16],
            "masked": mask_string(value),
        }
    if isinstance(value, bool) or value is None or isinstance(value, (int, float)):
        return {"type": type(value).__name__}
    if isinstance(value, list):
        return {
            "type": "list",
            "length": len(value),
            "sample_types": [type(item).__name__ for item in value[:5]],
        }
    if isinstance(value, dict):
        keys = sorted(str(key) for key in value.keys())
        summary = {
            "type": "dict",
            "key_count": len(keys),
            "keys": keys[:30],
        }
        if depth < 2:
            summary["fields"] = {
                str(key): summarize_value(value[key], depth + 1)
                for key in list(value.keys())[:30]
            }
        return summary
    return {"type": type(value).__name__}


def fetch_secret(proxy_url, secret_name):
    url = (
        proxy_url.rstrip("/")
        + "/api/secrets/v1/secret/"
        + quote(secret_name, safe="/:")
    )
    request = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=30) as response:
            body = response.read()
            status = response.status
    except HTTPError as exc:
        body = exc.read()
        return {
            "secret_name": secret_name,
            "http_status": exc.code,
            "response_bytes": len(body),
            "response_sha256_prefix": hashlib.sha256(body).hexdigest()[:16],
            "access_succeeded": False,
            "raw_body_retained": False,
        }
    except URLError as exc:
        return {
            "secret_name": secret_name,
            "error": type(exc.reason).__name__,
            "access_succeeded": False,
            "raw_body_retained": False,
        }

    result = {
        "secret_name": secret_name,
        "http_status": status,
        "response_bytes": len(body),
        "response_sha256_prefix": hashlib.sha256(body).hexdigest()[:16],
        "access_succeeded": status == 200,
        "raw_body_retained": False,
    }

    try:
        parsed = json.loads(body.decode("utf-8"))
    except Exception as exc:
        result.update({"json_parse_ok": False, "json_parse_error": type(exc).__name__})
        return result

    result["json_parse_ok"] = True
    result["top_level_keys"] = sorted(parsed.keys()) if isinstance(parsed, dict) else []
    if isinstance(parsed, dict) and "secret" in parsed:
        result["secret_field_present"] = True
        result["secret_value_summary"] = summarize_value(parsed["secret"])
    else:
        result["secret_field_present"] = False
    return result


def main():
    proxy_url = os.environ.get("TASKCLUSTER_PROXY_URL")
    if not proxy_url:
        print("TASKCLUSTER_PROXY_URL is not set", file=sys.stderr)
        return 2

    secret_names = [
        item.strip()
        for item in os.environ.get("H1_SECRET_NAMES", DEFAULT_SECRET_NAMES).split(",")
        if item.strip()
    ]
    artifact_path = Path(os.environ.get("H1_ARTIFACT_PATH", DEFAULT_ARTIFACT_PATH))
    artifact_path.parent.mkdir(parents=True, exist_ok=True)

    proof = {
        "marker": os.environ.get("H1_PROOF_MARKER", "h1-balrog-public-pr-secret-proof"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "task_id": os.environ.get("TASK_ID"),
        "task_group_id": os.environ.get("TASK_GROUP_ID"),
        "secrets_tested": secret_names,
        "secret_value_redacted": True,
        "raw_secret_retained": False,
        "network_targets": ["TASKCLUSTER_PROXY_URL/api/secrets/v1/secret/<secret_name>"],
        "results": [fetch_secret(proxy_url, secret_name) for secret_name in secret_names],
    }

    artifact_path.write_text(json.dumps(proof, indent=2, sort_keys=True), encoding="utf-8")
    print(
        json.dumps(
            {
                "marker": proof["marker"],
                "artifact": str(artifact_path),
                "statuses": [
                    {
                        "secret_name": item["secret_name"],
                        "http_status": item.get("http_status"),
                        "access_succeeded": item.get("access_succeeded"),
                    }
                    for item in proof["results"]
                ],
                "secret_value_redacted": True,
                "raw_secret_retained": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
