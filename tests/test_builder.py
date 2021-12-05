import attr
import pytest

from pathlib import Path
from PIL import Image


from modules.builder import KnobStripBuilder, StripBuilder
from modules.entities.strip import StripDirection
from modules.entities.knob import Knob, KnobRotation

@pytest.fixture
def led_images():
    return [
        Image.open(p) for p in ("./data/led_off.png", "./data/led_on.png")
    ]

@pytest.fixture
def test_knob():
    return Knob(
        image=Image.open(str(Path("./data/knob.png").absolute())),
    )

def test_strip_builder(led_images):
    test_result_file_path = "./data/test_led_horizontal.png"
    sb = StripBuilder(
        items=led_images,
        direction=StripDirection.HORIZONTAL
    )
    res = sb.build()
    sb.save(res.image, file_path=test_result_file_path)
    assert attr.asdict(res.metadata) == {
        "direction": StripDirection.HORIZONTAL,
        "file_paths": [
            "/home/thealchemist/dev/python/knobby/data/led_off.png",
            "/home/thealchemist/dev/python/knobby/data/led_on.png",
        ],
        "frames_count": 2
    }
    assert Path(test_result_file_path).is_file()

def test_knob_strip_builder(test_knob):
    test_result_file_path = "./data/test_led_horizontal.png"

    sb = KnobStripBuilder(
        knob=test_knob
    )
    res = sb.build()
    sb.save(res.image, file_path=test_result_file_path)
    assert attr.asdict(res.metadata) == {
        "rotation": KnobRotation.CLOCKWISE,
        "direction": StripDirection.VERTICAL,
        "file_paths": [
            "/home/thealchemist/dev/python/knobby/data/knob.png",
        ],
        "frames_count": 27
    }
    assert Path(test_result_file_path).is_file()