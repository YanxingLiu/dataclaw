#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

source .venv/bin/activate

PUSH=true
if [[ "${1:-}" == "--push" ]]; then
  PUSH=true
  shift
fi

FULL_NAME="${1:-Yanxing Liu}"
EXPORT_FILE="${EXPORT_FILE:-$ROOT_DIR/dataclaw_conversations.jsonl}"
PUBLISH_ATTESTATION="${PUBLISH_ATTESTATION:-User explicitly approved publishing to Hugging Face.}"

ATTEST_FULL_NAME="${ATTEST_FULL_NAME:-Asked for full name and scanned export for YanxingLiu, lyx, and ${FULL_NAME}; exact-name matches were reviewed and redacted before final export.}"
ATTEST_SENSITIVE="${ATTEST_SENSITIVE:-Asked about company/client/internal names and private URLs; user provided liuyanxing98@foxmail.com and no other additional redactions. Added redactions for the email, private URLs, and additional sensitive strings found during review before re-exporting.}"
ATTEST_MANUAL_SCAN="${ATTEST_MANUAL_SCAN:-Manually scanned 20 sessions across beginning, middle, and end, reviewed findings with the user, and re-exported after adding redactions for exact-name and high-entropy sensitive strings.}"

dataclaw status
dataclaw export --no-push -o "$EXPORT_FILE"

echo
echo "Review $EXPORT_FILE, run any needed dataclaw config --redact/--exclude, then press Enter to continue."
read -r

dataclaw confirm \
  --file "$EXPORT_FILE" \
  --full-name "$FULL_NAME" \
  --attest-full-name "$ATTEST_FULL_NAME" \
  --attest-sensitive "$ATTEST_SENSITIVE" \
  --attest-manual-scan "$ATTEST_MANUAL_SCAN"

if [[ "$PUSH" == "true" ]]; then
  echo
  echo "Press Enter to publish to Hugging Face."
  read -r
  dataclaw export --publish-attestation "$PUBLISH_ATTESTATION"
else
  echo
  echo "Review complete. Re-run with --push when you want to publish."
fi
