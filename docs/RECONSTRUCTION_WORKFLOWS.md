# Reconstruction Workflows

This document describes two ways to reconstruct benchmark-compatible inputs without placing restricted residential identifiers, full AOI polygons, or imagery in the public GitHub release.

## Scope

The public release is a georeferenced, boundary-free benchmark table. It is expanded and optimized from the dataset used in the ECCV 2026 paper and will be maintained as an evolving research resource. Versioned updates may add model checkpoints, evaluation scripts, new non-sensitive aggregate fields, and improved reconstruction utilities.

## Workflow A: Licensed Baidu/Amap AOI Reconstruction From Centroid And Area

This workflow is for researchers who have their own licensed access to Baidu Maps, Amap, Google Earth, or equivalent imagery providers. It is the closest path to reconstructing the paper-style AOI inputs, but it is not an unrestricted public-data workflow because exact AOI geometries and provider records are governed by the requester's provider agreements.

The public `aoi_id` values are stable row identifiers, but reconstruction should not depend on them. Use `centroid_lon`, `centroid_lat`, `area_m2`, and `city` as the primary matching fields. This avoids breakage when provider IDs or internal AOI IDs change across future updates.

### Inputs

- Public georeferenced table:
  - `data/gba_gcs_mainland_public_georeferenced.csv`
  - optionally `data/hk_macao_transfer_diagnostics_public_georeferenced.csv`
- Public matching fields:
  - `city`
  - `centroid_lon`
  - `centroid_lat`
  - `area_m2`
- Optional controlled crosswalk for strict audit/reproduction, available only after DUA approval.
- Researcher's own API credentials and provider terms permitting AOI retrieval and imagery use.

### Provider Access Setup

1. Register a Baidu Maps Open Platform or Amap developer account.
2. Create a server-side API key with access to the relevant POI/AOI search endpoints allowed by your account and local terms.
3. Record the API product, date, quota, and terms-of-service version used for reconstruction.
4. Do not commit API keys, provider IDs, raw provider responses, names, addresses, or reconstructed polygons to a public repository.

### Reconstruction Steps

1. Read a public row and build a local search window around `centroid_lon`, `centroid_lat`.
2. Query the licensed provider for residential AOIs or residential POIs within the search radius.
3. Rank candidates by spatial distance to the centroid and relative area difference:

```text
score = distance_m / distance_tolerance_m
      + abs(candidate_area_m2 - area_m2) / max(area_m2, area_floor_m2)
```

4. Select a candidate only if it passes conservative thresholds, for example:
   - centroid distance <= 150 m
   - relative area difference <= 0.50
   - city matches the expected city
   - residential category or provider tag is compatible
5. Validate the returned AOI record:
   - city matches the expected city
   - geometry is valid
   - duplicate or overlapping provider records are resolved by the documented matching score
   - optional controlled checksums are used only when strict DUA-based reproduction is required
6. Download or prepare imagery using the requester's own licensed imagery source.
7. Convert each AOI to the model input schema:

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

8. Run the released MCGC preprocessing and inference code.

### Suggested Local Directory

```text
licensed_reconstruction/
  public_seed_rows.csv           # centroid/area rows from this repo
  optional_private_crosswalk.csv # controlled, never public
  provider_responses/            # controlled, never public
  aoi_geometries/                # controlled, never public
  image_tiles/                   # controlled, never public unless license permits
  model_inputs.jsonl
  predictions.csv
  reconstruction_report.md
```

### Minimal Pseudocode

```python
public = read_csv("data/gba_gcs_mainland_public_georeferenced.csv")

for row in public:
    candidates = query_provider_nearby(
        lon=row["centroid_lon"],
        lat=row["centroid_lat"],
        radius_m=300,
        category="residential",
        api_key=BAIDU_OR_AMAP_KEY,
    )
    provider_record = rank_by_centroid_and_area(candidates, row["centroid_lon"], row["centroid_lat"], row["area_m2"])
    geometry = validate_geometry(provider_record, expected_city=row["city"])
    image = fetch_licensed_image_tile(geometry, buffer_m=50)
    features = build_structured_features(geometry, provider_record)
    write_model_input(row["aoi_id"], geometry, image, features)
```

### Ethics And Redistribution

Do not redistribute reconstructed names, coordinates, provider IDs, polygons, or image chips. Derived aggregate statistics may be published when they do not expose individual residential compounds.

## Workflow B: Fully Open OSM + GEE Reconstruction

This workflow uses OpenStreetMap and Google Earth Engine or open satellite products to create a fully open, license-compatible benchmark-style dataset. It can use public centroid/area rows as seeds, or it can generate a new city-scale AOI set from OSM alone. It is not an exact reconstruction of the proprietary AOI set, but it provides an unrestricted path for building comparable AOI-plus-imagery inputs.

### Inputs

- OpenStreetMap building, landuse, place, and highway features.
- Optional OSMnx road-network extraction.
- Google Earth Engine access for open imagery products, or other open imagery sources.
- Public centroid/area rows from this repository, when reconstructing GBA-GCs-style records.
- Released MCGC preprocessing and model code.

### Steps

1. Select public seed rows or a city boundary from OSM/open administrative boundaries.
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
5. Match candidates to public seed rows when using this repository:
   - nearest candidate centroid
   - relative area difference
   - overlap with a centroid buffer if available
6. Fetch open imagery through GEE:
   - define a buffered AOI window
   - select a cloud-free composite or high-resolution open product
   - export fixed-size image tiles
7. Produce the model input schema:

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

8. Run MCGC inference with visual imagery required and text/numerical inputs optional.
9. Treat outputs as model predictions requiring local validation, not as universal ground truth.

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
seed_rows = read_csv("data/gba_gcs_mainland_public_georeferenced.csv")
residential = ox.features_from_polygon(
    city_boundary.geometry.iloc[0],
    tags={"landuse": "residential"},
)
aois = clean_and_filter_residential_polygons(residential)
matched = match_to_seed_rows(aois, seed_rows, keys=["centroid_lon", "centroid_lat", "area_m2"])
tiles = export_gee_tiles(matched, buffer_m=50, output_dir="image_tiles")
features = build_osm_features(matched)
write_model_inputs(matched, tiles, features, output="model_inputs.jsonl")
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

The public dataset repository includes a reference MCGC inference API in `model/` and a minimal calling example in `examples/`. Large trained checkpoints should be released through GitHub Releases or controlled storage and linked here. The full model release should include:

- preprocessing from AOI geometry to image/text/structured tensors
- inference scripts
- evaluation scripts
- model cards and intended-use restrictions
- checkpoint hashes
