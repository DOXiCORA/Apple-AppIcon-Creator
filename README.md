
# AppIcon Creator

A simple Python script to generate app icons for iOS, macOS, and watchOS from a base image. This project creates the necessary icon files and corresponding JSON configuration files for your Xcode project.

## Features

- Generate app icons for multiple platforms:
  - iOS
  - macOS
  - watchOS
- Maintain aspect ratio while resizing images
- Automatically create the required directory structure
- Output icons in the correct sizes and formats for each platform

## Requirements

- Python 3.x
- [Pillow](https://pypi.org/project/Pillow/) library for image processing

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/AppIcon-Creator.git
   cd AppIcon-Creator
   ```

2. Install the required Python package:

   ```bash
   pip install Pillow
   ```

## Usage

To generate app icons, run the script with the path to your base image and the desired output directory:

```bash
python creator.py <path_to_base_image> <output_directory>
```

For example:

```bash
python creator.py /path/to/your/image.png /path/to/output
```

## Icon Sizes

### iOS
- 1024x1024 @1x
- 1024x1024 for dark and tinted appearances

### macOS
- 16x16 @1x, @2x
- 32x32 @1x, @2x
- 128x128 @1x, @2x
- 256x256 @1x, @2x
- 512x512 @1x, @2x

### watchOS
- 1024x1024 @1x

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you would like to contribute.

## Acknowledgments

- [Pillow](https://pypi.org/project/Pillow/) for image processing capabilities.
