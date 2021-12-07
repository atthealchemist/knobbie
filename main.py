# /usr/bin/env python

import logging
from argparse import ArgumentParser

from PIL import Image

from modules.builders.knob_builder import KnobStripBuilder
from modules.builders.strip_builder import StripBuilder

logging.basicConfig(level=logging.INFO)


def parse_args(args=None):
    """
    Функция парсит аргументы командной строки, используя argparse.ArgumentParser.
    """
    parser = ArgumentParser()

    parser.add_argument(
        "type",
        help="Type of builder (strip or knob)",
        default="strip",
    )
    parser.add_argument(
        "-p",
        "--paths",
        nargs="+",
        help="Path(s) to build strip/knob file(s)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="knob_strip.png",
        help="Output file name",
    )
    parser.add_argument(
        "-d",
        "--direction",
        default="vertical",
        help="Direction of strip - vertical (default) or horizontal",
    )
    parser.add_argument(
        "-r",
        "--rotation",
        default=None,
        help="Rotation direction - clockwise or counterclockwise",
    )

    return parser.parse_args(args)


def get_builder(args):
    """
    Функция получает конкретного сборщика из аргументов командной строки,
    переданных программе.

    Args:
        `args` - список аргументов командной строки
    """
    builder_cls = {"strip": StripBuilder, "knob": KnobStripBuilder}.get(args.type)
    builder_args = {
        "direction": args.direction,
        "items": [Image.open(path) for path in args.paths],
    }
    if args.type == "knob":
        image, *_ = builder_args.pop("items")
        builder_args["knob_image"] = image
        builder_args["rotation"] = args.rotation

    return builder_cls(**builder_args)


def main():
    """
    Главная функция для работы в CLI режиме.
    """
    args = parse_args()

    builder = get_builder(args)
    strip_result = builder.build()
    strip_result.save(
        file_path="{output}_{direction}_{rotation}.png".format(
            output=args.output,
            direction=strip_result.strip.direction,
            rotation=strip_result.metadata.extra.get("rotation"),
        ),
    )


if __name__ == "__main__":
    main()
