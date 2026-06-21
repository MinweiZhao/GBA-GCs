# Code Notes

`validate_public_release.py` checks the public CSV schema, expected row counts, allowed labels, required centroid/area fields, and absence of direct sensitive tokens in the public data files:

```bash
python code/validate_public_release.py
```

For reconstruction beyond the public georeferenced release, use licensed Baidu/Amap access or the fully open OSM/GEE workflow described in `../docs/RECONSTRUCTION_WORKFLOWS.md`.

The original controlled package contains third-party and privacy-sensitive components that are not mirrored in this public repository.
