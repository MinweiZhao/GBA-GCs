# MCGC Checkpoints

The trained MCGC checkpoint is distributed through GitHub Releases rather than committed to this repository.

## ECCV 2026 Checkpoint

- Release: https://github.com/MinweiZhao/GBA-GCs/releases/tag/v2026-06-mcgc
- Asset: `trimodal_io_fused_gba_full.pth`
- Size: approximately 1.6 GB
- SHA-256: `48518dafd9b2e2702db812ae9977bc6699bbc2e55c4a8044bd7d993114ebb1b8`
- Associated public data version: `2026-06-public-georeferenced`
- Associated controlled documentation repository: https://github.com/MinweiZhao/GBA-GCs-Controlled-Access

Verify after download:

```bash
sha256sum trimodal_io_fused_gba_full.pth
```

The checksum must match:

```text
48518dafd9b2e2702db812ae9977bc6699bbc2e55c4a8044bd7d993114ebb1b8  trimodal_io_fused_gba_full.pth
```

## Input Contract

The visual modality is required. Optional text and numerical modalities may be absent if the corresponding modality masks are set.

```text
image:          [B, 3, H, W], required
text_embedding: [B, 768], optional
numerical:      [B, 3], optional
has_text:       [B] or [B, 1], optional mask
has_numerical:  [B] or [B, 1], optional mask
```

## Use Restrictions

This checkpoint is released for non-commercial research, reproducibility, benchmarking, and aggregate urban-science analysis. It is not intended for surveillance, policing, geofencing, commercial real-estate scoring, resident-level profiling, targeted enforcement, or per-compound public lookup systems.
