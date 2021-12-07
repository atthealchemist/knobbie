from main import parse_args


class TestMain:
    """
    Тесты для main функции. Тестируем обработку ввода из консоли.
    """

    def test_parse_args_for_strip_builder(
        self, test_led_file_paths, test_led_result_file_path
    ):
        """
        Тестируем парсинг аргументов для сборки стрипа.
        """
        test_strip_builder_cli_args = [
            "strip",
            "-d",
            "horizontal",
            "-o",
            test_led_result_file_path,
            "-p",
            *test_led_file_paths,
        ]
        parsed_args = parse_args(test_strip_builder_cli_args)
        assert vars(parsed_args) == {
            "type": "strip",
            "paths": test_led_file_paths,
            "direction": "horizontal",
            "output": test_led_result_file_path,
            "rotation": None,
        }

    def test_parse_args_for_knob_strip_builder(
        self, test_knob_file_path, test_knob_result_file_path
    ):
        """
        Тестируем парсинг аргументов для сборки кноб стрипа.
        """
        test_strip_builder_cli_args = [
            "knob",
            "-d",
            "vertical",
            "-o",
            test_knob_result_file_path,
            "-p",
            test_knob_file_path,
            "-r",
            "clockwise",
        ]
        parsed_args = parse_args(test_strip_builder_cli_args)
        assert vars(parsed_args) == {
            "type": "knob",
            "paths": [test_knob_file_path],
            "direction": "vertical",
            "output": test_knob_result_file_path,
            "rotation": "clockwise",
        }
