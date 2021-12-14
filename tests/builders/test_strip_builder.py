from pathlib import Path

import attr
import pytest


class TestStripBuilder:
    """Тесты для сборщика стрипа"""

    @pytest.mark.parametrize("direction", ("vertical", "horizontal"))
    def test_strip_builder_create_ok(
        self,
        test_led_file_paths,
        test_led_result_file_path,
        strip_builder_factory,
        direction,
    ):
        """
        Тестируется создание и сохранение стрипа.
        """
        res = strip_builder_factory(direction=direction)
        res.save(file_path=test_led_result_file_path)
        assert res.strip.direction.value == direction
        assert attr.asdict(res.metadata) == {
            "file_paths": test_led_file_paths,
            "frames_count": 2,
            "extra": {},
        }
        assert Path(test_led_result_file_path).is_file()
