# Code Notes

`validate_public_release.py` checks the public CSV schema, expected row counts, allowed labels, and absence of direct sensitive tokens in the public data files:

```bash
python code/validate_public_release.py
```

For reconstruction beyond the anonymized release, use public map data and your own licensed imagery sources where possible. The original controlled package contains third-party and privacy-sensitive components that are not mirrored in this public repository.

See `../docs/RECONSTRUCTION_WORKFLOWS.md` for two supported paths:

- licensed reconstruction from controlled AOI crosswalks and provider APIs
- fully open reconstruction using OSM/OSMnx and GEE/open imagery
