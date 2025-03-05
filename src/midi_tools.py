import threading
import mido

from image_tools import *

midi_notes = [i for i in range(24,37)]

def get_midi_port():
    # Get a list of available input port names
    input_ports = mido.get_input_names()

    # Get first port that is not a Through type
    for p in input_ports:
        if "Midi Through" not in p:
            print(p)
            port = p
            return p

    if not input_ports or not p: 
        raise Exception("No MIDI input ports found.")

def midi_to_note(max_num, midi_number):
    """Converts a MIDI note number to its musical note representation."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = midi_number // 12 - 1
    note_index = midi_number % 12
    if note_index >= max_num:
        note_index = max_num - note_index
    return note_index, notes[note_index] + str(octave)