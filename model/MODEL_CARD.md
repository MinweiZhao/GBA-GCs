# MCGC Model Card

MCGC is a vision-centric multimodal classifier for gated/open residential compound recognition.

Required modality:

- remote-sensing image tile

Optional modalities:

- text metadata embedding
- numerical/structured features such as area, FAR, and POI density

The public reference API supports missing optional modalities through `has_text` and `has_numerical` masks. The visual modality is required and cannot be omitted.

Large trained checkpoints are not committed directly to this data repository. Final checkpoint files should be released through GitHub Releases or controlled storage with filename, SHA-256 hash, training data version, expected input schema, license, and intended-use restrictions.

Not intended for surveillance, geofencing, policing, commercial real-estate scoring, resident-level profiling, or per-compound public lookup systems.

