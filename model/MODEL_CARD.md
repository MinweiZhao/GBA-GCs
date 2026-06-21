# MCGC Model Card

MCGC is a vision-centric multimodal classifier for gated/open residential compound recognition.

## Architecture Summary

The paper model uses:

- DINOv3-SAT visual backbone with LoRA adaptation
- inner/outer visual context around the AOI
- optional text encoder for community metadata
- MLP encoder for structured numerical attributes
- cross-modal community-aware fusion for image/text/numerical interactions
- confidence/modality-aware fusion so weak or missing modalities do not dominate

Required modality:

- remote-sensing image tile

Optional modalities:

- text metadata embedding
- numerical/structured features such as area, FAR, and POI density

The public reference API supports missing optional modalities through `has_text` and `has_numerical` masks. The visual modality is required and cannot be omitted.

## Released Checkpoint

The ECCV 2026 checkpoint is distributed as a GitHub Release asset:

- Release: https://github.com/MinweiZhao/GBA-GCs/releases/tag/v2026-06-mcgc
- Asset: `trimodal_io_fused_gba_full.pth`
- Size: approximately 1.6 GB
- SHA-256: `48518dafd9b2e2702db812ae9977bc6699bbc2e55c4a8044bd7d993114ebb1b8`

Verify the checksum after download before using the checkpoint.

## Input Contract

Reference API tensors:

```text
image:          [B, 3, H, W], required
text_embedding: [B, 768], optional
numerical:      [B, 3], optional
has_text:       [B] or [B, 1], optional mask
has_numerical:  [B] or [B, 1], optional mask
```

Recommended numerical features for the public reconstruction path:

- `area_m2`
- FAR if reconstructed from licensed/open sources
- POI density or POI count if reconstructed from licensed/open sources

When text or numerical inputs are unavailable, pass `None` or set the corresponding mask to zero. Do not omit the image modality.

## Projection And Reconstruction Context

The public dataset provides WGS84 centroids (`EPSG:4326`) and `area_m2` to seed AOI reconstruction. Full AOI polygons are not public. Reconstructed AOIs should be used to crop image tiles before MCGC inference, and any reconstructed names, addresses, provider IDs, polygons, or imagery must follow the relevant source licenses and ethics rules.

Not intended for surveillance, geofencing, policing, commercial real-estate scoring, resident-level profiling, or per-compound public lookup systems.
