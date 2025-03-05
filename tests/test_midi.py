import pytest
import sys
sys.path.append("../src/")
from ..src.midi import *

@pytest.fixture(scope="function")
def shared_instance():
    instance = MIDI_Images("./sample_images","scroll", False, False)
    yield instance

def test_image_load(shared_instance):
    assert len(shared_instance.loaded_images) == 3
