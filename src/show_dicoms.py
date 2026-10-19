"""Show up to 25 DICOM files from a directory in a grid in a pop-out window.

Usage: python show_dicoms.py <directory> [--recursive] [--max-files N]
"""

import argparse
import math
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pydicom
from pydicom.misc import is_dicom
from pydicom.pixels import apply_color_lut, apply_modality_lut, apply_voi_lut


def find_dicoms(directory: Path, recursive: bool, max_files: int) -> list:
    """Return up to max_files DICOM paths in the directory, sorted by path."""
    pattern = "**/*" if recursive else "*"
    paths = []
    for path in sorted(directory.glob(pattern)):
        if len(paths) >= max_files:
            break
        if not path.is_file():
            continue
        if path.suffix.lower() in {".dcm", ".dicom"} or is_dicom(path):
            paths.append(path)
    return paths


def load_image(path: Path):
    """Read a DICOM as a displayable array plus the colormap to show it with."""
    # force=True also reads files without the standard DICOM header preamble
    dcm = pydicom.dcmread(path, force=True)
    if "TransferSyntaxUID" not in dcm.file_meta:
        dcm.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    # pydicom 3 already converts YBR to RGB here
    img = dcm.pixel_array
    samples = int(dcm.get("SamplesPerPixel", 1))
    photometric = str(dcm.get("PhotometricInterpretation", ""))

    # Multi-frame files show the middle frame
    if (samples == 1 and img.ndim == 3) or (samples > 1 and img.ndim == 4):
        img = img[img.shape[0] // 2]

    if photometric == "PALETTE COLOR":
        img = apply_color_lut(img, dcm)
    elif samples == 1:
        img = apply_voi_lut(apply_modality_lut(img, dcm), dcm)
        cmap = "gray_r" if photometric == "MONOCHROME1" else "gray"
        return img, cmap

    # imshow needs RGB as uint8 or as floats in [0, 1]
    if img.dtype != np.uint8:
        img = img / img.max()
    return img, None


def show_grid(directory: Path, paths: list):
    """Plot the images in a square-ish grid, with the file name above each."""
    cols = math.ceil(math.sqrt(len(paths)))
    rows = math.ceil(len(paths) / cols)
    # Up to 3 inches per image, keeping the window under 9 inches tall
    size = min(3, 9 / rows)
    fig, axes = plt.subplots(
        rows, cols, figsize=(size * cols, size * rows), squeeze=False
    )
    fig.canvas.manager.set_window_title(str(directory))

    for ax in axes.flat:
        ax.axis("off")
    for ax, path in zip(axes.flat, paths):
        ax.set_title(str(path.relative_to(directory)), fontsize=8)
        try:
            img, cmap = load_image(path)
            ax.imshow(img, cmap=cmap)
        except Exception as e:
            message = "Could not load:\n" + textwrap.fill(str(e), 30)
            ax.text(
                0.5,
                0.5,
                message,
                ha="center",
                va="center",
                fontsize=7,
                transform=ax.transAxes,
            )

    fig.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Show DICOM files in a grid.")
    parser.add_argument("directory", type=Path)
    parser.add_argument(
        "--recursive", action="store_true", help="Also search subdirectories"
    )
    parser.add_argument("--max-files", type=int, default=25)
    args = parser.parse_args()

    paths = find_dicoms(args.directory, args.recursive, args.max_files)
    if not paths:
        parser.error(f"No DICOM files found in {args.directory}")
    print(f"Showing {len(paths)} DICOM files from {args.directory}")
    show_grid(args.directory, paths)


if __name__ == "__main__":
    main()
