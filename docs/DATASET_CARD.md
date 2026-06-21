# Dataset Card

## Dataset

GBA-GCs public georeferenced release, version `2026-06-camera-ready-georeferenced`.

## Motivation

The dataset supports reproducible research on recognizing Chinese `fengbi xiaoqu` / gated residential compounds and studying aggregate spatial equity patterns without exposing precise residential boundaries or direct identifiers in the public release. Centroid coordinates and area are provided to support reconstruction with licensed map APIs or open OSM/GEE workflows.

## Composition

- Mainland benchmark rows: 46,747
- Separate Hong Kong/Macao transfer-diagnostic rows: 10,323
- Total public rows across both CSV files: 57,070
- Hong Kong diagnostic rows: 10,186
- Macao diagnostic rows: 137
- Public fields: stable row ID, city, WGS84 centroid, area, predicted gated/open label, rounded probability, confidence bin, and coarse attribute bins.

## Not Publicly Released

The public repository excludes community names, addresses, provider UIDs/OSM IDs, AOI polygons, image chips, and raw map-provider metadata. These fields are sensitive for residential privacy and may also be constrained by third-party data terms.

## Georeferencing Notice

This release is not a strict anonymous table because it includes centroid coordinates and area. These fields are included to support transparent reconstruction with licensed Baidu/Amap APIs or fully open OSM/GEE workflows without depending on fragile provider IDs. Users must not attempt to infer or publish community names, addresses, exact boundaries, or provider identifiers from these fields.

## Label Meaning

`gated` and `open` refer to the paper's operationalization of residential enclosure in the Chinese `fengbi xiaoqu` context. Hong Kong and Macao rows are best treated as transfer diagnostics rather than evidence of a universal gated-community category.

## Intended Uses

- Reproducing aggregate counts and label distributions.
- Benchmark bookkeeping and split construction.
- Auditing model outputs at public row level.
- Non-commercial urban analytics and fairness research at aggregate scales.

## Out-Of-Scope Uses

- Re-identifying residential communities.
- Targeting, ranking, or profiling individual compounds or residents.
- Operational surveillance, policing, real-estate targeting, or commercial decision-making.
- Treating labels as universal ground truth outside the paper's operational scope.
