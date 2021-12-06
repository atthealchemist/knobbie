#/usr/bin/env python

import logging

from modules.builders.strip_builder import StripBuilder
logging.basicConfig(level=logging.INFO)

from modules.builders import KnobStripBuilder

from PIL import Image
from pathlib import Path
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    
    parser.add_argument(
        "type",
        action="store",
        help="Type of builder (strip or knob)",
        default="strip"
    )
    parser.add_argument(
        "-p", "--paths",
        nargs='+', 
        help="Path(s) to build strip/knob file(s)"
    )
    parser.add_argument(
        "-o", "--output", 
        action="store", 
        default="knob_strip.png", 
        help="Output file name"
    )
    parser.add_argument(
        "-d", "--direction", 
        action="store", 
        default="vertical", 
        help="Direction of strip - vertical (default) or horizontal"
    )
    parser.add_argument(
        "-r", "--rotation",
        action="store",
        default="clockwise",
        help="Rotation direction - clockwise (default) or counterclockwise"
    )

    return parser.parse_args()

def main():
    args = parse_args()

    builder_types = {
        "strip": StripBuilder,
        "knob": KnobStripBuilder
    }

    builder = builder_types.get(args.type)
    builder_args = {
        "direction": args.direction,
        "items": [Image.open(p) for p in args.paths]
    }
    if args.type == "knob":
        image, *_ = builder_args.pop("items")
        builder_args["knob_image"] = image
        builder_args["rotation"] = args.rotation

    b = builder(**builder_args)
    strip_result = b.build()
    strip_result.save(
        file_path=f"{Path(args.output)}_{strip_result.strip.direction}_{strip_result.metadata.extra.get('rotation', '')}.png"
    )

if __name__ == "__main__":
    main()