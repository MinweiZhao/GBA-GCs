# Maintenance Plan

GBA-GCs is released as a maintained research dataset rather than a one-off dump. Updates will follow explicit versioning so paper results remain reproducible.

## Versioning

- `2026-06-camera-ready-anonymized`: ECCV 2026 camera-ready public anonymized release.
- Future versions should use `YYYY-MM-description`.
- Every version must keep a manifest with row counts, schema changes, and release exclusions.

## Update Policy

Future updates may include:

- additional anonymized AOI rows
- corrected labels after documented human verification
- new aggregate or binned non-sensitive attributes
- improved split files
- model checkpoints and inference links
- reconstruction utilities for licensed and fully open pipelines

Updates must not include unrestricted names, addresses, coordinates, raw polygons, image chips, provider IDs, or raw provider metadata.

## Change Log Requirements

Each release should document:

- added or removed rows
- changed labels
- schema changes
- changes to ethics/access policy
- checksum changes for distributed files
- compatibility with the MCGC model release

