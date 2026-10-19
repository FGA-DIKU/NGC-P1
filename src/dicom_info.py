"""Print the header fields and decoded pixel stats that matter for displaying DICOMs.

Usage: python dicom_info.py <file.dcm> [<file.dcm> ...]
"""

import sys
import warnings

import numpy as np
import PIL
import pydicom
from pydicom.encaps import generate_fragments, generate_frames
from pydicom.pixels import pixel_array
from pydicom.pixels.decoders.base import get_decoder


def white_stats(img) -> str:
    """Share of white pixels in the whole image, its top 20% and the rest."""
    white = img == 255
    if img.ndim == 3 and img.shape[-1] == 3:
        white = white.all(axis=-1)
    top = white.shape[-2] // 5
    return (
        f"white: all {white.mean():.0%}, "
        f"top 20% {white[..., :top, :].mean():.0%}, "
        f"rest {white[..., top:, :].mean():.0%}"
    )


def jpeg_header(frame: bytes) -> str:
    """Summarize the JPEG frame and scan headers of one compressed frame."""
    sof = -1
    for marker in (b"\xff\xc0", b"\xff\xc1", b"\xff\xc3"):
        sof = frame.find(marker)
        if sof != -1:
            break
    if sof == -1:
        return "no JPEG frame header found"
    precision = frame[sof + 4]
    height = int.from_bytes(frame[sof + 5 : sof + 7], "big")
    width = int.from_bytes(frame[sof + 7 : sof + 9], "big")
    components = frame[sof + 9]

    sos = frame.find(b"\xff\xda")
    scan_components = frame[sos + 4]
    predictor = frame[sos + 5 + 2 * scan_components]
    point_transform = frame[sos + 7 + 2 * scan_components] & 0x0F

    dri = frame.find(b"\xff\xdd")
    restart = int.from_bytes(frame[dri + 4 : dri + 6], "big") if dri != -1 else 0
    # Fragments are padded to an even length with a zero byte
    ends_with_eoi = frame.rstrip(b"\x00").endswith(b"\xff\xd9")
    return (
        f"precision {precision}, size {height} {width}, components {components}, "
        f"predictor {predictor}, point transform {point_transform}, "
        f"restart interval {restart}, ends with EOI {ends_with_eoi}"
    )


def describe(path: str):
    """Print one file's color-related header fields and pixel stats."""
    dcm = pydicom.dcmread(path, force=True)
    syntax = dcm.file_meta.get("TransferSyntaxUID")
    print(path)
    print(
        "  ",
        syntax.name if syntax else "no TransferSyntaxUID",
        dcm.get("PhotometricInterpretation"),
        "samples", dcm.get("SamplesPerPixel"),
        "planar", dcm.get("PlanarConfiguration"),
        "bits", dcm.get("BitsAllocated"), dcm.get("BitsStored"),
        "signed", dcm.get("PixelRepresentation"),
        "frames", dcm.get("NumberOfFrames", 1),
        "size", dcm.get("Rows"), dcm.get("Columns"),
        dcm.get("Manufacturer"),
    )
    if syntax is None or "PixelData" not in dcm:
        return

    # Uncompressed: look at the stored bytes before any decoding
    if not syntax.is_compressed:
        raw = np.frombuffer(dcm.PixelData, dtype=np.uint8)
        print(f"   raw bytes: {(raw == 255).mean():.0%} are 255")
    else:
        num_frames = int(dcm.get("NumberOfFrames", 1) or 1)
        fragments = list(generate_fragments(dcm.PixelData))
        frame = next(generate_frames(dcm.PixelData, number_of_frames=num_frames))
        print(
            f"   compressed: {len(fragments)} fragments, "
            f"{len(frame)} bytes in first frame"
        )
        print("   jpeg:", jpeg_header(frame))

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            img = dcm.pixel_array
            print("   decoded", img.shape, img.dtype, white_stats(img))
        except Exception as e:
            print("   decode error:", e)
    for warning in caught:
        print("   warning:", warning.message)

    # Compressed: compare every installed decoder
    if syntax.is_compressed:
        for plugin in sorted(get_decoder(syntax).available_plugins):
            try:
                img = pixel_array(path, decoding_plugin=plugin)
                print("   with", plugin, white_stats(img))
            except Exception as e:
                print("   with", plugin, "error:", e)


def main():
    print(
        "pydicom", pydicom.__version__,
        "| numpy", np.__version__,
        "| pillow", PIL.__version__,
    )
    for path in sys.argv[1:]:
        describe(path)


if __name__ == "__main__":
    main()
