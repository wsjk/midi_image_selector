import threading
import matplotlib
matplotlib.use('TkAgg')  # Or another suitable backend like 'QtAgg'
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import mido

from image_tools import *
from midi_tools import *

min_note = 24

class MIDI_Images():
    def __init__(
        self, 
        path=".", 
        mode="scroll", 
        full_screen=False,
        auto_start=True,
        verbose=False
    ):
        self.path = path
        self.loaded_images = get_images(self.path)
        self.num_images = len(self.loaded_images)
        self.curr = 0
        self.mode = mode
        self.full_screen = full_screen
        self.verbose = verbose
        if auto_start:
            self.create_window()
            
    def create_window(self):
        self.fig, self.ax = plt.subplots()
        self.display()
        if self.full_screen:
            plt.get_current_fig_manager().full_screen_toggle()
        self.display()
        threading.Thread(target=self.poll_midi, daemon=1).start()
        plt.show()  # use blocking show()

    def poll_midi(self):
        try:
            p = get_midi_port()
            with mido.open_input(p) as inport:
                inport.poll()
                print(f"Listening for MIDI messages on port: {inport.name}")
                while True:
                    for msg in inport.iter_pending():
                        if self.verbose:
                            print("MIDI message: ", msg)
                        self.curr = midi_note_to_index(self.num_images, min_note, msg.note)
                        if self.verbose:
                            print("image index: ", self.curr)
                        self.update_image()
        except Exception as e:
            print(f"Error: {e}")

    def update_image(self):
        """
        Load in next image
        """

        # advance to next image
        try:
            # self.curr = n
            self.im.set_array(self.loaded_images[self.curr])
            self.display()
            # self.fig.canvas.draw_idle()
        except IndexError:
            print("Sorry no image in index: ", self.curr)

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

            plt.draw()



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--imagedir', action="store", dest='imagedir', default='')
    parser.add_argument('--mode', action="store", dest='mode', default='scroll')
    parser.add_argument('--autostart', action=argparse.BooleanOptionalAction)
    parser.add_argument('--fullscreen', action=argparse.BooleanOptionalAction)
    parser.add_argument('--verbose', action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    MIDI_Images(args.imagedir, args.mode, args.fullscreen, args.autostart, args.verbose)