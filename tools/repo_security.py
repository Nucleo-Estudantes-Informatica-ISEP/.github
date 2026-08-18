#!/usr/bin/env python3
"""Audit or apply NEI repository rulesets and CodeQL Default Setup.

Usage:
    GITHUB_TOKEN=... python tools/repo_security.py
    GITHUB_TOKEN=... python tools/repo_security.py --apply
    GITHUB_TOKEN=... python tools/repo_security.py --repo fallstack-website --apply

By default the script is read-only. Pass --apply to create/update repository
rulesets from rulesets/*.json and enable CodeQL Default Setup where needed.

The token needs repository Administration read access for auditing, and
Administration write access when --apply is used.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_ROOT = "https://api.github.com"
API_VERSION = "2026-03-10"
DEFAULT_ORG = "Nucleo-Estudantes-Informatica-ISEP"
ROOT = Path(__file__).resolve().parents[1]

# Repository -> canonical repository-level ruleset presets.
PRESETS: dict[str, tuple[str, ...]] = {
    "fallstack-website": (
        "rulesets/fallstack-main.json",
        "rulesets/fallstack-dev.json",
    ),
    "orbit": ("rulesets/orbit-main.json",),
    "antirecurso": ("rulesets/antirecurso-main.json",),
    "antirecurso-api-adonis": ("rulesets/antirecurso-api-adonis-main.json",),
    "unclassed": (
        "rulesets/unclassed-main.json",
        "rulesets/unclassed-dev.json",
    ),
}


class ApiError(RuntimeError):
    def __init__(self, status: int, method: str, path: str, body: str) -> None:
        super().__init__(f"GitHub API {status} for {method} {path}: {body}")
        self.status = status
        self.method = method
        self.path = path
        self.body = body


def api_request(
    token: str,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    query: dict[str, str] | None = None,
) -> tuple[int, Any]:
    url = f"{API_ROOT}{path}"
    if query:
        url += "?" + urlencode(query)

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "nei-repo-security-sync",
            "Content-Type": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw else None
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise ApiError(exc.code, method, path, raw) from exc


def load_preset(relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def comparable_live_ruleset(live: dict[str, Any], desired: dict[str, Any]) -> dict[str, Any]:
    """Compare only canonical fields present in the preset.

    This intentionally preserves live-only fields such as bypass_actors when a
    preset does not define them.
    """

    return {key: live.get(key) for key in desired}


def audit_rulesets(token: str, org: str, repo: str, apply: bool) -> int:
    drift = 0
    preset_paths = PRESETS.get(repo, ())
    if not preset_paths:
        print(f"  rulesets: no canonical presets for {repo}; skipped")
        return drift

    _, summaries = api_request(
        token,
        "GET",
        f"/repos/{org}/{repo}/rulesets",
        query={"includes_parents": "false", "targets": "branch"},
    )

    by_name = {
        item["name"]: item
        for item in summaries
        if item.get("source_type") == "Repository"
    }

    for relative_path in preset_paths:
        desired = load_preset(relative_path)
        name = desired["name"]
        existing = by_name.get(name)

        if existing is None:
            print(f"  ruleset {name}: MISSING ({relative_path})")
            drift += 1
            if apply:
                _, created = api_request(
                    token,
                    "POST",
                    f"/repos/{org}/{repo}/rulesets",
                    payload=desired,
                )
                print(f"    -> created ruleset id={created['id']}")
            continue

        ruleset_id = existing["id"]
        _, live = api_request(
            token,
            "GET",
            f"/repos/{org}/{repo}/rulesets/{ruleset_id}",
            query={"includes_parents": "false"},
        )
        current = comparable_live_ruleset(live, desired)

        if current == desired:
            print(f"  ruleset {name}: OK (id={ruleset_id})")
            continue

        drift += 1
        print(f"  ruleset {name}: DRIFT (id={ruleset_id}, preset={relative_path})")
        for key in desired:
            if current.get(key) != desired.get(key):
                print(f"    - {key} differs")

        if apply:
            api_request(
                token,
                "PATCH",
                f"/repos/{org}/{repo}/rulesets/{ruleset_id}",
                payload=desired,
            )
            print("    -> updated from canonical preset")

    return drift


def find_local_codeql_workflows(token: str, org: str, repo: str) -> list[str]:
    try:
        _, items = api_request(
            token,
            "GET",
            f"/repos/{org}/{repo}/contents/.github/workflows",
        )
    except ApiError as exc:
        if exc.status == 404:
            return []
        raise

    return [
        item["path"]
        for item in items
        if "codeql" in item.get("name", "").lower()
        or "codeql" in item.get("path", "").lower()
    ]


def audit_codeql(token: str, org: str, repo: str, apply: bool) -> int:
    _, config = api_request(
        token,
        "GET",
        f"/repos/{org}/{repo}/code-scanning/default-setup",
    )

    state = config.get("state")
    if state == "configured":
        languages = ", ".join(config.get("languages") or []) or "auto"
        print(
            "  CodeQL Default Setup: OK "
            f"(languages={languages}, query_suite={config.get('query_suite', 'default')})"
        )
        return 0

    workflows = find_local_codeql_workflows(token, org, repo)
    suffix = f"; local workflow(s): {', '.join(workflows)}" if workflows else ""
    print(f"  CodeQL Default Setup: NOT CONFIGURED{suffix}")

    if not apply:
        return 1

    status, response = api_request(
        token,
        "PATCH",
        f"/repos/{org}/{repo}/code-scanning/default-setup",
        payload={"state": "configured"},
    )
    run_id = response.get("run_id") if isinstance(response, dict) else None
    extra = f", validation run={run_id}" if run_id else ""
    print(f"    -> enable requested (HTTP {status}{extra})")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit/apply NEI rulesets and CodeQL Default Setup."
    )
    parser.add_argument("--apply", action="store_true", help="Apply detected drift")
    parser.add_argument("--org", default=DEFAULT_ORG, help="GitHub organization")
    parser.add_argument(
        "--repo",
        action="append",
        choices=sorted(PRESETS),
        help="Limit to one repository; may be repeated",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--rulesets-only", action="store_true")
    mode.add_argument("--codeql-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("error: set GITHUB_TOKEN", file=sys.stderr)
        return 2

    repos = args.repo or sorted(PRESETS)
    drift = 0
    api_errors = 0

    print("mode:", "APPLY" if args.apply else "AUDIT (read-only)")
    print("organization:", args.org)

    for repo in repos:
        print(f"\n[{repo}]")
        try:
            if not args.codeql_only:
                drift += audit_rulesets(token, args.org, repo, args.apply)
            if not args.rulesets_only:
                drift += audit_codeql(token, args.org, repo, args.apply)
        except ApiError as exc:
            api_errors += 1
            print(f"  ERROR: {exc}")

    if args.apply:
        print(
            f"\ncompleted; detected {drift} drift item(s), "
            f"API errors={api_errors}"
        )
        return 1 if api_errors else 0

    if drift or api_errors:
        print(
            f"\naudit found {drift} drift item(s), "
            f"API errors={api_errors}"
        )
        return 1

    print("\naudit clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
