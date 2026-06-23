# GBA-GCs: Public Georeferenced Release

This repository contains the public, ethics-first release for the ECCV 2026 provisionally accepted paper:

**Urban Boundaries, Social Barriers: A Benchmark and Vision-Centric Framework for Mapping Gated Communities and Equity Implications** (Submission #11296).

This repository is a maintained release built from the ECCV paper dataset and further refined after acceptance. The **37,444-AOI** `data/paper_v1/` table is the stable paper version; for new use or citation, we recommend the latest expanded release because it contains the paper benchmark plus additional AOIs, while keeping the same data structure and processing workflow described in the paper.

<p align="center">
  <img src="assets/teaser_figure_eccv_2.png" alt="GBA-GCs teaser figure" width="95%">
</p>

The latest public release provides gated/open labels, centroid coordinates, area, and coarse non-identifying attributes for **46,747** mainland residential AOIs in China's Greater Bay Area. Hong Kong/Macao are provided as a separate **10,323** AOI transfer-diagnostic file. The release supports benchmark transparency and reconstruction while reducing risks from releasing precise residential boundaries, addresses, community names, raw map-provider metadata, or imagery.

## Access Tiers

This repository is the main public entry point for GBA-GCs. It hosts the unrestricted anonymized release, public documentation, reconstruction workflows, reference model API, and the public MCGC checkpoint.

Researchers who need the full controlled dataset should use the separate Controlled Access repository:

https://github.com/MinweiZhao/GBA-GCs-Controlled-Access

The controlled access path covers non-public components that are intentionally not redistributed here, including AOI boundaries, community names, provider identifiers when present, raw remote-sensing image chips, provider-derived metadata, raw Guangzhou annotation sheets and linkage fields, and Hong Kong/Macao controlled diagnostic components. To request access, review the access policy, fill in the request form, sign the non-commercial DUA, and submit the materials to `m.zhao@connect.hkust-gz.edu.cn`. Approved archives are distributed through controlled storage, not public GitHub.

The controlled repository also includes a small de-identified `data_sample/` preview with JSON metadata, local AOI geometry, and low-resolution remote-sensing thumbnails so requesters can understand the structure of the data available after approval.

## Overview

GBA-GCs is a public, boundary-free release built from the paper dataset and optimized for continued maintenance. Compared with the original ECCV paper benchmark, this repository may include expanded AOI coverage, improved documentation, model releases, and reconstruction utilities. It exposes enough spatial information for reproducible reconstruction and model auditing, while withholding raw AOI polygons, names, addresses, provider IDs, imagery, and provider-owned metadata.

<p align="center">
  <img src="assets/mcgc_pipeline.png" alt="MCGC dataset and model pipeline" width="95%">
</p>

## Files

- `data/paper_v1/gba_gcs_paper_v1_public_georeferenced.csv`: stable public paper-count table for the ECCV 2026 benchmark release (**37,444** mainland GBA AOIs).
- `data/paper_v1/manifest.json`: checksums and relationship between `paper_v1`, the maintained public table, and controlled access.
- `data/paper_v1/paper_v1_city_summary.csv`: city-level summary for the stable paper-count public table.
- `data/guangzhou_human_eval/guangzhou_human_eval_public_labels.csv`: public anonymized Guangzhou expert evaluation labels with WGS84 centroids (**5,268** AOIs: 2,605 gated / 2,663 open).
- `data/gba_gcs_mainland_public_georeferenced.csv`: georeferenced boundary-free labels and coarse attribute bins for the mainland GBA benchmark.
- `data/hk_macao_transfer_diagnostics_public_georeferenced.csv`: separate georeferenced Hong Kong and Macao transfer-diagnostic rows.
- `metadata/city_summary.csv`: city-level counts.
- `metadata/manifest.json`: source summaries, versioning, and public-release exclusions.
- `docs/DATASET_CARD.md`: dataset composition, intended use, limitations, and ethics notes.
- `docs/ETHICS_AND_ACCESS.md`: public vs controlled access policy.
- `docs/DATA_USE_AGREEMENT_TEMPLATE.md`: template for controlled non-commercial access requests.
- `docs/RECONSTRUCTION_WORKFLOWS.md`: Baidu/Amap and OSM/GEE reconstruction workflows.
- `model/`: reference MCGC inference API and model card.
- `model/CHECKPOINTS.md`: released checkpoint links, hashes, and use restrictions.
- `examples/`: minimal MCGC inference example.
- `code/README.md`: code and reconstruction notes.
- `assets/`: paper figures used for repository documentation.

## Projection And Source Notes

- Public coordinates are WGS84 longitude/latitude (`EPSG:4326`).
- `centroid_lon` and `centroid_lat` are AOI centroids, not AOI boundaries.
- `area_m2` is the AOI area in square meters from the projected/source AOI record.
- Mainland rows use provider-record WGS84 centroid fields when available.
- Hong Kong/Macao rows did not consistently include WGS84 centroid fields locally; their public centroids were computed from controlled projected AOI geometries and transformed from UTM Zone 50N (`EPSG:32650`) to WGS84.
- Controlled raw records may contain provider metadata such as community names, addresses, administrative fields, tags, provider IDs, AOI polygons, raster source names, and image metadata. These are not redistributed in this public repository.

## Public Schema

Each row is a georeferenced public record. The release includes centroid coordinates and area for reconstruction/matching. It does **not** include AOI polygons, names, addresses, provider identifiers, raw provider metadata, or imagery.

| Column | Description |
| --- | --- |
| `aoi_id` | Stable anonymous hash ID. |
| `city` | City-level location only. |
| `centroid_lon`, `centroid_lat` | WGS84 centroid coordinates for approximate spatial matching. |
| `area_m2` | AOI area in square meters, rounded to two decimals. |
| `label` | `gated` or `open`, generated by the validated MCGC model for the metropolitan-scale inference set. |
| `prediction_probability_gated` | Model probability rounded to four decimals. |
| `confidence_bin` | Coarse confidence category. |
| `area_bin`, `far_bin`, `poi_density_bin`, `poi_count_bin` | Coarse derived bins only. |
| `has_boundary_in_controlled_release`, `has_imagery_in_controlled_release` | Indicates whether the non-public controlled package contains restricted components. |

## Counts

Paper-count stable public table: **37,444** mainland AOIs (`data/paper_v1/`).

Maintained mainland public table: **46,747** mainland AOIs.

Hong Kong/Macao transfer-diagnostic AOIs: **10,323**.

Guangzhou expert evaluation labels: **5,268** public anonymized georeferenced records (**2,605 gated** / **2,663 open**). Raw annotation sheets and linkage fields remain controlled.

## Citation

If you use this release, cite the ECCV 2026 paper above. A BibTeX entry will be added after the official proceedings metadata is available.

## License And Access

This public georeferenced release is provided for non-commercial research and reproducibility. Controlled components, including AOI boundaries, names, raw imagery, provider metadata, raw annotation sheets, and linkage fields, are not redistributed in this public repository.

For access to controlled components, use the Controlled Access repository:

- Request portal: https://github.com/MinweiZhao/GBA-GCs-Controlled-Access
- Access policy: https://github.com/MinweiZhao/GBA-GCs-Controlled-Access/blob/main/docs/ACCESS_POLICY.md
- Request form: https://github.com/MinweiZhao/GBA-GCs-Controlled-Access/blob/main/forms/ACCESS_REQUEST_FORM.md
- DUA template: https://github.com/MinweiZhao/GBA-GCs-Controlled-Access/blob/main/docs/DUA_TEMPLATE.md
- Manifest and checksums: https://github.com/MinweiZhao/GBA-GCs-Controlled-Access/tree/main/metadata
- Controlled data samples: https://github.com/MinweiZhao/GBA-GCs-Controlled-Access/tree/main/data_sample
- Contact: `m.zhao@connect.hkust-gz.edu.cn`

## MCGC Reference Model

The `model/` folder contains a reference MCGC inference API. Remote-sensing imagery is required at inference time. Text and numerical features are optional and may be omitted through modality masks.

### Download Checkpoint

The ECCV 2026 MCGC checkpoint has been uploaded to GitHub Releases. The checkpoint is not committed into the repository because it is a large binary model file.

- Release: https://github.com/MinweiZhao/GBA-GCs/releases/tag/v2026-06-mcgc
- Direct download: https://github.com/MinweiZhao/GBA-GCs/releases/download/v2026-06-mcgc/trimodal_io_fused_gba_full.pth
- Asset: `trimodal_io_fused_gba_full.pth`
- Size: 1,716,771,558 bytes
- SHA-256: `48518dafd9b2e2702db812ae9977bc6699bbc2e55c4a8044bd7d993114ebb1b8`

Download and verify:

```bash
curl -L -o trimodal_io_fused_gba_full.pth \
  https://github.com/MinweiZhao/GBA-GCs/releases/download/v2026-06-mcgc/trimodal_io_fused_gba_full.pth

sha256sum trimodal_io_fused_gba_full.pth
```

See `model/CHECKPOINTS.md` and `model/MODEL_CARD.md` before use.

<p align="center">
  <img src="assets/ccf_block.png" alt="MCGC cross-modal fusion block" width="70%">
</p>

MCGC inputs:

- required: remote-sensing image tile, typically cropped around the reconstructed AOI with context buffer
- optional: text metadata embedding, e.g. name/tag/address descriptions when licensed and available
- optional: numerical/structured features, e.g. area, FAR, POI density, POI count
- optional masks: `has_text`, `has_numerical`; visual imagery cannot be missing

The paper model uses a DINOv3-SAT visual backbone with LoRA adaptation, an optional text encoder, structured-feature MLP, inner/outer visual context, and cross-modal community-aware fusion. The lightweight implementation in `model/mcgc_reference.py` is an API-compatible reference for downstream callers.

Use of the checkpoint is limited to non-commercial research, reproducibility, benchmarking, and aggregate urban-science analysis. It is not intended for surveillance, policing, geofencing, commercial real-estate scoring, resident-level profiling, targeted enforcement, or per-compound public lookup systems.

Minimal call:

```bash
PYTHONPATH=. python examples/run_mcgc_inference.py \
  --image_tensor example_image_tensor.pt \
  --output prediction.json
```
