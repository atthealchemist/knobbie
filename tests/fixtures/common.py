import pytest
from PIL import Image

from constants import DATA_DIR


@pytest.fixture
def test_knob_file_path():
    return f"{DATA_DIR}/knob.png"


@pytest.fixture
def test_led_file_paths():
    return [
        f"{DATA_DIR}/led_off.png",
        f"{DATA_DIR}/led_on.png",
    ]


@pytest.fixture
def test_led_result_file_path():
    return f"{DATA_DIR}/test_led_horizontal.png"


@pytest.fixture
def test_knob_result_file_path():
    return f"{DATA_DIR}/test_knob_horizontal.png"


@pytest.fixture
def led_images(test_led_file_paths):
    """
    Фикстура создаёт набор тестовых изображений (объекты PIL.Image)
    из путей тестовых файлов с изображением включенного светодиода
    (led_on) и выключенного светодиода (led_off).
    """
    return [Image.open(led_path) for led_path in test_led_file_paths]


@pytest.fixture
def test_knob_image(test_knob_file_path):
    """
    Фикстура создаёт тестовое изображение (объект PIL.Image)
    из пути тестового файла с изображением ручки (knob).
    """
    return Image.open(test_knob_file_path)
