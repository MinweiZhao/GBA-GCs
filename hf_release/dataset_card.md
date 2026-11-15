---
pretty_name: GBA-GCs Public Georeferenced Release
license: other
license_name: gba-gcs-public-non-commercial-research
license_link: LICENSE-DATA.txt
task_categories:
  - tabular-classification
tags:
  - arxiv:2609.03804
  - remote-sensing
  - geospatial
  - urban-science
  - gated-communities
  - multimodal
  - benchmark
__CONFIGS__
---

# GBA-GCs: Public Georeferenced Release

Public companion to **Urban Boundaries, Social Barriers: A Benchmark and Vision-Centric Framework for Mapping Gated Communities and Equity Implications** ([arXiv:2609.03804](https://arxiv.org/abs/2609.03804)).

- [Code and release documentation](https://github.com/MinweiZhao/GBA-GCs)
- [MCGC checkpoint](https://huggingface.co/__HF_NAMESPACE__/MCGC)
- [Controlled-access request portal](https://github.com/MinweiZhao/GBA-GCs-Controlled-Access)
- Source revision: `5db26237a66146b1f521033f894120b1082da423`

This Hub repository mirrors the existing public, boundary-free release. Coordinates are WGS84 AOI centroids (`EPSG:4326`). They are approximate locations of residential areas, so these records should not be described as fully anonymous. The existing non-commercial research license and restrictions apply.

## Load the data

```python
from datasets import load_dataset

# Default: maintained mainland table, 46,747 model-predicted records.
dataset = load_dataset("__HF_NAMESPACE__/GBA-GCs")
print(dataset["data"][0])

# Paper-count stable public subset.
paper = load_dataset("__HF_NAMESPACE__/GBA-GCs", "paper_v1", split="data")

# One of five official expert-labeled Guangzhou benchmark splits.
benchmark = load_dataset("__HF_NAMESPACE__/GBA-GCs", "guangzhou_split_1")
train = benchmark["train"]
validation = benchmark["validation"]
test = benchmark["test"]
```

CSV files and explicit configuration metadata support standard `load_dataset` access and the Hub Dataset Viewer without a custom loading script. Viewer processing happens on the Hub after upload.

The four complete-table configurations use the split name `data`; this name does not imply a training/test partition. The five official Guangzhou configurations use `train`, `validation`, and `test`.

## Configurations and overlap

| Configuration | Rows | Meaning |
| --- | ---: | --- |
| `mainland` (default) | 46,747 | Maintained mainland GBA table; MCGC predictions. |
| `paper_v1` | 37,444 | Stable paper-count public subset of `mainland`. |
| `hk_macao` | 10,323 | Hong Kong/Macao transfer diagnostics; MCGC predictions. |
| `guangzhou_labels` | 5,268 | Public Guangzhou expert labels: 2,605 gated, 2,663 open. |
| `guangzhou_split_1` through `guangzhou_split_5` | 5,268 each | The same expert records, partitioned into 3,806 train / 412 validation / 1,050 test rows per official split. |

These counts must **not** be added as independent examples. In particular, `paper_v1` overlaps `mainland`, and all five Guangzhou split configurations reuse the same 5,268 expert records. The source manifest describes `paper_v1` as a deterministic, city-proportional stable subset of the maintained table, selected using `SHA-256(aoi_id|paper_v1)`. Matching the paper's count does not establish that every public row is identical to the original controlled benchmark.

Metropolitan predictions are not human ground truth. Hong Kong/Macao records (10,186 / 137) are transfer diagnostics, not a universal gated-community benchmark. Official Guangzhou partitions are materialized directly from the released record-ID lists, retaining their membership and order. They do not provide the controlled imagery required for model training.

## Fields

| Field | Description |
| --- | --- |
| `aoi_id` | Stable public hash identifier in prediction tables. |
| `city` | City name in prediction tables. |
| `centroid_lon`, `centroid_lat` | WGS84 centroid, not the AOI boundary. |
| `area_m2` | AOI area in square meters, rounded to two decimals. |
| `label` | `gated` or `open`, under the paper's Chinese residential-enclosure definition. |
| `label_source` | Prediction provenance in metropolitan tables. |
| `prediction_probability_gated` | Model probability rounded to four decimals. |
| `confidence_bin` | Coarse prediction confidence category. |
| `area_bin`, `far_bin`, `poi_density_bin`, `poi_count_bin` | Coarse derived attributes. |
| `has_boundary_in_controlled_release`, `has_imagery_in_controlled_release` | Availability in the separate controlled package, not access through this repository. |
| `record_id`, `subset_id` | Public identifiers in Guangzhou expert tables. |
| `label_binary` | Guangzhou expert label: 0 = open, 1 = gated. |
| `annotation_scope`, `public_fields_excluded` | Scope and exclusions recorded in the expert-label release. |

Prediction and expert-label configurations have different schemas. Missing numerical values remain missing; coarse bins are not replacements for original continuous measurements.

## Source, access, and limitations

See [the upstream dataset card](docs/DATASET_CARD.md), [ethics and access policy](docs/ETHICS_AND_ACCESS.md), and [reconstruction documentation](docs/RECONSTRUCTION_WORKFLOWS.md). This mirror preserves source files, manifests, and SHA-256 checksums. `release_metadata.json` records the pinned source revision and configuration counts.

Community names, addresses, provider IDs, AOI polygons, raw image chips, raw provider metadata, original annotation sheets, and private linkage fields are excluded. Those components remain available only through the upstream controlled-access process and applicable source terms. Public centroids do not grant redistribution rights to external map data or imagery.

Intended uses include non-commercial reproducibility, benchmark bookkeeping, model auditing, and aggregate urban-science and equity research. Labels reflect a locally grounded operational definition and should not be treated as universal social categories. Do not use this release for residential targeting, surveillance, policing, commercial real-estate profiling, or re-identification. Consult [LICENSE-DATA.txt](LICENSE-DATA.txt) for the exact existing terms.

## Citation

Please cite **Urban Boundaries, Social Barriers: A Benchmark and Vision-Centric Framework for Mapping Gated Communities and Equity Implications**, arXiv:2609.03804 (2026), and identify the configuration and source revision used. Official proceedings metadata should be taken from the upstream repository when available.
