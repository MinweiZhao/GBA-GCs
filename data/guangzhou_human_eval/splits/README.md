# Guangzhou Official Benchmark Splits

This folder contains the five fixed Guangzhou evaluation splits referenced in Supplementary Sec. D.4 of the ECCV 2026 camera-ready paper.

Each `guangzhou_split_k.json` file contains anonymous `record_id` lists for `train`, `validation`, and `test`. The source records are the public labels in `../guangzhou_human_eval_public_labels.csv`.

Split construction follows the paper protocol:

- 8:2 train/test split for each of five fixed seeds.
- 10% validation sampled from the training pool for early stopping and model selection.
- Joint stratification over AOI area bin, geographic cluster, and gated/open label.
- `seed=42` is the global training seed used with the fixed split indices.

The area bins were computed from controlled AOI `area_m2` during release preparation, but raw controlled AOI metadata is not redistributed here. The published split files contain only anonymous public record IDs and non-sensitive split metadata.

Use these files when reproducing the controlled Guangzhou benchmark results reported in the paper.
