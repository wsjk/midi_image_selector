### Inspiration comes from https://stackoverflow.com/questions/53704524/show-gif-and-wait-for-key-press

import matplotlib.pyplot as plt
import glob, os, sys
import cv2
import numpy as np

curr = 0
images = []

def get_images(path: str) -> list:
    """
    Recursively crawl through dir and load in all images
    """
    global images
    image_files = glob.glob(os.path.join(path, '*'))
    print(image_files)

    for i in image_files:
        images.append(cv2.imread(i))

    return images

def next_image(evt=None):
    """
    Load in next image
    """
    global curr

    print(evt.key, type(evt.key))
    # do something with current image

    if evt.key == 'escape':
        sys.exit()

    try:
        n = int(evt.key)
        print("You pressed {}".format(n))
    except ValueError:
        n = curr
        print("Sorry can only use number keys")

    # advance to next image
    try:
        curr = n
        im.set_array(images[curr])
        load_image(images[curr])
        fig.canvas.draw_idle()
    except IndexError:
        print("Sorry no image in index: ", curr)

## https://stackoverflow.com/questions/59432324/how-to-mask-image-with-binary-mask
def get_mask(image):
    """
    Create a mask to reveal only section of image
    """
    mask = np.zeros(image.shape, dtype=np.uint8)
    mask = cv2.circle(mask, (260, 300), 225, (255, 255, 255), -1)
    result = cv2.bitwise_and(image, mask)
    result[mask == 0] = 255

    return mask, result


def load_image(image):
    """
    Load an image into window
    """
    global im, ax

    mask, result = get_mask(image) ## apply mask
    ax.imshow(image)
    ax.imshow(mask)
    im = ax.imshow(result)
    return im

def main(images):
    """
    Orchestrating function to run
    """
    global im, ax, fig

    fig, ax = plt.subplots()
    load_image(images[0])

    fig.canvas.mpl_connect("key_press_event", next_image)
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--imagedir', action="store", dest='imagedir', default='')

    args = parser.parse_args()

    images = get_images(args.imagedir)

    main(images)