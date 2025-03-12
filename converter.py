import os
from PIL import Image
import svglib
from reportlab.graphics import renderPM
import svglib.svglib

# TODO: Preprocess images before implementing the model

def resize_images(dir_name):
    directory = os.listdir(dir_name)
    for file in directory:
        try:
            file_path = os.path.join(dir_name, file)
            image = Image.open(file_path)
            image = image.resize((32, 32))
            image.save(file_path)
        except Exception as e:
            os.remove(file_path)  # Remove any corrupted images
            print(f"Error resizing {file}: {e}")

def convert_to_png(dir_name):
    directory = os.listdir(dir_name)
    print(f"Converting icons in {dir_name} to PNG")
    for file in directory:
        file_path = os.path.join(dir_name, file) 
        new_file_path = os.path.join(dir_name, f"{prefix}.png") 
        prefix, suffix = os.path.splitext(file)
        try:
            if suffix == '.png':
                continue
            if suffix == '.ico':
                os.remove(file_path) 
                with Image.open(file_path) as img:
                    img.save(new_file_path, 'PNG')  
                print(f"Converted {file}.ico to {prefix}.png")
            elif suffix == '.svg':
                drawing = svglib.svglib.svg2rlg(file_path)
                renderPM.drawToFile(drawing, new_file_path, fmt="PNG")
                print(f"Converted {file}.svg to {prefix}.png")
            else:
                os.remove(file_path)  # Remove any non-ICO/SVG files
                print(f"Removed {file} as it's not an .ico or .svg file")
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
       

