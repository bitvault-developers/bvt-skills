#!/usr/bin/env python3
"""Make an App Store ready app icon set from one picture.

Usage:  python3 make_icons.py <source image> <output folder> [--background RRGGBB]

Writes  <output folder>/AppIcon.appiconset/AppIcon.png   (1024x1024, no transparency)
        <output folder>/AppIcon.appiconset/Contents.json
        <output folder>/Contents.json                     (if missing)

Apple rejects icons with transparency, so see-through areas are filled with the
background colour (default white). The source should be square and at least 1024 px.
Needs the Pillow library:  pip install Pillow
"""
import json
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow is not installed. Run: pip install Pillow")
    sys.exit(2)

SIZE = 1024


def main():
    argv = sys.argv[1:]
    background = "FFFFFF"
    if "--background" in argv:
        index = argv.index("--background")
        if index + 1 >= len(argv):
            print(__doc__)
            return 2
        background = argv[index + 1].lstrip("#")
        del argv[index:index + 2]
    if len(argv) != 2:
        print(__doc__)
        return 2
    source, out_dir = argv
    try:
        colour = tuple(int(background[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        print("Background must look like FFFFFF")
        return 2

    image = Image.open(source).convert("RGBA")
    width, height = image.size
    if width != height:
        print(f"Note: source is {width}x{height}, not square. It is centred on a square canvas.")
    if min(width, height) < SIZE:
        print(f"Warning: source is smaller than {SIZE}px. The icon will look soft.")

    side = max(width, height)
    canvas = Image.new("RGBA", (side, side), colour + (255,))
    canvas.paste(image, ((side - width) // 2, (side - height) // 2), image)
    flat = Image.new("RGB", (side, side), colour)
    flat.paste(canvas, mask=canvas.split()[3])
    flat = flat.resize((SIZE, SIZE), Image.LANCZOS)

    icon_dir = os.path.join(out_dir, "AppIcon.appiconset")
    os.makedirs(icon_dir, exist_ok=True)
    flat.save(os.path.join(icon_dir, "AppIcon.png"), "PNG")

    contents = {
        "images": [{"filename": "AppIcon.png", "idiom": "universal", "platform": "ios", "size": "1024x1024"}],
        "info": {"author": "xcode", "version": 1},
    }
    with open(os.path.join(icon_dir, "Contents.json"), "w", encoding="utf-8") as handle:
        json.dump(contents, handle, indent=2)
        handle.write("\n")

    root_contents = os.path.join(out_dir, "Contents.json")
    if not os.path.exists(root_contents):
        with open(root_contents, "w", encoding="utf-8") as handle:
            json.dump({"info": {"author": "xcode", "version": 1}}, handle, indent=2)
            handle.write("\n")

    print(f"Wrote {os.path.join(icon_dir, 'AppIcon.png')} ({SIZE}x{SIZE}, no transparency)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
