from pathlib import Path

import attr
import pytest


class TestKnobStripBuilder:
    """
    Тесты для сборки кноб стрипа.
    """

    @pytest.mark.parametrize("direction", ("vertical", "horizontal"))
    @pytest.mark.parametrize("rotation", ("clockwise", "counterclockwise"))
    def test_knob_strip_builder_create_ok(
        self,
        knob_strip_builder_factory,
        test_knob_file_path,
        test_knob_result_file_path,
        direction,
        rotation,
    ):
        """
        Проверяем, что сборщик успешно собирает и сохраняет в файл кноб стрип.
        """
        res = knob_strip_builder_factory(
            direction=direction,
            rotation=rotation,
        )
        res.save(file_path=test_knob_result_file_path)
        assert res.strip.direction.value == direction
        assert attr.asdict(res.metadata) == {
            "extra": {"rotation": rotation},
            "file_paths": [test_knob_file_path],
            "frames_count": 27,
        }
        assert Path(test_knob_result_file_path).is_file()
