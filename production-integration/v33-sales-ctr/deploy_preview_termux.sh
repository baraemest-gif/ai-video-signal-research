#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SITE_ROOT="${1:-$PWD}"
BRANCH="v33-sales-ctr-preview"
PROJECT="ai-video-signal"

cd "$SITE_ROOT"
python "$HOME/aivs-v33-tools/patch_current_production.py" .
python "$HOME/aivs-v33-tools/patch_current_production.py" . --apply --manifest "$HOME/aivs-v33-tools/qa-manifest.json"

npx wrangler@latest pages deploy . --project-name="$PROJECT" --branch="$BRANCH"

echo
echo "STOP: validate the preview URL on desktop + mobile. Do NOT promote yet."
