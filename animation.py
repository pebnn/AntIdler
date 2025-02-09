import os
import moviepy.video.io.ImageSequenceClip
import re
from datetime import datetime
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

def Time():
    now = datetime.now()
    return now.strftime("%d_%m_%y %H-%M")

def is_valid_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception as e:
        print(f"Skipping invalid image: {image_path} ({e})")
        return False

def Animation_create(fps):
    screenshot_path = "dependencies/screenshots/"
    if not os.path.exists(screenshot_path):
        os.mkdir(screenshot_path)

    animation_path = "dependencies/animation/"
    if not os.path.exists(animation_path):
        os.mkdir(animation_path)
    
    animation_files = os.listdir(animation_path)
    animation_name = len(animation_files)
    
    image_files = [os.path.join(screenshot_path, img)
                   for img in os.listdir(screenshot_path)
                   if img.endswith(".png") and is_valid_image(os.path.join(screenshot_path, img))]

    # List sorter from https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside/5967539#5967539
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        return [atoi(c) for c in re.split(r'(\d+)', text)]

    image_files.sort(key=natural_keys)  # Sort image list after order

    if not image_files:
        print("Exception: No valid image files found in the screenshot folder!")
        return

    try:
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
        animation_file_name = f"{Time()} Animation{animation_name}.mp4"
        output_path = os.path.join(animation_path, animation_file_name)
        clip.write_videofile(output_path)
        
        for file in os.listdir(screenshot_path):
            os.remove(os.path.join(screenshot_path, file))
    except Exception as e:
        print(f"An error occurred during video creation: {e}")

# If animation.py is run directly, then create animation using existing screenshots in screenshots folder.
if __name__ == "__main__":
    os.system("cls")
    Animation_create(fps=15)
