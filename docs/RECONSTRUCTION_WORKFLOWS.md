# Reconstruction Workflows

This document describes two ways to reconstruct benchmark-compatible inputs without placing restricted residential identifiers, coordinates, polygons, or imagery in the public GitHub release.

## Scope

The public release is an anonymized benchmark table. It is expanded and optimized from the dataset used in the ECCV 2026 paper and will be maintained as an evolving research resource. Versioned updates may add model checkpoints, evaluation scripts, new non-sensitive aggregate fields, and improved reconstruction utilities.

## Workflow A: Licensed AOI Reconstruction With Controlled Crosswalk

This workflow is for researchers who have their own licensed access to Baidu Maps, Amap, Google Earth, or equivalent imagery providers.

The public `aoi_id` values are stable anonymous identifiers. They do not encode names, coordinates, provider IDs, or geometry. Reconstructing exact paper AOIs therefore requires a controlled crosswalk file distributed only under a non-commercial data-use agreement.

### Inputs

- Public anonymized table:
  - `data/gba_gcs_mainland_anonymized_aoi_labels.csv`
  - optionally `data/hk_macao_transfer_diagnostics_anonymized_aoi_labels.csv`
- Controlled crosswalk, available only after DUA approval:
  - `aoi_id`
  - provider namespace
  - provider AOI identifier or query key when redistribution is allowed by the requester's license
  - city
  - checksum of the expected geometry record
- Researcher's own API credentials and provider terms permitting AOI retrieval and imagery use.

### Steps

1. Join the public CSV with the controlled crosswalk on `aoi_id`.
2. Query the licensed map provider for AOI polygons and permitted metadata.
3. Download or prepare imagery using the requester's own licensed imagery source.
4. Convert each AOI to the model input schema:

```text
aoi_id
city
geometry
image_path
text_metadata
structured_features
label
split
```

5. Run the released MCGC preprocessing and inference code when the model repository is published.

### Ethics And Redistribution

Do not redistribute reconstructed names, coordinates, provider IDs, polygons, or image chips. Derived aggregate statistics may be published when they do not expose individual residential compounds.

## Workflow B: Fully Open OSM + GEE Reconstruction

This workflow uses OpenStreetMap and Google Earth Engine or open satellite products to create a fully open, license-compatible benchmark-style dataset. It is not an exact reconstruction of the proprietary AOI set, but it provides an unrestricted path for building comparable AOI-plus-imagery inputs.

### Inputs

- OpenStreetMap building, landuse, place, and highway features.
- Optional OSMnx road-network extraction.
- Google Earth Engine access for open imagery products, or other open imagery sources.
- Released MCGC preprocessing and model code.

### Steps

1. Select a city boundary from OSM or an open administrative boundary source.
2. Extract residential candidate polygons:
   - `landuse=residential`
   - residential building clusters
   - named residential complexes where available
3. Clean polygons:
   - remove very small slivers
   - merge adjacent residential fragments with shared names or contiguous footprints
   - simplify invalid geometries
4. Build contextual features:
   - road-network connectivity around each AOI with OSMnx
   - internal/external POI counts from OSM
   - area, compactness, perimeter, and optional floor-area proxies where available
5. Fetch open imagery through GEE:
   - define a buffered AOI window
   - select a cloud-free composite or high-resolution open product
   - export fixed-size image tiles
6. Produce the model input schema:

```text
aoi_id
city
geometry
image_path
text_metadata
structured_features
label_optional
split_optional
```

7. Run MCGC inference after the model checkpoint and inference scripts are released.
8. Treat outputs as model predictions requiring local validation, not as universal ground truth.

### Recommended Output Files

```text
open_reconstruction/
  aoi_candidates.geojson
  image_tiles/
  features.csv
  model_inputs.jsonl
  predictions.csv
  README.md
```

## Model Release Plan

The public dataset repository will remain focused on dataset metadata, anonymized labels, release policy, and reconstruction instructions. The MCGC model code and checkpoints should be released in a separate repository and linked here. That model repository should include:

- preprocessing from AOI geometry to image/text/structured tensors
- inference scripts
- evaluation scripts
- model cards and intended-use restrictions
- checkpoint hashes

