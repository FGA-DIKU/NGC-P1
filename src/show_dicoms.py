"""Show the DICOM files in a directory, 6 at a time, in pop-out windows.

Closing a window opens the next one.

Usage: python show_dicoms.py <directory> [--recursive] [--per-window N]
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


def find_dicoms(directory: Path, recursive: bool) -> list:
    """Return all DICOM paths in the directory, sorted by path."""
    pattern = "**/*" if recursive else "*"
    paths = []
    for path in sorted(directory.glob(pattern)):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".dcm", ".dicom"} or is_dicom(path):
            paths.append(path)
    return paths


def decompress_if_needed(ds):
    """Decompress a compressed DICOM in place."""
    if ds.file_meta.TransferSyntaxUID.is_compressed:
        try:
            declared_rgb = ds.get("PhotometricInterpretation") == "RGB"
            # pydicom 3 overrides an RGB label to YBR on a JFIF marker and then
            # converts RGB samples again
            ds.decompress(as_rgb=not declared_rgb)
            if declared_rgb:
                ds.PhotometricInterpretation = "RGB"
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
            ds["PixelData"].is_undefined_length = False
        except Exception as e:
            raise RuntimeError(f"Failed to decompress: {e}")
    return ds


def load_image(path: Path):
    """Read a DICOM as a displayable array plus the colormap to show it with."""
    # force=True also reads files without the standard DICOM header preamble
    dcm = pydicom.dcmread(path, force=True)
    if "TransferSyntaxUID" not in dcm.file_meta:
        dcm.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    decompress_if_needed(dcm)
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


def show_grid(directory: Path, paths: list, slots: int, title: str):
    """Plot the images in a grid and wait for the window to be closed."""
    cols = math.ceil(math.sqrt(slots))
    rows = math.ceil(slots / cols)
    # Up to 4 inches per image, keeping the window under 9 inches tall
    size = min(4, 9 / rows)
    fig, axes = plt.subplots(
        rows, cols, figsize=(size * cols, size * rows), squeeze=False
    )
    fig.canvas.manager.set_window_title(title)

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
    parser.add_argument(
        "--per-window", type=int, default=6, help="Images per window (default: 6)"
    )
    args = parser.parse_args()

    paths = find_dicoms(args.directory, args.recursive)
    if not paths:
        parser.error(f"No DICOM files found in {args.directory}")

    per_window = args.per_window
    # Keep the same grid in every window, unless there are fewer files than that
    slots = min(per_window, len(paths))
    num_windows = math.ceil(len(paths) / per_window)
    print(f"Found {len(paths)} DICOM files in {args.directory}")
    print("Close each window to open the next, or press Ctrl+C here to stop")
    for i in range(num_windows):
        window_paths = paths[i * per_window : (i + 1) * per_window]
        title = f"{args.directory} ({i + 1}/{num_windows})"
        print(f"Window {i + 1}/{num_windows}")
        show_grid(args.directory, window_paths, slots, title)


if __name__ == "__main__":
    main()
