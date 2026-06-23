# Guangzhou Human Evaluation Public Labels

This folder provides the public anonymized label file for the Guangzhou expert evaluation subset reported in the ECCV 2026 paper.

The file contains **5,268** valid human-labeled records: **2,605 gated** and **2,663 open** AOIs. Invalid or uncertain labels (`-1` or blank) from the internal annotation sheets are excluded.

## Public Fields

- `record_id`: stable anonymous record ID.
- `subset_id`: internal evaluation subset identifier.
- `centroid_lon`, `centroid_lat`: WGS84 centroid coordinates for georeferencing and reconstruction.
- `label_binary`: `1` for gated, `0` for open.
- `label`: `gated` or `open`.
- `annotation_scope`: Guangzhou expert evaluation subset.
- `public_fields_excluded`: fields intentionally excluded from the public release.

## Exclusions

This public file does not include community names, addresses, AOI polygons, raw imagery, imagery links, provider IDs, or provider-owned metadata. Exact reconstruction and audit materials are available only through the controlled-access DUA workflow:

https://github.com/MinweiZhao/GBA-GCs-Controlled-Access
