import sys

import mido

from midi_image_selector.src.image_tools import *

def get_midi_port():
    # Get a list of available input port names
    input_ports = mido.get_input_names()

    # Get first port that is not a Through type
    for p in input_ports:
        if "Midi Through" not in p:
            port = p
            return p

    if not input_ports or not p: 
        raise Exception("No MIDI input ports found.")

class MIDI_Images():
    def __init__(
        self, 
        path=".", 
        mode="scroll", 
        auto_start=True
    ):
        self.path = path
        self.loaded_images = get_images(self.path)
        self.curr = 0
        self.mode = mode
        if auto_start:
            self.fig, self.ax = plt.subplots()
            self.display()
            plt.get_current_fig_manager().full_screen_toggle()
            plt.show()
            
            try:
                p = get_midi_port()

                with mido.open_input(p) as inport:
                    inport.poll()
                    print(f"Listening for MIDI messages on port: {inport.name}")
                    while True:
                        for msg in inport.iter_pending():
                            print(msg)
                            self.curr = msg.note
                            self.update_image()

            except Exception as e:
                print(f"Error: {e}")

    def update_image(self):
        """
        Load in next image
        """

        # do something with current image
        try:
            n = int(msg.note)
            print("You pressed {}".format(n))
        except ValueError:
            print("Sorry can only use MIDI notes")

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

            # self.fig.canvas.mpl_connect("key_press_event", self.next_image)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--imagedir', action="store", dest='imagedir', default='')
    parser.add_argument('--mode', action="store", dest='mode', default='scroll')

    args = parser.parse_args()

    # MIDI_Images(args.imagedir, args.mode)
    MIDI_Images("/home/schoolsofthought/Desktop/rpi/midi_image_selector/sample_images/", "scroll")