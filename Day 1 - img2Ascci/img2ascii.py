#!/usr/bin/env python3
"""
img2ascii.py — Image to ASCII converter (CLI)

Features:
- Converts images to ASCII art.
- Optionally saves to a text file.
- Adjustable output width.
- Invert brightness and choose character set.
- Optional colored output using ANSI escape codes.
- Requires Pillow and (optionally) colorama for Windows.

Install requirements:
    pip install pillow colorama
"""

import sys
import argparse
from PIL import Image, ImageOps
import math

# Optional: import colorama for Windows terminal color support
try:
    import colorama
    colorama.init()
except Exception:
    colorama = None

# Default character ramps (dense -> sparse)
DEFAULT_RAMP = "@%#*+=-:. "
EXTENDED_RAMP = "$@B%8&WM#*oahkbdpqwmZ0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def get_args():
    p = argparse.ArgumentParser(description="Image → ASCII art")
    p.add_argument("image", help="Path to the input image")
    p.add_argument("-W", "--width", type=int, default=100, help="Output character width (default: 100)")
    p.add_argument("-o", "--output", help="Save ASCII to file instead of printing")
    p.add_argument("-r", "--ramp", choices=["default","extended"], default="default", help="Character ramp density")
    p.add_argument("-i", "--invert", action="store_true", help="Invert brightness mapping")
    p.add_argument("-c", "--color", action="store_true", help="Produce colored ASCII (ANSI). Uses foreground color based on pixel RGB.")
    p.add_argument("-g", "--grayscale_only", action="store_true", help="Force grayscale (no color even if -c specified)")
    p.add_argument("-b", "--background", action="store_true", help="Use background color instead of foreground for colored output (ANSI BG)")
    return p.parse_args()

def map_pixel_to_char(luminance, ramp, invert=False):
    if invert:
        luminance = 255 - luminance
    # Normalize 0..255 to 0..len(ramp)-1
    idx = int((luminance / 255) * (len(ramp) - 1))
    return ramp[idx]

def rgb_to_ansi_fg(r, g, b):
    # Use 24-bit (truecolor) ANSI escape code
    return f"\x1b[38;2;{r};{g};{b}m"

def rgb_to_ansi_bg(r, g, b):
    return f"\x1b[48;2;{r};{g};{b}m"

def reset_ansi():
    return "\x1b[0m"

def image_to_ascii(img: Image.Image, width: int, ramp: str, invert: bool=False,
                   color: bool=False, bg_color: bool=False, grayscale_only: bool=False):
    # Convert to RGB
    img = img.convert("RGB")
    # Resize preserving aspect ratio. Characters are taller than wide in many fonts,
    # so use a correction factor (approx 0.5 or 0.55). Tweak as needed.
    aspect_correction = 0.55  # character height / width factor
    w0, h0 = img.size
    new_w = width
    new_h = max(1, int((h0 / w0) * new_w * aspect_correction))
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # Convert to grayscale for brightness mapping
    gray = ImageOps.grayscale(img)

    lines = []
    for y in range(img.height):
        line = []
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            lum = gray.getpixel((x, y))  # 0..255
            ch = map_pixel_to_char(lum, ramp, invert=invert)
            if color and not grayscale_only:
                if bg_color:
                    line.append(f"{rgb_to_ansi_bg(r,g,b)}{ch}{reset_ansi()}")
                else:
                    line.append(f"{rgb_to_ansi_fg(r,g,b)}{ch}{reset_ansi()}")
            else:
                line.append(ch)
        lines.append("".join(line))
    return "\n".join(lines)

def main():
    args = get_args()
    ramp = EXTENDED_RAMP if args.ramp == "extended" else DEFAULT_RAMP

    try:
        img = Image.open(args.image)
    except Exception as e:
        print(f"Error opening image: {e}", file=sys.stderr)
        sys.exit(1)

    ascii_art = image_to_ascii(img,
                               width=args.width,
                               ramp=ramp,
                               invert=args.invert,
                               color=args.color and not args.grayscale_only,
                               bg_color=args.background,
                               grayscale_only=args.grayscale_only)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                # If user requested color, we still write ANSI codes to file.
                f.write(ascii_art)
            print(f"Saved ASCII art to: {args.output}")
        except Exception as e:
            print(f"Error saving to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(ascii_art)

if __name__ == "__main__":
    main()
    
# Appa is My Hero
