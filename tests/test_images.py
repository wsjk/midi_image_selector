import pytest
import sys
sys.path.append("../src/")
from ..src.images import *

@pytest.fixture(scope="function")
def shared_instance():
    instance = Images("./sample_images","scroll", False)
    yield instance

def test_image_load(shared_instance):
    assert len(shared_instance.loaded_images) == 3
