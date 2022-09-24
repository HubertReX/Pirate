from PIL import Image
import os

# image = Image.open('graphics/coins/Potion/1.png')

def interate_dir(directory, out_dir):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f) and '.png' in filename:
            print(f)
            resize_image(f, 24, 32, os.path.join(out_dir, filename))

def resize_image(image_file, x, y, out_dir):
    image = Image.open(image_file)
    #print(image.size)
    new_image = image.resize((24, 32), resample=Image.Resampling.NEAREST)
    #print(new_image.size)
    #new_image.show()
    new_image.save(out_dir)


