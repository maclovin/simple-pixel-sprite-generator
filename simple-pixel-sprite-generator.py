#!/usr/bin/env python3
"""
Usage:
    python simple-pixel-sprite-generator.py --input path/to/image_or_directory [--output path/to/output]
                         [--pixel-size N] [--spritemap] [--auto-adjust]

Examples:
    python simple-pixel-sprite-generator.py --input texture.png --pixel-size 4 --auto-adjust
    python simple-pixel-sprite-generator.py --input textures/ --output out/ --spritemap
"""

import os
import sys
import math
import argparse
from PIL import Image, ImageOps

SUPPORTED_EXTENSIONS = ('.png', '.tga')

def pixelate_image(image: Image.Image, pixel_size: int, auto_adjust: bool) -> Image.Image:
    """
    Applies a pixelation effect to the image.
    The algorithm reduces the image resolution and then scales it back up using 'nearest' interpolation
    to preserve the blocky look. If auto_adjust is True, an auto-contrast adjustment is applied
    to enhance clarity.
    """

    new_width = max(1, image.width // pixel_size)
    new_height = max(1, image.height // pixel_size)
    small_image = image.resize((new_width, new_height), resample=Image.BILINEAR)
    pixelated_image = small_image.resize(image.size, Image.NEAREST)

    if auto_adjust:
        pixelated_image = ImageOps.autocontrast(pixelated_image)

    return pixelated_image

def process_single_image(filepath: str, output_dir: str, pixel_size: int, auto_adjust: bool) -> str:
    """
    Processes a single image: applies pixelation and saves the result.
    Returns the path of the saved image.
    """

    try:
        with Image.open(filepath) as img:
            print(f"Processing {filepath}...")
            result = pixelate_image(img, pixel_size, auto_adjust)
            base_name = os.path.basename(filepath)
            name, _ = os.path.splitext(base_name)
            output_path = os.path.join(output_dir, f"{name}_pixelated.png")

            result.save(output_path)
            print(f"Saved: {output_path}")

            return output_path
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

        return None

def get_image_files(input_path: str) -> list:
    """
    Returns a list of image paths (PNG or TGA) from a directory or a single image file.
    """

    if os.path.isfile(input_path):
        if input_path.lower().endswith(SUPPORTED_EXTENSIONS):
            return [input_path]
        else:
            print(f"File {input_path} does not have a supported extension.")

            return []
    elif os.path.isdir(input_path):
        files = []

        for entry in os.listdir(input_path):
            full_path = os.path.join(input_path, entry)

            if os.path.isfile(full_path) and entry.lower().endswith(SUPPORTED_EXTENSIONS):
                files.append(full_path)

        return files
    else:
        print(f"Input {input_path} is neither a valid file nor a directory.")

        return []

def generate_spritemap(image_paths: list, output_dir: str, spritemap_name: str = "spritemap.png"):
    """
    Generates a spritemap from the processed images.
    It assumes that all images are the same size; if not, it uses the maximum dimensions found.
    The images are arranged in a square (or nearly square) grid.
    """

    if not image_paths:
        print("No images to generate a spritemap.")
        return

    images = []
    widths = []
    heights = []

    for path in image_paths:
        try:

            with Image.open(path) as img:
                img_copy = img.copy()

            images.append(img_copy)
            widths.append(img_copy.width)
            heights.append(img_copy.height)

        except Exception as e:
            print(f"Error opening {path} for spritemap: {e}")

    if not images:
        print("No valid images found for the spritemap.")
        return

    cell_width = max(widths)
    cell_height = max(heights)
    count = len(images)
    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols)
    spritemap_width = cols * cell_width
    spritemap_height = rows * cell_height
    spritemap = Image.new('RGBA', (spritemap_width, spritemap_height), (0, 0, 0, 0))

    for idx, img in enumerate(images):
        x = (idx % cols) * cell_width + (cell_width - img.width) // 2
        y = (idx // cols) * cell_height + (cell_height - img.height) // 2
        spritemap.paste(img, (x, y))

    spritemap_path = os.path.join(output_dir, spritemap_name)
    spritemap.save(spritemap_path)
    print(f"Spritemap saved: {spritemap_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Converts images (PNG/TGA) into pixel art using a pixelation effect."
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Path to the image or directory of images"
    )
    parser.add_argument(
        "--output", "-o", default=".",
        help="Output directory. Default: current directory."
    )
    parser.add_argument(
        "--pixel-size", "-p", type=int, default=16,
        help="Pixelation level. Suggested values: 4, 8, 16, 32. Default: 16."
    )
    parser.add_argument(
        "--spritemap", "-s", action="store_true",
        help="Generate a spritemap with all processed images."
    )
    parser.add_argument(
        "--auto-adjust", "-a", action="store_true",
        help="Apply auto-contrast adjustment to enhance clarity. Default: disabled."
    )
    args = parser.parse_args()

    if not os.path.exists(args.output):
        try:
            os.makedirs(args.output)
        except Exception as e:
            print(f"Error creating output directory {args.output}: {e}")
            sys.exit(1)

    image_files = get_image_files(args.input)
    if not image_files:
        print("No images found to process.")
        sys.exit(1)

    output_files = []
    for file in image_files:
        out_file = process_single_image(file, args.output, args.pixel_size, args.auto_adjust)
        if out_file:
            output_files.append(out_file)

    if args.spritemap:
        generate_spritemap(output_files, args.output)

if __name__ == '__main__':
    main()
