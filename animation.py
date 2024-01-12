import os
import moviepy.video.io.ImageSequenceClip
import re
from datetime import datetime

def Time():
    now = datetime.now()
    current_time = now.strftime("%d_%m_%y %H-%M")
    return str(current_time)

def Animation_create(fps):
    screenshot_path = "dependencies/screenshots/"
    if os.path.exists(screenshot_path) == False:
        os.mkdir(screenshot_path)

    animation_path = "dependencies/animation/"
    if os.path.exists(animation_path) == False:
        os.mkdir(animation_path)
    animation_files = os.listdir(animation_path)

    animation_name = 0
    for i in animation_files:
        animation_name += 1

    image_files = [os.path.join(screenshot_path, img)
                   for img in os.listdir(screenshot_path)
                   if img.endswith(".png")]



    # List sorter from https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside/5967539#5967539
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        return [atoi(c) for c in re.split(r'(\d+)', text)]



    image_files.sort(key=natural_keys) # Sort image list after order
    try:
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
        animation_file_name = Time() + " Animation" + str(animation_name) + ".mp4"
        clip.write_videofile(animation_path + animation_file_name)
        animation_files = os.listdir(animation_path)

        if (animation_file_name) in animation_files:
            screenshot_files = os.listdir("dependencies/screenshots/")
            for file in screenshot_files:
                os.remove(screenshot_path + file)
    except IndexError:
        print("Exception: No files found in screenshot folder!")

# If animation.py is run directly, then create animation using existing screenshots in screenshots folder.
if __name__ == "__main__":
    os.system("cls")
    Animation_create(fps=15)