import matplotlib
matplotlib.use('TkAgg')  # Or another suitable backend like 'QtAgg'
import matplotlib.pyplot as plt
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import image_tools

class Images():
    def __init__(
        self, 
        path=".", 
        mode="scroll", 
        auto_start=True,
        midi=False
    ):
        self.path = path
        self.loaded_images = image_tools.get_images(self.path)
        self.curr = 0
        self.mode = mode
        if auto_start:
            self.fig, self.ax = plt.subplots()
            self.display()
            plt.get_current_fig_manager().full_screen_toggle()
            plt.show()

    def next_image(self, evt=None):
        """
        Load in next image
        """

        print(evt.key, type(evt.key))
        # do something with current image

        if evt.key == 'escape':
            sys.exit()
        try:
            n = int(evt.key)
            print("You pressed {}".format(n))
        except ValueError:
            n = self.curr
            print("Sorry can only use number keys")

        # advance to next image
        try:
            self.curr = n
            self.im.set_array(self.loaded_images[self.curr])
            self.display()
            self.fig.canvas.draw_idle()
        except IndexError:
            print("Sorry no image in index: ", n)

    def display(self):
        """
        Orchestrating function to run
        """

        image = self.loaded_images[self.curr]

        if self.mode == "masked":
            mask, result = get_mask(image) ## apply mask
            self.ax.imshow(image)
            self.ax.imshow(mask)
            self.im = self.ax.imshow(result)
        elif self.mode == "scroll":
            self.im = self.ax.imshow(image)

        self.fig.canvas.mpl_connect("key_press_event", self.next_image)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--imagedir', action="store", dest='imagedir', default='')
    parser.add_argument('--mode', action="store", dest='mode', default='scroll')

    args = parser.parse_args()

    images = Images(args.imagedir, args.mode)

    images.display()

