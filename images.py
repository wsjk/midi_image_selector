import matplotlib.pyplot as plt
import glob, os
import matplotlib.image as mpimg

curr = 0
images = []

def load_images(path: str) -> list:
    global images
    image_files = glob.glob(os.path.join(path, '*'))
    print(image_files)

    for i in image_files:
        images.append(mpimg.imread(i))

    return images

def next_image(evt=None):
    global curr

    print(evt.key, type(evt.key))
    # do something with current image

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
        fig.canvas.draw_idle()
    except IndexError:
        print("Sorry no image in index: ", curr)


def main(images):
    global im, fig

    fig, ax = plt.subplots()

    im = ax.imshow(images[0])

    fig.canvas.mpl_connect("key_press_event", next_image)
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--imagedir', action="store", dest='imagedir', default='')

    args = parser.parse_args()

    images = load_images(args.imagedir)
    main(images)