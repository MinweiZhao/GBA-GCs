# Dataset Card

## Dataset

GBA-GCs public anonymized release, version `2026-06-camera-ready-anonymized`.

## Motivation

The dataset supports reproducible research on recognizing Chinese `fengbi xiaoqu` / gated residential compounds and studying aggregate spatial equity patterns without exposing precise residential boundaries or direct identifiers in the public release.

## Composition

- Mainland benchmark rows: 46,747
- Separate Hong Kong/Macao transfer-diagnostic rows: 10,323
- Total public rows across both CSV files: 57,070
- Hong Kong diagnostic rows: 10,186
- Macao diagnostic rows: 137
- Public fields: anonymous AOI ID, city, predicted gated/open label, rounded probability, confidence bin, and coarse attribute bins.

## Not Publicly Released

The public repository excludes community names, addresses, provider UIDs, coordinates, AOI polygons, image chips, and raw map-provider metadata. These fields are sensitive for residential privacy and may also be constrained by third-party data terms.

## Label Meaning

`gated` and `open` refer to the paper's operationalization of residential enclosure in the Chinese `fengbi xiaoqu` context. Hong Kong and Macao rows are best treated as transfer diagnostics rather than evidence of a universal gated-community category.

## Intended Uses

- Reproducing aggregate counts and label distributions.
- Benchmark bookkeeping and split construction.
- Auditing model outputs at anonymized AOI level.
- Non-commercial urban analytics and fairness research at aggregate scales.

## Out-Of-Scope Uses

- Re-identifying residential communities.
- Targeting, ranking, or profiling individual compounds or residents.
- Operational surveillance, policing, real-estate targeting, or commercial decision-making.
- Treating labels as universal ground truth outside the paper's operational scope.
