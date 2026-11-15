"""Download and verify the original MCGC artifact without deserializing it."""

import argparse
import hashlib
from pathlib import Path

FILENAME = "trimodal_io_fused_gba_full.pth"
SIZE = 1716771558
SHA256 = "48518dafd9b2e2702db812ae9977bc6699bbc2e55c4a8044bd7d993114ebb1b8"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-id", default="__HF_NAMESPACE__/MCGC")
    args = parser.parse_args()
    from huggingface_hub import hf_hub_download

    path = Path(hf_hub_download(args.repo_id, FILENAME))
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    if path.stat().st_size != SIZE or digest.hexdigest() != SHA256:
        raise SystemExit("Checkpoint integrity check failed.")
    print(path)
    print("Verified original MCGC checkpoint; no model code was executed.")


if __name__ == "__main__":
    main()
