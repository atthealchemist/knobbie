#/usr/bin/env python

import logging

from modules.builder import KnobStripBuilder
from modules.entities.knob import Knob, KnobRotation
from modules.entities.strip import StripDirection
logging.basicConfig(level=logging.INFO)

from PIL import Image
from pathlib import Path
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--path", 
        action="store", 
        help="Path to knob file"
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

    knob_path = Path(args.path)
    knob = Knob(
        image=Image.open(str(knob_path.absolute())),
        rotation=KnobRotation.from_argument(args.rotation)
    )
    knob_strip_builder = KnobStripBuilder(
        knob=knob,
        direction=StripDirection.from_argument(args.direction)
    )
    knob_strip = knob_strip_builder.build()
    knob_strip_builder.save(
        image=knob_strip.image,
        file_path=knob_path.parent / f"{Path(args.output).stem}_{knob_strip.metadata.direction}_{knob_strip.metadata.rotation}{knob_path.suffix}"
    )

if __name__ == "__main__":
    main()