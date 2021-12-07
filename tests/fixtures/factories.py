import pytest

from modules.builders.knob_builder import KnobStripBuilder
from modules.builders.strip_builder import StripBuilder


@pytest.fixture
def strip_builder_factory(led_images):
    def new(direction="horizontal"):
        return StripBuilder(images=led_images, direction=direction).build()

    return new


@pytest.fixture
def knob_strip_builder_factory(test_knob_image):
    def new(direction="vertical", rotation="clockwise"):
        return KnobStripBuilder(
            knob_image=test_knob_image,
            direction=direction,
            rotation=rotation,
        ).build()

    return new
