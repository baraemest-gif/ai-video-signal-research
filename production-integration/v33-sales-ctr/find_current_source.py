#!/usr/bin/env python3
"""Find exactly one AI Video Signal source tree that passes v33 safety guards.

Scans directories and AI-Video-Signal/AIVS ZIPs under supplied roots. ZIPs are
validated in temporary extraction folders. It never edits a candidate.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATCH = HERE / "patch_current_production.py"
REQUIRED = [
    "_worker.js",
    "elevenlabs-cancellation-refund-policy/index.html",
    "filmora-free-vs-paid/index.html",
    "best-ai-video-tools-for-compliance-training/index.html",
    "filmora-free-trial/index.html",
    "ai-video-pricing-benchmarks/index.html",
    "ai-video-annual-vs-monthly-pricing-comparison/index.html",
    "ai-video-credits-usage-comparison/index.html",
]

def looks_like_site(p: Path) -> bool:
    return p.is_dir() and all((p / rel).is_file() for rel in REQUIRED)

def guard_ok(p: Path) -> tuple[bool, str]:
    cp = subprocess.run([sys.executable, str(PATCH), str(p)], text=True, capture_output=True)
    return cp.returncode == 0, (cp.stdout + cp.stderr).strip()

def dir_candidates(root: Path):
    if not root.exists():
        return
    if looks_like_site(root):
        yield root
    try:
        for worker in root.rglob("_worker.js"):
            p = worker.parent
            if looks_like_site(p):
                yield p
    except (PermissionError, OSError):
        return

def zip_candidates(root: Path):
    if not root.exists():
        return
    seen=set()
    for pat in ("AI-Video-Signal*.zip", "AIVS*.zip"):
        try:
            for p in root.rglob(pat):
                if p not in seen:
                    seen.add(p)
                    yield p
        except (PermissionError, OSError):
            pass

def detect_zip_prefix(z: zipfile.ZipFile) -> str | None:
    names = [n.lstrip("./") for n in z.namelist() if not n.endswith("/")]
    for w in [n for n in names if n.endswith("_worker.js")]:
        prefix=w[:-len("_worker.js")]
        if all(prefix+rel in names for rel in REQUIRED):
            return prefix
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("roots", nargs="*", type=Path, default=[Path.home(), Path("/storage/emulated/0/Download")])
    ap.add_argument("--extract-to", type=Path, default=Path.home()/"aivs-v33-current-source")
    args=ap.parse_args()
    passed=[]; checked=set()
    for root in args.roots:
        root=root.expanduser().resolve()
        for p in dir_candidates(root):
            rp=str(p.resolve())
            if rp in checked:
                continue
            checked.add(rp)
            ok, detail=guard_ok(p)
            if ok:
                passed.append({"kind":"dir","path":rp,"detail":detail})
    if not passed:
        for root in args.roots:
            root=root.expanduser().resolve()
            for zp in zip_candidates(root):
                try:
                    with zipfile.ZipFile(zp) as z:
                        prefix=detect_zip_prefix(z)
                        if prefix is None:
                            continue
                        with tempfile.TemporaryDirectory(prefix="aivs-v33-check-") as td:
                            td=Path(td)
                            z.extractall(td)
                            site=td/prefix if prefix else td
                            ok, detail=guard_ok(site)
                            if ok:
                                passed.append({"kind":"zip","path":str(zp),"prefix":prefix,"detail":detail})
                except (zipfile.BadZipFile, OSError):
                    continue
    if len(passed) != 1:
        print(json.dumps({"status":"STOP","valid_candidates":len(passed),"candidates":[{k:v for k,v in x.items() if k!="detail"} for x in passed]}, indent=2))
        return 3
    c=passed[0]
    if c["kind"] == "dir":
        print(c["path"])
        return 0
    dest=args.extract_to.expanduser().resolve()
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    with zipfile.ZipFile(c["path"]) as z:
        z.extractall(dest)
    site=dest/c.get("prefix","") if c.get("prefix") else dest
    ok, detail=guard_ok(site)
    if not ok:
        print("STOP: extracted ZIP failed re-validation", file=sys.stderr)
        return 4
    print(str(site))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
