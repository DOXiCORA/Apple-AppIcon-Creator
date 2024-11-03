import subprocess
import sys
import os
import json

def install_pillow():
    try:
        from PIL import Image
    except ImportError:
        print("Pillow library not found. Setting up a virtual environment...")

        # Directory for virtual environment
        venv_dir = os.path.join(os.path.dirname(__file__), "venv")

        # Create virtual environment if it doesn't exist
        if not os.path.exists(venv_dir):
            subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
            print("Virtual environment created.")

        # Install Pillow in the virtual environment
        subprocess.check_call([os.path.join(venv_dir, "bin", "python"), "-m", "pip", "install", "pillow"])
        print("Pillow installed in virtual environment.")

        # Activate the virtual environment
        activate_venv(venv_dir)

    finally:
        global Image
        from PIL import Image

def activate_venv(venv_dir):
    # Ensure the virtual environment is used
    venv_python = os.path.join(venv_dir, "bin", "python")
    sys.executable = venv_python
    sys.path.insert(0, os.path.join(venv_dir, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages"))
    print("Virtual environment activated.")

# Run Pillow installation check
install_pillow()

import argparse

# Define icon sizes for each platform
icon_sizes = {
    "iOS": [
        (1024, 1)
    ],
    "macOS": [
        (16, 1), (16, 2),
        (32, 1), (32, 2),
        (128, 1), (128, 2),
        (256, 1), (256, 2),
        (512, 1), (512, 2)
    ],
    "watchOS": [
        (1024, 1)
    ]
}

# Function to generate icon
def generate_icon(base_image_path, platform_path, platform, size, scale):
    # Calculate the target size in pixels
    target_size = size * scale
    target_dimensions = (target_size, target_size)

    # Open the original image
    with Image.open(base_image_path) as img:
        # Calculate the new size to preserve aspect ratio
        img.thumbnail((target_size, target_size), Image.LANCZOS)  # Resize maintaining aspect ratio

        # Create a new image with the exact target dimensions
        new_image = Image.new("RGBA", target_dimensions, (255, 255, 255, 0))  # Use transparent background
        
        # Center the thumbnail in the new image
        img_width, img_height = img.size
        x_offset = (target_size - img_width) // 2
        y_offset = (target_size - img_height) // 2
        new_image.paste(img, (x_offset, y_offset))

        # Save the resized image with a new filename
        filename = f"icon_{platform.lower()}_{int(size)}x{int(size)}@{scale}x.png"
        new_image.save(os.path.join(platform_path, filename), format='PNG')

def create_ios_contents_json(output_path, icons):
    contents = {
        "images": [],
        "info": {
            "author": "xcode",
            "version": 1
        }
    }
    
    for size, scale in icons:
        filename = f"icon_ios_{int(size)}x{int(size)}@{scale}x.png"
        contents["images"].append({
            "filename": filename,
            "idiom": "universal",
            "platform": "ios",
            "size": f"{size}x{size}"
        })
    
    with open(os.path.join(output_path, "Contents.json"), "w") as f:
        json.dump(contents, f, indent=4)

def create_macos_contents_json(output_path, icons):
    contents = {
        "images": [],
        "info": {
            "author": "xcode",
            "version": 1
        }
    }
    
    for size, scale in icons:
        filename = f"icon_macos_{int(size)}x{int(size)}@{scale}x.png"
        contents["images"].append({
            "filename": filename,
            "idiom": "mac",
            "size": f"{size}x{size}",
            "scale": f"{scale}x"
        })
    
    with open(os.path.join(output_path, "Contents.json"), "w") as f:
        json.dump(contents, f, indent=4)

def create_watchos_contents_json(output_path, icons):
    contents = {
        "images": [],
        "info": {
            "author": "xcode",
            "version": 1
        }
    }
    
    for size, scale in icons:
        filename = f"icon_watchos_{int(size)}x{int(size)}@{scale}x.png"
        contents["images"].append({
            "filename": filename,
            "idiom": "universal",
            "platform": "watchos",
            "size": f"{size}x{size}"
        })
    
    with open(os.path.join(output_path, "Contents.json"), "w") as f:
        json.dump(contents, f, indent=4)

# Main function to generate appiconset for each platform
def generate_appiconset(base_image_path, output_path):
    for platform, icons in icon_sizes.items():
        platform_path = os.path.join(f"{output_path}/{platform}", "AppIcon.appiconset")
        if not os.path.exists(platform_path):
            os.makedirs(platform_path)
        
        if platform == "iOS":
            for size, scale in icons:
                generate_icon(base_image_path, platform_path, platform, size, scale)
            create_ios_contents_json(platform_path, icons)
        elif platform == "macOS":
            for size, scale in icons:
                generate_icon(base_image_path, platform_path, platform, size, scale)
            create_macos_contents_json(platform_path, icons)
        elif platform == "watchOS":
            for size, scale in icons:
                generate_icon(base_image_path, platform_path, platform, size, scale)
            create_watchos_contents_json(platform_path, icons)
        
        print(f"AppIcon.appiconset for {platform} generated in '{platform_path}'")

# Main script entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate AppIcon.appiconset for all Apple OSes.")
    parser.add_argument("base_image_path", type=str, help="Path to the base 1024x1024 icon image.")
    parser.add_argument("output_path", type=str, help="Directory to save the AppIcon.appiconset.")
    
    args = parser.parse_args()
    generate_appiconset(args.base_image_path, args.output_path)