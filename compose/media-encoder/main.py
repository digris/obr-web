#!/usr/bin/env python3
import argparse
import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENCODER_PATH = os.path.join(PROJECT_ROOT, "services", "media-encoder")
sys.path.insert(0, ENCODER_PATH)

try:
    import encoder
except ImportError:
    sys.stderr.write(f"encoder module not in PATH")
    sys.exit(1)


def encode_dir_to_dash(
    src_dir,
    dst_dir,
):
    sys.stdout.write(f"encode dash: {src_dir} > {dst_dir}\n")
    if src := next(
        (f for f in src_dir.iterdir() if f.is_file() and f.stem == "master"),
        None,
    ):
        os.makedirs(dst_dir / "dash", exist_ok=True)
        dst = dst_dir / "dash" / "manifest.mpd"
        encoder.encode_dash(
            src=str(src.absolute()),
            dst=str(dst.absolute()),
        )


def encode_dir_to_hls(
    src_dir,
    dst_dir,
):
    sys.stdout.write(f"encode hls: {src_dir} > {dst_dir}\n")
    if src := next(
        (f for f in src_dir.iterdir() if f.is_file() and f.stem == "master"),
        None,
    ):
        os.makedirs(dst_dir / "hls", exist_ok=True)
        dst = dst_dir / "hls" / "manifest.m3u8"
        encoder.encode_hls(
            src=str(src.absolute()),
            dst=str(dst.absolute()),
        )


def run(
    master_dir,
    encoded_dir,
    force=False,
):

    num_encoded = 0
    num_skipped = 0
    master_dirs = [d for d in master_dir.iterdir() if d.is_dir() and len(d.stem) == 8]

    for src_dir in master_dirs:
        dst_dir = encoded_dir / src_dir.stem
        # if (dst_dir / 'dash').is_dir() and not force:
        #     num_skipped += 1
        # else:
        #     encode_dir_to_dash(src_dir, dst_dir)
        #     num_encoded += 1

        if (dst_dir / 'hls').is_dir() and not force:
            num_skipped += 1
        else:
            encode_dir_to_hls(src_dir, dst_dir)
            num_encoded += 1

    return num_encoded, num_skipped


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "master_dir",
        type=Path,
        help="master directory",
    )
    parser.add_argument(
        "encoded_dir",
        type=Path,
        help="encoded directory",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
    )
    args = parser.parse_args()

    force = False  # TODO: add as flag
    master_dir = args.master_dir
    encoded_dir = args.encoded_dir

    if not master_dir.is_dir():
        sys.stderr.write(f"master_dir does not exist: {master_dir}")
        sys.exit(1)

    if not encoded_dir.is_dir():
        sys.stderr.write(f"encoded_dir does not exist: {encoded_dir}")
        sys.exit(1)

    while args.interval:
        num_encoded, num_skipped = run(master_dir, encoded_dir, force)
        sys.stdout.write(
            f"files encoded: {num_encoded} - skipped: {num_skipped} - re-scan in {args.interval} seconds\n"
        )
        time.sleep(args.interval)
    else:
        num_encoded, num_skipped = run(master_dir, encoded_dir, force)
        sys.stdout.write(
            f"files encoded: {num_encoded} - skipped: {num_skipped}\n"
        )
