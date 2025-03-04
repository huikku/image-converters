# Image Converters

A collection of Python utilities for converting images between different formats with a simple drag-and-drop interface.

## Tools Included

### WebP Converter
Converts images to WebP format with 50% scaling and 50% quality, which is ideal for web optimization.



### Favicon ICO Converter
Converts images to ICO format for use as website favicons, with multiple size options.



## Features

- Simple drag-and-drop interface
- Fast batch processing
- Maintains transparency where applicable
- No command-line knowledge required

## Requirements

- Python 3.6+
- Pillow (PIL Fork)
- tkinterdnd2 (for drag-and-drop functionality)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/image-converters.git
   cd image-converters
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### WebP Converter

1. Run the WebP converter:
   ```
   python webp_converter.py
   ```

2. Drag and drop image files onto the application window.
3. WebP versions will be created in the same folder as the original files, with the same filename but .webp extension.
4. The converted images will be scaled to 50% of their original size with 50% quality.

### Favicon ICO Converter

1. Run the Favicon converter:
   ```
   python favicon_converter.py
   ```

2. Select the favicon sizes you want to include in the ICO file (16x16, 32x32, etc.).
3. Drag and drop image files onto the application window.
4. ICO files will be created in the same folder as the original files, with the same filename but .ico extension.
5. Each ICO will contain all the sizes you selected, with proper transparency.

## Notes

- For best favicon results, start with a large, square PNG image with transparency.
- WebP conversion works best with JPG and PNG files.
- Both converters preserve the original files and create new ones with different extensions.

## Troubleshooting

If you encounter drag-and-drop issues:

1. Make sure tkinterdnd2 is installed: 
   ```
   pip install tkinterdnd2
   ```

2. If installation fails, try: 
   ```
   pip install --no-deps --upgrade tkinterdnd2
   ```

3. On some systems, you may need to install the package from a wheel file:
   Download from: https://pypi.org/project/tkinterdnd2/#files

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
