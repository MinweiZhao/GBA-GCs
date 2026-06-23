#!/usr/bin/env python3
"""Validate the public georeferenced GBA-GCs release files."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILES = [
    ROOT / "data" / "gba_gcs_mainland_public_georeferenced.csv",
    ROOT / "data" / "hk_macao_transfer_diagnostics_public_georeferenced.csv",
    ROOT / "data" / "paper_v1" / "gba_gcs_paper_v1_public_georeferenced.csv",
]
GUANGZHOU_EVAL_FILE = (
    ROOT
    / "data"
    / "guangzhou_human_eval"
    / "guangzhou_human_eval_public_labels.csv"
)
GUANGZHOU_SPLIT_DIR = ROOT / "data" / "guangzhou_human_eval" / "splits"
REQUIRED_COLUMNS = {
    "aoi_id",
    "city",
    "centroid_lon",
    "centroid_lat",
    "area_m2",
    "label",
    "label_source",
    "prediction_probability_gated",
    "confidence_bin",
    "area_bin",
    "far_bin",
    "poi_density_bin",
    "poi_count_bin",
    "has_boundary_in_controlled_release",
    "has_imagery_in_controlled_release",
}
SENSITIVE_PATTERN = re.compile(
    r"address|uid|osm_id|original_geometry|POLYGON|\\.png|\\.tif|\\.shp",
    re.IGNORECASE,
)


def validate_csv(path: Path) -> int:
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    if SENSITIVE_PATTERN.search(text):
        raise ValueError(f"sensitive-looking token found in {path}")
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} missing columns: {sorted(missing)}")
        rows = list(reader)
    bad_labels = sorted({row["label"] for row in rows}.difference({"gated", "open"}))
    if bad_labels:
        raise ValueError(f"{path} has unexpected labels: {bad_labels}")
    missing_geo = [
        row["aoi_id"]
        for row in rows
        if not row["centroid_lon"] or not row["centroid_lat"] or not row["area_m2"]
    ]
    if missing_geo:
        raise ValueError(f"{path} has {len(missing_geo)} rows missing centroid/area")
    return len(rows)


def main() -> None:
    counts = {path.name: validate_csv(path) for path in DATA_FILES}
    manifest = json.loads((ROOT / "metadata" / "manifest.json").read_text(encoding="utf-8"))
    paper_manifest = json.loads(
        (ROOT / "data" / "paper_v1" / "manifest.json").read_text(encoding="utf-8")
    )
    expected = {
        "gba_gcs_mainland_public_georeferenced.csv": manifest["mainland_benchmark_aoi"],
        "hk_macao_transfer_diagnostics_public_georeferenced.csv": manifest["hk_macao_transfer_diagnostic_aoi"],
        "gba_gcs_paper_v1_public_georeferenced.csv": paper_manifest["rows"],
    }
    if counts != expected:
        raise ValueError(f"count mismatch: observed={counts}, expected={expected}")

    with GUANGZHOU_EVAL_FILE.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    gz_record_ids = {row["record_id"] for row in rows}
    gz_counts = {}
    for row in rows:
        gz_counts[row["label"]] = gz_counts.get(row["label"], 0) + 1
        if not row["centroid_lon"] or not row["centroid_lat"]:
            raise ValueError(f"{GUANGZHOU_EVAL_FILE} has rows missing georeference")
    expected_gz = manifest["guangzhou_human_eval_public_labels"]
    if len(rows) != expected_gz["rows"] or gz_counts != expected_gz["label_counts"]:
        raise ValueError(
            "Guangzhou label mismatch: "
            f"observed={{'rows': {len(rows)}, 'label_counts': {gz_counts}}}, "
            f"expected={expected_gz}"
        )

    split_counts = {}
    for split_idx in range(1, 6):
        split_path = GUANGZHOU_SPLIT_DIR / f"guangzhou_split_{split_idx}.json"
        split = json.loads(split_path.read_text(encoding="utf-8"))
        parts = {
            name: set(split["record_id_lists"][name])
            for name in ("train", "validation", "test")
        }
        if parts["train"] & parts["validation"]:
            raise ValueError(f"{split_path} has train/validation overlap")
        if parts["train"] & parts["test"]:
            raise ValueError(f"{split_path} has train/test overlap")
        if parts["validation"] & parts["test"]:
            raise ValueError(f"{split_path} has validation/test overlap")
        observed_ids = parts["train"] | parts["validation"] | parts["test"]
        if observed_ids != gz_record_ids:
            raise ValueError(
                f"{split_path} does not exactly cover Guangzhou public record IDs"
            )
        split_counts[f"guangzhou_split_{split_idx}.json"] = {
            name: len(ids) for name, ids in parts.items()
        }

    print(
        json.dumps(
            {
                "status": "pass",
                "counts": counts,
                "guangzhou_human_eval": {
                    "rows": len(rows),
                    "label_counts": gz_counts,
                    "official_splits": split_counts,
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
