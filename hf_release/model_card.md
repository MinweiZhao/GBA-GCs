---
library_name: pytorch
pipeline_tag: image-classification
license: other
license_name: mcgc-non-commercial-research
license_link: USE_RESTRICTIONS.md
datasets:
  - __HF_NAMESPACE__/GBA-GCs
tags:
  - arxiv:2609.03804
  - remote-sensing
  - multimodal
  - geospatial
  - gated-communities
  - urban-science
---

# MCGC: Gated/Open Residential Community Classification

Checkpoint companion to **Urban Boundaries, Social Barriers: A Benchmark and Vision-Centric Framework for Mapping Gated Communities and Equity Implications** ([arXiv:2609.03804](https://arxiv.org/abs/2609.03804)).

- [Dataset](https://huggingface.co/datasets/__HF_NAMESPACE__/GBA-GCs)
- [Code and release documentation](https://github.com/MinweiZhao/GBA-GCs)
- [Original checkpoint release](https://github.com/MinweiZhao/GBA-GCs/releases/tag/v2026-06-mcgc)

## Download the original checkpoint

```python
from huggingface_hub import hf_hub_download

checkpoint_path = hf_hub_download(
    repo_id="__HF_NAMESPACE__/MCGC",
    filename="trimodal_io_fused_gba_full.pth",
)
```

The published artifact is an unchanged mirror of the existing checkpoint, not a converted Transformers model. This repository does not currently provide a verified `from_pretrained` integration, an Inference API endpoint, or a turnkey inference pipeline.

| Property | Value |
| --- | --- |
| Filename | `trimodal_io_fused_gba_full.pth` |
| Bytes | 1,716,771,558 |
| SHA-256 | `48518dafd9b2e2702db812ae9977bc6699bbc2e55c4a8044bd7d993114ebb1b8` |

Run `python download_checkpoint.py` to download and verify the file. Downloading does not execute or deserialize the checkpoint.

## Architecture and input contract

The upstream paper describes a DINOv3-SAT visual backbone with LoRA adaptation, inner/outer visual context, optional text and numerical encoders, and cross-modal community-aware fusion.

Remote-sensing imagery is required. Text embeddings and numerical features are optional, with `has_text` and `has_numerical` modality masks. The documented reference interface accepts `image: [B, 3, H, W]`, optional `text_embedding: [B, 768]`, and optional `numerical: [B, 3]`. This is the upstream reference contract, not a validation of the full checkpoint architecture or its preprocessing.

**Compatibility limitation:** upstream `model/mcgc_reference.py` uses a lightweight convolutional image encoder rather than the paper's complete DINOv3-SAT+LoRA model. Compatibility with the released weights has not been established. Do not load the paper weights into that reference model using `strict=False` and interpret the result as a reproduced trained model. Full architecture definitions, preprocessing, and a verified strict checkpoint load are needed before advertising `PyTorchModelHubMixin.from_pretrained` support.

No independent inference or performance reproduction is claimed by this mirror. Consult [the original model card](upstream/MODEL_CARD.md) and [checkpoint documentation](upstream/CHECKPOINTS.md).

## Intended use and restrictions

This checkpoint is released for non-commercial research, reproducibility, benchmarking, and aggregate urban-science analysis. The upstream restrictions are preserved in [USE_RESTRICTIONS.md](USE_RESTRICTIONS.md). They do not grant redistribution or commercial rights to the visual backbone, imagery, text encoder, or any external data. Follow applicable upstream component terms.

It is not intended for surveillance, policing, geofencing, commercial real-estate scoring, resident-level profiling, targeted enforcement, or per-compound public lookup systems. Gated/open predictions are locally grounded research labels and must not be treated as universal social categories or human-verified ground truth.

The public dataset excludes raw imagery, names, addresses, AOI boundaries, and private provider metadata. Restricted data continue to require the [controlled-access process](https://github.com/MinweiZhao/GBA-GCs-Controlled-Access).

## Citation

Please cite **Urban Boundaries, Social Barriers: A Benchmark and Vision-Centric Framework for Mapping Gated Communities and Equity Implications**, arXiv:2609.03804 (2026), and record the checkpoint SHA-256 above.
