import os
from PIL import Image
import svglib
from reportlab.graphics import renderPM
import svglib.svglib
import hashlib
import random


def image_hash(image):
    return hashlib.md5(image.tobytes()).hexdigest()

def remove_duplicates(dir_name):
    directory = os.listdir(dir_name)
    hashes = []
    for file in directory:
        file_path = os.path.join(dir_name, file)
        try:
            image = Image.open(file_path)
            image_hash_value = image_hash(image)
            if image_hash_value in hashes:
                os.remove(file_path)
                print(f"Removed duplicate {file}")
            else:
                hashes.append(image_hash_value)
        except Exception as e:
            print(f"Error processing {file}: {e}")

# Trying sort of data augmentation

def resize_images(dir_name):
    directory = os.listdir(dir_name)
    for file in directory:
        try:
            file_path = os.path.join(dir_name, file)
            rotated_file_path = os.path.join(dir_name, f"{file[:len(file)-4]}_rotated.png")
            flipped_file_path = os.path.join(dir_name, f"{file[:len(file)-4]}_flipped.png")
            cropped_file_path = os.path.join(dir_name, f"{file[:len(file)-4]}_cropped.png")
            image = Image.open(file_path)
            image = image.resize((32, 32))
            width, height = image.size
            crop_width, crop_height = (24, 24)
            left = random.randint(0, width - crop_width)
            upper = random.randint(0, height - crop_height)
            right = left + crop_width
            lower = upper + crop_height
            cropped_image = (image.crop((left, upper, right, lower)))
            cropped_image.save(cropped_file_path)
            rotated_image = image.rotate(30)
            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
            image.save(file_path)
            rotated_image.save(rotated_file_path)
            flipped_image.save(flipped_file_path)
        except Exception as e:
            os.remove(file_path)  # Remove any corrupted images
            print(f"Error resizing {file}: {e}")

# After scraping, we convert all icons to png format
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
    
       

