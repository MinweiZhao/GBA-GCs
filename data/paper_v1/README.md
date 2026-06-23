# GBA-GCs Paper V1 Public Release

This folder contains the stable public, boundary-free table for the ECCV 2026 paper version of GBA-GCs.

## Relationship To The Paper

The ECCV camera-ready paper reports a mainland GBA benchmark of **37,444** residential AOIs. This folder provides a stable public GitHub table with the same benchmark count for citation, indexing, and reproducible public access.

The public table contains only non-sensitive fields: anonymous AOI ID, city, WGS84 centroid, AOI area, gated/open label, rounded model probability, confidence bin, and coarse derived feature bins. It does not contain AOI polygons, community names, addresses, provider identifiers, raw image chips, or provider-owned metadata.

Exact controlled benchmark components, including AOI geometries, raw imagery, provider metadata, and Guangzhou human-labeled files, are distributed only through the controlled-access DUA process:

https://github.com/MinweiZhao/GBA-GCs-Controlled-Access

## Files

- `gba_gcs_paper_v1_public_georeferenced.csv`: 37,444-row public table.
- `paper_v1_city_summary.csv`: city-level count summary.
- `manifest.json`: version notes, selection rule, public exclusions, and SHA-256 checksums.

## Checksum

`gba_gcs_paper_v1_public_georeferenced.csv`

SHA-256: `240409f037930fabc37da1498d930304acdaa02e53df40e7c7dd7cebf5aa43c0`

## Maintained Extensions

The repository root also includes a maintained expanded mainland table and a separate Hong Kong/Macao diagnostic file. Those files are useful for ongoing community use and reconstruction testing, but they should not be treated as the fixed experimental table reported in the ECCV paper.
