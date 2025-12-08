#!/usr/bin/env python
"""
download_data.py

Utility script for acquiring and verifying raw data files used in the project.
For this course project, some datasets (EPA eGRID, EIA Form 860) are downloaded
manually due to license/portal constraints. This script mainly:

- Verifies that expected raw files exist in data/raw/
- Optionally computes and prints file sizes and basic checksums
- Writes a small log to docs/provenance_download.log

Usage:
    python scripts/download_data.py
"""

import hashlib
import os
from pathlib import Path
from datetime import datetime

RAW_DIR = Path("data/raw")
DOCS_DIR = Path("docs")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

EXPECTED_FILES = {
    "egrid_2023.csv": "EPA eGRID 2023 (converted to CSV)",
    "eia860_2024.csv": "EIA Form 860 2024 (CSV extract)",
    "osint_ai_centers_raw.csv": "OSINT AI data center registry (manually compiled)",
}


def file_checksum(path: Path, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    log_lines = []
    log_lines.append(f"# Download / acquisition check\n")
    log_lines.append(f"Timestamp: {datetime.utcnow().isoformat()}Z\n")

    for filename, desc in EXPECTED_FILES.items():
        p = RAW_DIR / filename
        if not p.exists():
            log_lines.append(f"[MISSING] {filename} – {desc}\n")
            continue

        size_mb = p.stat().st_size / (1024 * 1024)
        checksum = file_checksum(p)
        log_lines.append(f"[OK] {filename} – {desc}\n")
        log_lines.append(f"    Size: {size_mb:.2f} MB\n")
        log_lines.append(f"    SHA256: {checksum}\n")

    out_log = DOCS_DIR / "provenance_download.log"
    with out_log.open("a", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
        f.write("\n" + "-" * 60 + "\n")

    print("Acquisition check complete. See docs/provenance_download.log for details.")


if __name__ == "__main__":
    main()
