#!/usr/bin/env python3
"""Reference MCGC inference API.

This compact implementation defines the public inference contract:
remote-sensing imagery is required, while text and numerical modalities are
optional and represented by modality masks when missing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import torch
from torch import nn
import torch.nn.functional as F


class MCGCReference(nn.Module):
    """Reference MCGC-style multimodal classifier.

    For paper-level reproduction, replace the lightweight image encoder with
    DINOv3-SAT+LoRA and load the released checkpoint. The forward signature is
    kept stable for downstream examples.
    """

    def __init__(
        self,
        image_dim: int = 512,
        text_dim: int = 768,
        numerical_dim: int = 3,
        hidden_dim: int = 256,
        num_classes: int = 2,
    ) -> None:
        super().__init__()
        self.image_encoder = nn.Sequential(
            nn.Conv2d(3, 32, 3, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(64, image_dim),
            nn.LayerNorm(image_dim),
        )
        self.image_proj = nn.Linear(image_dim, hidden_dim)
        self.text_proj = nn.Linear(text_dim, hidden_dim)
        self.num_proj = nn.Linear(numerical_dim, hidden_dim)
        self.gate = nn.Sequential(
            nn.Linear(hidden_dim * 3 + 2, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, 3),
        )
        self.head = nn.Sequential(
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, num_classes),
        )

    def forward(
        self,
        image: torch.Tensor,
        text_embedding: Optional[torch.Tensor] = None,
        numerical: Optional[torch.Tensor] = None,
        has_text: Optional[torch.Tensor] = None,
        has_numerical: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        if image is None:
            raise ValueError("MCGC requires the visual remote-sensing image modality.")
        if image.ndim != 4 or image.shape[1] != 3:
            raise ValueError("image must have shape [B, 3, H, W].")

        bsz = image.shape[0]
        device = image.device
        img_feat = self.image_proj(self.image_encoder(image))

        if text_embedding is None:
            text_embedding = torch.zeros(bsz, self.text_proj.in_features, device=device)
            has_text = torch.zeros(bsz, 1, device=device)
        elif has_text is None:
            has_text = torch.ones(bsz, 1, device=device)
        else:
            has_text = has_text.float().view(bsz, 1).to(device)

        if numerical is None:
            numerical = torch.zeros(bsz, self.num_proj.in_features, device=device)
            has_numerical = torch.zeros(bsz, 1, device=device)
        elif has_numerical is None:
            has_numerical = torch.ones(bsz, 1, device=device)
        else:
            has_numerical = has_numerical.float().view(bsz, 1).to(device)

        text_feat = self.text_proj(text_embedding.to(device)) * has_text
        num_feat = self.num_proj(numerical.to(device)) * has_numerical
        gate_in = torch.cat([img_feat, text_feat, num_feat, has_text, has_numerical], dim=1)
        weights = F.softmax(self.gate(gate_in), dim=1)
        fused = weights[:, 0:1] * img_feat + weights[:, 1:2] * text_feat + weights[:, 2:3] * num_feat
        return self.head(fused)


def load_mcgc_reference(checkpoint: Optional[str | Path] = None, map_location: str = "cpu") -> MCGCReference:
    model = MCGCReference()
    if checkpoint:
        state = torch.load(checkpoint, map_location=map_location)
        if isinstance(state, dict) and "model_state_dict" in state:
            state = state["model_state_dict"]
        model.load_state_dict(state, strict=False)
    model.eval()
    return model

