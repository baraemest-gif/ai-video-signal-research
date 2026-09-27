# Test Results

## Test A — stale snapshot safety gate
Input: v32 package base containing several pages older than current live production.
Expected: abort before writing.
Result: PASS. Exit code 3; Filmora Free vs Paid, Compliance and Filmora Free Trial title guards rejected the stale source. No files were written.

## Test B — current-live metadata fixture, dry run
Expected: identify only the intended 7 files.
Result: PASS. Exactly 7 files staged.

## Test C — current-live metadata fixture, apply
Expected: write the same 7 files and keep infrastructure-critical files bit-identical.
Result: PASS.

Critical files verified unchanged by SHA-256 comparison:
- _worker.js
- assets/site.js
- assets/styles.css
- _headers

Other protected areas intentionally untouched:
- affiliate URLs / clickrefs
- checkout
- canonical URLs
- robots directives
- D1 / R2 / Cloudflare config
