### Inspiration comes from https://stackoverflow.com/questions/53704524/show-gif-and-wait-for-key-press

import glob, os, sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_images(path: str) -> list:
    """
    Recursively crawl through dir and load in all images
    """
    print("Loading images")
    images = []
    image_files = glob.glob(os.path.join(path, '*'))

    for i in image_files:
        images.append(cv2.imread(i))
    print(len(image_files), " images loaded")
    return images

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

