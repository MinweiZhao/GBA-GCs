#!/usr/bin/env python3
"""Minimal MCGC inference example with optional modalities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from model.mcgc_reference import load_mcgc_reference


def load_tensor_or_none(path: str | None) -> torch.Tensor | None:
    if not path:
        return None
    return torch.load(path, map_location="cpu")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_tensor", required=True, help="Torch tensor [1,3,H,W].")
    parser.add_argument("--text_embedding", default=None, help="Optional tensor [1,768].")
    parser.add_argument("--numerical", default=None, help="Optional tensor [1,3].")
    parser.add_argument("--checkpoint", default=None, help="Optional MCGC checkpoint.")
    parser.add_argument("--output", default="prediction.json")
    args = parser.parse_args()

    image = torch.load(args.image_tensor, map_location="cpu")
    text = load_tensor_or_none(args.text_embedding)
    numerical = load_tensor_or_none(args.numerical)

    model = load_mcgc_reference(args.checkpoint)
    with torch.no_grad():
        logits = model(
            image=image,
            text_embedding=text,
            numerical=numerical,
            has_text=torch.tensor([text is not None], dtype=torch.float32),
            has_numerical=torch.tensor([numerical is not None], dtype=torch.float32),
        )
        prob = torch.softmax(logits, dim=1)[0, 1].item()
        pred = int(prob >= 0.5)

    result = {"label": "gated" if pred else "open", "probability_gated": prob}
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

