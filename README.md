# Simple Pixel Sprite Generator

Simple Pixel Sprite Generator is a lightweight Python tool that converts images into pixel art textures and spritemap by applying a pixelation effect. It can process a single image or a directory of images (supporting PNG and TGA formats), and can optionally generate a spritemap that arranges all processed images in a grid. The tool also provides an optional auto-contrast adjustment to enhance the clarity of the pixelated images.

## Features

- **Input Flexibility:** Process a single image or multiple images from a directory.
- **Supported Formats:** Works with PNG and TGA image formats.
- **Adjustable Pixelation:** Set the pixelation level with customizable values (suggested: 4, 8, 16, 32; default: 16).
- **Auto-Contrast Option:** Optionally apply auto-contrast adjustment to make images clearer.
- **Spritemap Generation:** Option to combine all processed images into one large PNG spritemap.

## Requirements

- **Python 3.x**
- **Pillow Library** 
## Installation
1 - Clone or download the repository.
2 - Install the required dependency:

```
python3 -m pip install -r requirements.txt
```

## Usage
Run the script using Python from the command line. Below are some usage examples:

### Example 1: Process a Single Image
Process a single image with a pixel size of 4 and apply auto-contrast:

```
python3 simple-pixel-sprite-generator.py --input path/to/image.png --pixel-size 4 --auto-adjust
```

### Example 2: Process a Directory and Generate a Spritemap
Process all images in a directory, specify an output folder, and generate a spritemap:

```
python3 simple-pixel-sprite-generator.py --input path/to/images/ --output path/to/output/ --spritemap
```

## Acknowledgements
- This tool leverages the Pillow library for image processing.
- Part of the "color auto-adjustment" code and the documentation of the methods was generated using ChatGPT o3-mini-high model.
- Feel free to adjust or expand upon this documentation as needed for your project.

## Samples
![Textures Samples](https://github.com/maclovin/simple-pixel-sprite-generator/blob/main/doc/textures-before-after.png?raw=true)


![Generated Spritemap](https://github.com/maclovin/simple-pixel-sprite-generator/blob/main/doc/spritemap.png?raw=true)


![Unity Scene Using Pixelated Textures](https://github.com/maclovin/simple-pixel-sprite-generator/blob/main/doc/unity-example.png?raw=true)

