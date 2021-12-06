import attr
import pytest

from pathlib import Path
from PIL import Image


from modules.builder import KnobStripBuilder, StripBuilder
from modules.entities.strip import StripDirection
from modules.entities.knob import Knob, KnobRotation

PROJECT_ROOT = ROOT = str(Path(__file__).parent.parent.absolute())


@pytest.fixture
def led_images():
    return [
        Image.open(p) for p in (f"{ROOT}/data/led_off.png", f"{ROOT}/data/led_on.png")
    ]

@pytest.fixture
def test_knob():
    return Knob(
        image=Image.open(str(Path(f"{ROOT}/data/knob.png").absolute())),
    )


def test_strip_builder(led_images):
    test_result_file_path = f"{ROOT}/data/test_led_horizontal.png"
    sb = StripBuilder(direction=StripDirection.HORIZONTAL)
    res = sb.build(
        items=led_images
    )
    sb.save(res.image, file_path=test_result_file_path)
    assert attr.asdict(res.metadata) == {
        "direction": StripDirection.HORIZONTAL,
        "file_paths": [
            f"{ROOT}/data/led_off.png",
            f"{ROOT}/data/led_on.png",
        ],
        "frames_count": 2,
        "extra": {}
    }
    assert Path(test_result_file_path).is_file()

def test_knob_strip_builder(test_knob):
    test_result_file_path = f"{ROOT}/data/test_led_horizontal.png"

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
            f"{ROOT}/data/knob.png",
        ],
        "frames_count": 27
    }
    assert Path(test_result_file_path).is_file()