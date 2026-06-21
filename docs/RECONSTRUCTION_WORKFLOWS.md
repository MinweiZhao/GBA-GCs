# Reconstruction Workflows

This document describes two ways to reconstruct benchmark-compatible inputs without placing restricted residential identifiers, coordinates, polygons, or imagery in the public GitHub release.

## Scope

The public release is an anonymized benchmark table. It is expanded and optimized from the dataset used in the ECCV 2026 paper and will be maintained as an evolving research resource. Versioned updates may add model checkpoints, evaluation scripts, new non-sensitive aggregate fields, and improved reconstruction utilities.

## Workflow A: Licensed Baidu/Amap AOI Reconstruction With Controlled Crosswalk

This workflow is for researchers who have their own licensed access to Baidu Maps, Amap, Google Earth, or equivalent imagery providers. It is the closest path to reconstructing the paper-style AOI inputs, but it is not an unrestricted public-data workflow because exact AOI geometries and provider records are governed by the requester's provider agreements.

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

### Provider Access Setup

1. Register a Baidu Maps Open Platform or Amap developer account.
2. Create a server-side API key with access to the relevant POI/AOI search endpoints allowed by your account and local terms.
3. Record the API product, date, quota, and terms-of-service version used for reconstruction.
4. Do not commit API keys, provider IDs, raw provider responses, names, addresses, or coordinates to a public repository.

### Reconstruction Steps

1. Join the public CSV with the controlled crosswalk on `aoi_id`.
2. For each row, query the licensed provider using the approved crosswalk key or query tuple.
3. Validate the returned AOI record:
   - city matches the expected city
   - geometry is valid
   - provider response checksum matches the controlled manifest when a checksum is supplied
   - duplicate provider records are resolved by the documented rule in the DUA package
4. Download or prepare imagery using the requester's own licensed imagery source.
5. Convert each AOI to the model input schema:

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

6. Run the released MCGC preprocessing and inference code when the model repository is published.

### Suggested Local Directory

```text
licensed_reconstruction/
  private_crosswalk.csv          # controlled, never public
  provider_responses/            # controlled, never public
  aoi_geometries/                # controlled, never public
  image_tiles/                   # controlled, never public unless license permits
  model_inputs.jsonl
  predictions.csv
  reconstruction_report.md
```

### Minimal Pseudocode

```python
public = read_csv("data/gba_gcs_mainland_anonymized_aoi_labels.csv")
crosswalk = read_controlled_crosswalk("private_crosswalk.csv")
rows = join(public, crosswalk, on="aoi_id")

for row in rows:
    provider_record = query_provider(row["provider_query_key"], api_key=BAIDU_OR_AMAP_KEY)
    geometry = validate_geometry(provider_record, expected_city=row["city"])
    image = fetch_licensed_image_tile(geometry, buffer_m=50)
    features = build_structured_features(geometry, provider_record)
    write_model_input(row["aoi_id"], geometry, image, features)
```

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

### Recommended Open-Source Stack

- `osmnx` / `geopandas` / `shapely` for OSM extraction and polygon cleaning.
- `earthengine-api` or `geemap` for GEE imagery export.
- `rasterio` / `rio-tiler` for local tile normalization.
- the released MCGC model repository for preprocessing and inference.

### Minimal Pseudocode

```python
import osmnx as ox
import geopandas as gpd

city_boundary = load_open_boundary("Guangzhou")
residential = ox.features_from_polygon(
    city_boundary.geometry.iloc[0],
    tags={"landuse": "residential"},
)
aois = clean_and_filter_residential_polygons(residential)
tiles = export_gee_tiles(aois, buffer_m=50, output_dir="image_tiles")
features = build_osm_features(aois)
write_model_inputs(aois, tiles, features, output="model_inputs.jsonl")
run_mcgc_inference("model_inputs.jsonl", checkpoint="mcgc.pt")
```

### Output Status

Outputs from this workflow should be labeled as `open_reconstruction_prediction`, not as the original GBA-GCs labels. The workflow is intended to support fully open, reproducible dataset creation in new cities or under stricter licensing constraints.

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
