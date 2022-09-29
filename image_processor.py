from PIL import Image
import os

# image = Image.open('graphics/coins/Potion/1.png')

def interate_dir(directory, out_dir, x, y):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f) and '.png' in filename:
            print(f)
            resize_image(f, os.path.join(out_dir, filename), x, y)

def resize_image(image_file, out_dir, x, y):
    image = Image.open(image_file)
    #print(image.size)
    new_image = image.resize((x, y), resample=Image.Resampling.NEAREST)
    #print(new_image.size)
    new_image.show()
    #new_image.save(out_dir)


if __name__ == '__main__':
    #interate_dir('graphics/coins/Potion2', 'graphics/coins/Potion3', 24, 32)
    resize_image("graphics/ui/menu_button.png", "graphics/ui/menu_button_420x150.png", 420, 150)