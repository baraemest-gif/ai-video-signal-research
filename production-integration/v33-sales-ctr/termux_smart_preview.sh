#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
TOOLS="$HOME/aivs-v33-tools"
PROJECT="ai-video-signal"
BRANCH="v33-sales-ctr-preview"

CURRENT="$($TOOLS/find_current_source.py "$HOME" /storage/emulated/0/Download)"
echo "Validated current source: $CURRENT"

python "$TOOLS/patch_current_production.py" "$CURRENT"
python "$TOOLS/patch_current_production.py" "$CURRENT" --apply --manifest "$TOOLS/qa-manifest.json"
cd "$CURRENT"
npx wrangler@latest pages deploy . --project-name="$PROJECT" --branch="$BRANCH"

echo
echo "STOP: preview deployed only. Validate the returned URL before any production promotion."
