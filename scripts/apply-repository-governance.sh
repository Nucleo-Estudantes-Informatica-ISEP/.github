#!/usr/bin/env bash
set -euo pipefail

ORG="${ORG:-Nucleo-Estudantes-Informatica-ISEP}"
API_ROOT="${GITHUB_API_URL:-https://api.github.com}"
API_VERSION="${GITHUB_API_VERSION:-2026-03-10}"
DRY_RUN="${DRY_RUN:-false}"

: "${GH_TOKEN:?Set GH_TOKEN to a fine-grained PAT with Administration: read/write on the target repositories}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

REPOS=(
  antirecurso
  antirecurso-api-adonis
  orbit
  unclassed
  fallstack-website
)

RULESET_SPECS=(
  "antirecurso:rulesets/antirecurso-main.json"
  "antirecurso-api-adonis:rulesets/antirecurso-api-adonis-main.json"
  "orbit:rulesets/orbit-main.json"
  "unclassed:rulesets/unclassed-main.json"
  "unclassed:rulesets/unclassed-dev.json"
  "fallstack-website:rulesets/fallstack-main.json"
  "fallstack-website:rulesets/fallstack-dev.json"
)

api_get() {
  local path="$1"
  curl --fail-with-body --silent --show-error --location \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${GH_TOKEN}" \
    -H "X-GitHub-Api-Version: ${API_VERSION}" \
    "${API_ROOT}${path}"
}

api_write() {
  local method="$1"
  local path="$2"
  local data_file="${3:-}"

  if [[ "$DRY_RUN" == "true" ]]; then
    printf '[dry-run] %s %s\n' "$method" "$path"
    return 0
  fi

  local args=(
    --fail-with-body --silent --show-error --location
    --request "$method"
    -H "Accept: application/vnd.github+json"
    -H "Authorization: Bearer ${GH_TOKEN}"
    -H "X-GitHub-Api-Version: ${API_VERSION}"
  )

  if [[ -n "$data_file" ]]; then
    args+=( -H "Content-Type: application/json" --data-binary "@${data_file}" )
  fi

  curl "${args[@]}" "${API_ROOT}${path}" >/dev/null
}

write_json() {
  local method="$1"
  local path="$2"
  local json="$3"
  local tmp
  tmp="$(mktemp)"
  printf '%s\n' "$json" > "$tmp"
  api_write "$method" "$path" "$tmp"
  rm -f "$tmp"
}

enable_security() {
  local repo="$1"
  local base="/repos/${ORG}/${repo}"

  echo "==> ${repo}: dependency alerts"
  api_write PUT "${base}/vulnerability-alerts"

  echo "==> ${repo}: Dependabot security updates"
  api_write PUT "${base}/automated-security-fixes"

  echo "==> ${repo}: secret scanning + push protection"
  write_json PATCH "$base" '{"security_and_analysis":{"secret_scanning":{"status":"enabled"},"secret_scanning_push_protection":{"status":"enabled"}}}'

  echo "==> ${repo}: CodeQL default setup"
  write_json PATCH "${base}/code-scanning/default-setup" '{"state":"configured"}'
}

upsert_ruleset() {
  local repo="$1"
  local relative_file="$2"
  local file="${ROOT_DIR}/${relative_file}"

  [[ -f "$file" ]] || { echo "Missing ruleset file: $file" >&2; exit 1; }
  jq empty "$file"

  local name target existing id
  name="$(jq -r '.name' "$file")"
  target="$(jq -r '.target // "branch"' "$file")"
  existing="$(api_get "/repos/${ORG}/${repo}/rulesets")"
  id="$(jq -r --arg name "$name" --arg target "$target" '.[] | select(.name == $name and .target == $target) | .id' <<<"$existing" | head -n1)"

  if [[ -n "$id" ]]; then
    echo "==> ${repo}: update ruleset ${name} (${id})"
    api_write PUT "/repos/${ORG}/${repo}/rulesets/${id}" "$file"
  else
    echo "==> ${repo}: create ruleset ${name}"
    api_write POST "/repos/${ORG}/${repo}/rulesets" "$file"
  fi
}

command -v curl >/dev/null
command -v jq >/dev/null

for repo in "${REPOS[@]}"; do
  enable_security "$repo"
done

for spec in "${RULESET_SPECS[@]}"; do
  repo="${spec%%:*}"
  file="${spec#*:}"
  upsert_ruleset "$repo" "$file"
done

echo "Governance baseline applied successfully."
