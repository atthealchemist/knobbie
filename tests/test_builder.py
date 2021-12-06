import attr
import pytest

from pathlib import Path
from PIL import Image


from modules.builder import KnobStripBuilder, StripBuilder
from modules.entities.strip import StripDirection
from modules.entities.knob import Knob, KnobRotation

from constants import DATA_DIR
test_knob_file_path = f"{DATA_DIR}/knob.png"
test_led_file_paths = [
    f"{DATA_DIR}/led_off.png",
    f"{DATA_DIR}/led_on.png",
]
test_result_file_path = f"{DATA_DIR}/test_led_horizontal.png"

@pytest.fixture
def led_images():
    return [
        Image.open(p) for p in test_led_file_paths
    ]

@pytest.fixture
def test_knob():
    return Knob(image=Image.open(test_knob_file_path))


def test_strip_builder(led_images):
    sb = StripBuilder(direction=StripDirection.HORIZONTAL)
    res = sb.build(
        items=led_images
    )
    sb.save(res.image, file_path=test_result_file_path)
    assert attr.asdict(res.metadata) == {
        "direction": StripDirection.HORIZONTAL,
        "file_paths": test_led_file_paths,
        "frames_count": 2,
        "extra": {}
    }
    assert Path(test_result_file_path).is_file()

def test_knob_strip_builder(test_knob):
    sb = KnobStripBuilder(
        knob=test_knob
    )
    res = sb.build(
        items=[test_knob.image]
    )
    sb.save(res.image, file_path=test_result_file_path)
    assert attr.asdict(res.metadata) == {
        "extra": {
            "rotation": KnobRotation.CLOCKWISE
        },
        "direction": StripDirection.VERTICAL,
        "file_paths": [
            test_knob_file_path
        ],
        "frames_count": 27
    }
    assert Path(test_result_file_path).is_file()