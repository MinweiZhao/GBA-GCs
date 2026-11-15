#!/usr/bin/env python3
"""Prepare, verify, and publish only the existing public GBA-GCs artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import tempfile
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parent
DEFAULT_OUTPUT = DEFAULT_ROOT / ".hf-release"
SOURCE_REVISION = "5db26237a66146b1f521033f894120b1082da423"
CHECKPOINT = "trimodal_io_fused_gba_full.pth"
CHECKPOINT_SIZE = 1716771558
CHECKPOINT_HASH = "48518dafd9b2e2702db812ae9977bc6699bbc2e55c4a8044bd7d993114ebb1b8"
CHECKPOINT_URL = (
    "https://github.com/MinweiZhao/GBA-GCs/releases/download/"
    "v2026-06-mcgc/" + CHECKPOINT
)
BASE_TABLES = {
    "mainland": ("data/gba_gcs_mainland_public_georeferenced.csv", 46747),
    "paper_v1": ("data/paper_v1/gba_gcs_paper_v1_public_georeferenced.csv", 37444),
    "hk_macao": ("data/hk_macao_transfer_diagnostics_public_georeferenced.csv", 10323),
    "guangzhou_labels": (
        "data/guangzhou_human_eval/guangzhou_human_eval_public_labels.csv", 5268
    ),
}
PART_COUNTS = {"train": 3806, "validation": 412, "test": 1050}


def digest(path):
    sha = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_rows(path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def validate_rows(rows, expected, id_field):
    if len(rows) != expected or len({row[id_field] for row in rows}) != expected:
        raise ValueError(f"Expected {expected} unique {id_field} records.")
    for row in rows:
        if row["label"] not in {"gated", "open"}:
            raise ValueError("Unexpected label.")
        lon, lat = float(row["centroid_lon"]), float(row["centroid_lat"])
        if not math.isfinite(lon) or not math.isfinite(lat) or not (-180 <= lon <= 180 and -90 <= lat <= 90):
            raise ValueError("Invalid WGS84 centroid.")


def validate_split(split, records):
    parts = split["record_id_lists"]
    seen = set()
    for part, expected in PART_COUNTS.items():
        ids = parts[part]
        if len(ids) != expected or len(set(ids)) != len(ids):
            raise ValueError(f"Invalid count or duplicate IDs in {part}.")
        if seen.intersection(ids) or not set(ids).issubset(records):
            raise ValueError("Official split has overlapping or unknown IDs.")
        seen.update(ids)
    if seen != set(records):
        raise ValueError("Official split does not exactly cover expert records.")
    return parts


def source_inventory(root):
    manifest = read_json(HERE / "source_manifest.json")
    for relative, expected in manifest["files"].items():
        path = root / relative
        if path.is_symlink() or not path.is_file() or digest(path) != expected:
            raise ValueError(f"Source differs from pinned public release: {relative}")
    return manifest


def render(name, namespace):
    return (HERE / name).read_text(encoding="utf-8").replace("__HF_NAMESPACE__", namespace)


def yaml_configs(configs):
    lines = ["configs:"]
    for name, parts in configs.items():
        lines.append(f"  - config_name: {name}")
        if name == "mainland":
            lines.append("    default: true")
        lines.append("    data_files:")
        for part, info in parts.items():
            lines += [f"      - split: {part}", f"        path: {info['path']}"]
    return "\n".join(lines)


def prepare(root, output, namespace):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", namespace):
        raise ValueError("Supply a Hugging Face username or organization, without slashes.")
    if output.exists():
        raise ValueError(f"Output already exists: {output}. Verify/publish it, or choose a new --output.")
    inventory = source_inventory(root)
    tables = {}
    for name, (relative, count) in BASE_TABLES.items():
        fields, rows = read_rows(root / relative)
        validate_rows(rows, count, "record_id" if name == "guangzhou_labels" else "aoi_id")
        tables[name] = (fields, rows)
    mainland_ids = {row["aoi_id"] for row in tables["mainland"][1]}
    if not {row["aoi_id"] for row in tables["paper_v1"][1]}.issubset(mainland_ids):
        raise ValueError("Paper-count public records are not a subset of mainland records.")
    fields, expert_rows = tables["guangzhou_labels"]
    records = {row["record_id"]: row for row in expert_rows}
    if sum(row["label"] == "gated" for row in expert_rows) != 2605:
        raise ValueError("Expert class counts differ from the release.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="hf-prepare-", dir=output.parent) as temp:
        staging = Path(temp) / "release"
        dataset, model = staging / "dataset", staging / "model"
        dataset.mkdir(parents=True)
        (model / "upstream").mkdir(parents=True)
        # A fixed, hash-checked source inventory is the entire source upload boundary.
        for relative in inventory["files"]:
            target_root = model / "upstream" if relative.startswith("model/") else dataset
            target = target_root / (Path(relative).name if relative.startswith("model/") else relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / relative, target)
        configs = {name: {"data": {"path": relative, "rows": count}}
                   for name, (relative, count) in BASE_TABLES.items()}
        for index in range(1, 6):
            name = f"guangzhou_split_{index}"
            relative = f"data/guangzhou_human_eval/splits/{name}.json"
            parts = validate_split(read_json(root / relative), records)
            configs[name] = {}
            for part, ids in parts.items():
                if part not in PART_COUNTS:
                    raise ValueError(f"Unexpected partition: {part}")
                path = f"hf_data/{name}/{part}.csv"
                target = dataset / path
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(records[record_id] for record_id in ids)
                configs[name][part] = {"path": path, "rows": len(ids)}
        card = render("dataset_card.md", namespace).replace("__CONFIGS__", yaml_configs(configs))
        (dataset / "README.md").write_text(card, encoding="utf-8")
        (model / "README.md").write_text(render("model_card.md", namespace), encoding="utf-8")
        (model / "download_checkpoint.py").write_text(render("download_checkpoint.py", namespace), encoding="utf-8")
        restrictions = (root / "model/CHECKPOINTS.md").read_text(encoding="utf-8").split("## Use Restrictions\n", 1)[1]
        (model / "USE_RESTRICTIONS.md").write_text(
            "# Existing MCGC checkpoint use restrictions\n\n" + restrictions.strip() +
            "\n\nSource: https://github.com/MinweiZhao/GBA-GCs/blob/" + SOURCE_REVISION +
            "/model/CHECKPOINTS.md#use-restrictions\n", encoding="utf-8")
        metadata = {"source_repository": "MinweiZhao/GBA-GCs", "source_revision": SOURCE_REVISION,
                    "dataset_repo": f"{namespace}/GBA-GCs", "model_repo": f"{namespace}/MCGC",
                    "configs": configs}
        write_json(dataset / "release_metadata.json", metadata)
        write_json(dataset / "source_manifest.json", inventory)
        write_json(model / "checkpoint_manifest.json", {"filename": CHECKPOINT, "size": CHECKPOINT_SIZE,
                   "sha256": CHECKPOINT_HASH, "source_url": CHECKPOINT_URL})
        files = {}
        for kind in ("dataset", "model"):
            files[kind] = {path.relative_to(staging / kind).as_posix():
                           {"bytes": path.stat().st_size, "sha256": digest(path)}
                           for path in sorted((staging / kind).rglob("*")) if path.is_file()}
        write_json(staging / "release_manifest.json", {**metadata, "files": files})
        staging.rename(output)
    verify(output)
    print(f"Prepared {output}; nothing has been uploaded.")


def verify_checkpoint(path):
    if path.is_symlink() or path.stat().st_size != CHECKPOINT_SIZE or digest(path) != CHECKPOINT_HASH:
        raise ValueError("Checkpoint size/SHA-256 differs from the original GitHub Release.")


def verify(output):
    manifest = read_json(output / "release_manifest.json")
    for kind in ("dataset", "model"):
        folder = output / kind
        expected = set(manifest["files"][kind])
        present = {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file() or p.is_symlink()}
        checkpoint_present = kind == "model" and CHECKPOINT in present
        if checkpoint_present:
            present.remove(CHECKPOINT)
            verify_checkpoint(folder / CHECKPOINT)
        if present != expected:
            raise ValueError(f"Unexpected or missing files in {kind}: {present ^ expected}")
        for relative, info in manifest["files"][kind].items():
            path = folder / relative
            if path.is_symlink() or path.stat().st_size != info["bytes"] or digest(path) != info["sha256"]:
                raise ValueError(f"Prepared file changed: {kind}/{relative}")
        if "__HF_NAMESPACE__" in (folder / "README.md").read_text(encoding="utf-8"):
            raise ValueError("Unresolved HF namespace in card.")
    for parts in manifest["configs"].values():
        if any(part.lower() == "all" for part in parts):
            raise ValueError("'all' is reserved by datasets; use a concrete split name.")
        for info in parts.values():
            if len(read_rows(output / "dataset" / info["path"])[1]) != info["rows"]:
                raise ValueError("Prepared CSV row count mismatch.")
    print("Verified 9 dataset configurations, source checksums, and upload file boundary.")
    return manifest


def verify_loader(output, manifest):
    from datasets import load_dataset

    for name, parts in manifest["configs"].items():
        loaded = load_dataset(str((output / "dataset").resolve()), name)
        if set(loaded) != set(parts):
            raise ValueError(f"Local loader split names differ for {name}.")
        for part, info in parts.items():
            if len(loaded[part]) != info["rows"]:
                raise ValueError(f"Local loader row count differs for {name}/{part}.")
    print("Loaded all 9 configurations locally with datasets.")


def add_checkpoint(output, local_path, download):
    target = output / "model" / CHECKPOINT
    if target.exists():
        verify_checkpoint(target)
        return
    if local_path:
        verify_checkpoint(local_path)
        shutil.copyfile(local_path, target)
    elif download:
        partial = output / (CHECKPOINT + ".part")
        print("Downloading the original 1.72 GB MCGC artifact...", flush=True)
        request = Request(CHECKPOINT_URL, headers={"User-Agent": "GBA-GCs-HF-release"})
        with urlopen(request, timeout=120) as source, partial.open("wb") as handle:
            shutil.copyfileobj(source, handle, length=8 * 1024 * 1024)
        verify_checkpoint(partial)
        partial.rename(target)
    else:
        raise ValueError("Supply --checkpoint PATH or --download-checkpoint before publishing.")
    verify_checkpoint(target)


def publish(output, local_checkpoint, download):
    manifest = verify(output)
    from huggingface_hub import HfApi
    from huggingface_hub.errors import RepositoryNotFoundError
    from datasets import load_dataset

    api = HfApi()
    api.whoami()  # Fail before a large download if local authentication is missing.
    verify_loader(output, manifest)
    for key, kind in (("dataset_repo", "dataset"), ("model_repo", "model")):
        try:
            info = api.repo_info(repo_id=manifest[key], repo_type=kind)
        except RepositoryNotFoundError:
            continue
        if info.private:
            raise ValueError(f"{manifest[key]} already exists privately; visibility will not be changed.")
    add_checkpoint(output, local_checkpoint, download)
    verify(output)
    for key, kind in (("dataset_repo", "dataset"), ("model_repo", "model")):
        repo_id = manifest[key]
        api.create_repo(repo_id=repo_id, repo_type=kind, private=False, exist_ok=True)
        allowed = list(manifest["files"][kind]) + ([CHECKPOINT] if kind == "model" else [])
        api.upload_folder(repo_id=repo_id, repo_type=kind, folder_path=output / kind,
                          allow_patterns=allowed, commit_message="Publish GBA-GCs public research artifacts")
    # Load every named configuration from HF, not from the local staging directory.
    for name, parts in manifest["configs"].items():
        loaded = load_dataset(manifest["dataset_repo"], name)
        if set(loaded) != set(parts):
            raise ValueError(f"Remote split names differ for {name}.")
        for part, info in parts.items():
            local_rows = read_rows(output / "dataset" / info["path"])[1]
            remote = loaded[part]
            if len(remote) != info["rows"]:
                raise ValueError(f"Remote row count differs for {name}/{part}.")
            # Compare every field, accounting only for CSV type inference.
            for original, fetched in zip(local_rows, remote):
                if set(original) != set(fetched):
                    raise ValueError(f"Remote schema differs for {name}/{part}.")
                for column, value in original.items():
                    actual = fetched[column]
                    if value == "" and (actual is None or isinstance(actual, float) and math.isnan(actual)):
                        continue
                    if isinstance(actual, (int, float)) and not isinstance(actual, bool):
                        same = math.isclose(float(value), actual, rel_tol=1e-12, abs_tol=1e-12)
                    else:
                        same = value == str(actual)
                    if not same:
                        raise ValueError(f"Remote cell differs for {name}/{part}/{column}.")
    info = api.model_info(manifest["model_repo"], files_metadata=True)
    artifact = next((sibling for sibling in info.siblings if sibling.rfilename == CHECKPOINT), None)
    if artifact is None or artifact.size != CHECKPOINT_SIZE:
        raise ValueError("Remote model artifact missing or wrong size.")
    remote_hash = getattr(artifact.lfs, "sha256", None) if artifact.lfs else None
    if remote_hash and remote_hash != CHECKPOINT_HASH:
        raise ValueError("Remote checkpoint checksum differs.")
    print("Uploaded and loaded all 9 dataset configurations successfully.")
    print("Checkpoint remote size verified; " + ("remote SHA-256 verified." if remote_hash else "remote SHA-256 unavailable; local SHA-256 verified."))
    print("https://huggingface.co/datasets/" + manifest["dataset_repo"])
    print("https://huggingface.co/" + manifest["model_repo"])
    print("Open the dataset page to check Dataset Viewer processing; submit/claim the paper separately.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare", help="Build reviewable local folders; no upload.")
    prep.add_argument("--namespace", required=True)
    prep.add_argument("--source-root", type=Path, default=DEFAULT_ROOT)
    prep.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    for name in ("verify", "publish"):
        sub = commands.add_parser(name)
        sub.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
        if name == "verify":
            sub.add_argument("--load", action="store_true", help="Also load all configs using datasets.")
        if name == "publish":
            group = sub.add_mutually_exclusive_group()
            group.add_argument("--checkpoint", type=Path)
            group.add_argument("--download-checkpoint", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            prepare(args.source_root.resolve(), args.output.resolve(), args.namespace)
        elif args.command == "verify":
            manifest = verify(args.output.resolve())
            if args.load:
                verify_loader(args.output.resolve(), manifest)
        else:
            publish(args.output.resolve(), args.checkpoint, args.download_checkpoint)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
