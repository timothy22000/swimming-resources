#!/usr/bin/env python3
"""
Build the Swimming Resources Database.

Reads all `data_part*.py` modules in this folder, validates each entry against
the schema, and emits:

  data/swimming_resources.json     - pretty-printed canonical JSON
  data/swimming_resources.jsonl    - one JSON object per line (HF-friendly)
  data/swimming_resources.csv      - flat tabular form (tags joined by `;`)
  data/swimming_resources.parquet  - columnar Parquet (pyarrow)

Run from the repo root:
    python scripts/build_dataset.py

Dependencies:
    pip install pandas pyarrow

Exit code is non-zero on any validation failure.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
SCRIPTS_DIR = REPO_ROOT / "scripts"

# Import all data parts
sys.path.insert(0, str(SCRIPTS_DIR))
from data_part1 import GOVERNING_BODIES, CATEGORY_IDS  # noqa: E402
from data_part2 import LEARN_TO_SWIM, TECHNIQUE  # noqa: E402
from data_part3 import YOUTUBE, TRAINING_PLANS  # noqa: E402
from data_part4 import APPS, BOOKS  # noqa: E402
from data_part5 import CERTIFICATIONS, SCIENCE  # noqa: E402
from data_part6 import NEWS, PODCASTS, GEAR  # noqa: E402
from data_part7 import OPEN_WATER, TRIATHLON, MASTERS  # noqa: E402
from data_part8 import PARA, DROWNING_PREVENTION, RECORDS  # noqa: E402
from data_part9 import COLLEGE, RECRUITING  # noqa: E402

ALL_RESOURCES: list[dict[str, Any]] = (
    GOVERNING_BODIES + LEARN_TO_SWIM + TECHNIQUE + YOUTUBE + TRAINING_PLANS
    + APPS + BOOKS + CERTIFICATIONS + SCIENCE + NEWS + PODCASTS + GEAR
    + OPEN_WATER + TRIATHLON + MASTERS + PARA + DROWNING_PREVENTION + RECORDS
    + COLLEGE + RECRUITING
)

CATEGORY_LABELS = {
    "governing_bodies": "Governing Bodies & Federations",
    "learn_to_swim": "Learn-to-Swim & Water Safety Programs",
    "technique": "Technique & Stroke Resources",
    "youtube": "YouTube Channels",
    "training_plans": "Training Plans & Workout Repositories",
    "apps": "Apps & Swim Technology",
    "books": "Books on Swimming",
    "certifications": "Coaching Certifications & Education",
    "science": "Sports Science, Biomechanics & Research",
    "news": "News, Communities & Magazines",
    "podcasts": "Podcasts",
    "gear": "Gear, Equipment & Reviews",
    "open_water": "Open Water & Marathon Swimming",
    "triathlon": "Triathlon Swimming",
    "masters": "Masters Swimming",
    "para": "Para Swimming & Adaptive Resources",
    "drowning_prevention": "Drowning Prevention & Public Health",
    "records": "Records, Rankings & Results Databases",
    "college": "College / NCAA Programs & Conferences",
    "recruiting": "Recruiting Services & Swim Camps",
}

REQUIRED_FIELDS = [
    "id", "category", "name", "type", "audience", "description", "url",
    "pricing", "region", "language", "status", "tags", "verified",
]

VALID_PRICING = {"free", "paid", "freemium", "mixed", "varies"}
VALID_STATUS = {"active", "rebranded", "defunct"}
URL_RE = re.compile(r"^https?://", re.IGNORECASE)
DATE_RE = re.compile(r"^\d{4}-\d{2}$")


def validate(resources: list[dict[str, Any]]) -> list[str]:
    """Return a list of human-readable error messages (empty = OK)."""
    errors: list[str] = []
    seen_ids: set[str] = set()
    for r in resources:
        rid = r.get("id", "<missing-id>")
        for field in REQUIRED_FIELDS:
            if field not in r or r[field] in (None, ""):
                errors.append(f"{rid}: missing required field '{field}'")
        if rid in seen_ids:
            errors.append(f"{rid}: duplicate id")
        seen_ids.add(rid)
        if r.get("category") not in CATEGORY_IDS:
            errors.append(f"{rid}: invalid category {r.get('category')!r}")
        if r.get("pricing") not in VALID_PRICING:
            errors.append(f"{rid}: invalid pricing {r.get('pricing')!r}")
        if r.get("status") not in VALID_STATUS:
            errors.append(f"{rid}: invalid status {r.get('status')!r}")
        if r.get("url") and not URL_RE.match(r["url"]):
            errors.append(f"{rid}: url does not start with http(s)://")
        if r.get("verified") and not DATE_RE.match(r["verified"]):
            errors.append(f"{rid}: verified must be YYYY-MM, got {r.get('verified')!r}")
        if not isinstance(r.get("tags", []), list):
            errors.append(f"{rid}: tags must be a list")
    return errors


def normalize(resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Ensure every record has every field with a stable shape."""
    out: list[dict[str, Any]] = []
    optional = {
        "subcategory": "",
        "year_founded": None,
        "notes": "",
        "tags": [],
    }
    for r in resources:
        norm = {**optional, **r}
        # Stable key order for serialization
        out.append({
            "id": norm["id"],
            "category": norm["category"],
            "subcategory": norm.get("subcategory", ""),
            "name": norm["name"],
            "type": norm["type"],
            "audience": norm["audience"],
            "description": norm["description"],
            "url": norm["url"],
            "pricing": norm["pricing"],
            "region": norm["region"],
            "language": norm["language"],
            "year_founded": norm.get("year_founded"),
            "status": norm["status"],
            "notes": norm.get("notes", ""),
            "tags": list(norm.get("tags", [])),
            "verified": norm["verified"],
        })
    return out


def write_json(records: list[dict[str, Any]]) -> Path:
    payload = {
        "metadata": {
            "name": "Swimming Resources Database",
            "version": "1.0.0",
            "license": "CC-BY-4.0",
            "homepage": "https://github.com/timothy22000/swimming-resources",
            "total": len(records),
            "categories": [
                {"id": cid, "label": CATEGORY_LABELS[cid],
                 "count": sum(1 for r in records if r["category"] == cid)}
                for cid in CATEGORY_IDS
            ],
        },
        "resources": records,
    }
    out = DATA_DIR / "swimming_resources.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def write_jsonl(records: list[dict[str, Any]]) -> Path:
    out = DATA_DIR / "swimming_resources.jsonl"
    with out.open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return out


def write_csv(records: list[dict[str, Any]]) -> Path:
    out = DATA_DIR / "swimming_resources.csv"
    fieldnames = list(records[0].keys()) if records else []
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            row = {**r, "tags": ";".join(r.get("tags") or [])}
            writer.writerow(row)
    return out


def write_parquet(records: list[dict[str, Any]]) -> Path | None:
    try:
        import pandas as pd
        import pyarrow  # noqa: F401  (ensures the engine is installed)
    except ImportError:
        print("warning: pandas/pyarrow not installed - skipping parquet output",
              file=sys.stderr)
        print("  install with: pip install pandas pyarrow", file=sys.stderr)
        return None
    out = DATA_DIR / "swimming_resources.parquet"
    df = pd.DataFrame(records)
    # pyarrow handles list[str] for tags natively
    df.to_parquet(out, engine="pyarrow", compression="snappy", index=False)
    return out


def main() -> int:
    errors = validate(ALL_RESOURCES)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    records = normalize(ALL_RESOURCES)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    json_path = write_json(records)
    jsonl_path = write_jsonl(records)
    csv_path = write_csv(records)
    parquet_path = write_parquet(records)

    print(f"Built {len(records)} resources across {len(CATEGORY_IDS)} categories.")
    print(f"  -> {json_path.relative_to(REPO_ROOT)}")
    print(f"  -> {jsonl_path.relative_to(REPO_ROOT)}")
    print(f"  -> {csv_path.relative_to(REPO_ROOT)}")
    if parquet_path:
        print(f"  -> {parquet_path.relative_to(REPO_ROOT)}")

    # Per-category breakdown
    print("\nPer-category counts:")
    for cid in CATEGORY_IDS:
        n = sum(1 for r in records if r["category"] == cid)
        print(f"  {cid:.<32} {n:>4}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
