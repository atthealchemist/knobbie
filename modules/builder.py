import logging
from pathlib import Path

from typing import List
from PIL.Image import Image
from modules.entities.builder import (
    StripBuilderMetadata, StripBuilderResult, 
    KnobStripBuilderMetadata, KnobStripBuilderResult
)

from modules.entities.knob import Knob
from modules.interfaces.saver import ImageSaverInterface
from modules.interfaces.strip import KnobStripBuilderInterface, StripBuilderInterface
from modules.entities.strip import Strip, StripDirection

class StripBuilder(StripBuilderInterface, ImageSaverInterface):

    def file_paths(self):
        return [str(Path(i.filename).absolute()) for i in self.items]

    def build(self):
        items = self.items

        strip = Strip(direction=self.direction)
        strip.fill(items)

        metadata = StripBuilderMetadata(
            direction=self.direction,
            file_paths=self.file_paths(),
            frames_count=len(items)
        )
        self.logger.info(metadata)
        return StripBuilderResult(
            image=strip.image,
            metadata=metadata
        )
    
    def save(self, image: Image, file_path: str) -> None:
        image.save(file_path)
        self.logger.info(f"Saved strip to '{Path(file_path).absolute()}'")

    def __init__(self, items: List[Image], direction: StripDirection = StripDirection.VERTICAL):
        self.direction = direction
        self.items = items
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)


class KnobStripBuilder(KnobStripBuilderInterface, ImageSaverInterface):
    def __init__(
        self,
        knob: Knob,
        direction: StripDirection = StripDirection.VERTICAL,
    ):
        self.direction = direction
        self.knob = knob
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    
    def process(self) -> List[Image]:
        frames_count = int(self.knob.MAX_ANGLE / self.knob.step)
        angle = 0
        frames = []
        for _ in range(frames_count):
            rotated_knob = self.knob.rotate(angle)
            frames.append(rotated_knob)
            angle += self.knob.step
        return frames
    
    def build(self) -> Strip:
        frames = self.process()
        frames_count = len(frames)

        strip = Strip(direction=self.direction)
        strip.fill(frames)
        
        metadata = KnobStripBuilderMetadata(
            direction=self.direction,
            file_paths=[self.knob.image.filename],
            frames_count=frames_count,
            rotation=self.knob.rotation
        )
        self.logger.info(metadata)
        return KnobStripBuilderResult(
            image=strip.image,
            metadata=metadata
        )
    
    def save(self, image: Image, file_path: str) -> None:
        image.save(file_path)
        self.logger.info(f"Saved strip to '{Path(file_path).absolute()}'")
