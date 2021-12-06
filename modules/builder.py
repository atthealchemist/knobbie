import logging
from pathlib import Path

from typing import List
from PIL.Image import Image
from modules.entities.builder import (
    StripBuilderMetadata, StripBuilderResult
)

from modules.entities.knob import Knob
from modules.interfaces.saver import ImageSaverInterface
from modules.interfaces.strip import StripBuilderInterface
from modules.entities.strip import Strip, StripDirection

class StripBuilder(StripBuilderInterface, ImageSaverInterface):
    """
    Создание стрипа.
    """

    def file_paths(self, items: List[Image]) -> List[str]:
        """
        Функция возвращает список путей к файлам изображений в стрипе

        Args:
            `items: List[PIL.Image]` - набор файлов изображений для стрипа
        
        Returns:
            `List[str]` - список путей к файлам изображений в стрипе
        """
        return [str(Path(i.filename).absolute()) for i in items]
    
    def process(self, items: List[Image]) -> List[Image]:
        return items

    def build(self, items: List[Image]) -> StripBuilderResult:
        file_paths = self.file_paths(items)
        items = self.process(items)

        strip = Strip(direction=self.direction)
        strip.fill(items)

        metadata = StripBuilderMetadata(
            direction=self.direction,
            file_paths=file_paths,
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

    def __init__(self, direction: StripDirection = StripDirection.VERTICAL):
        self.direction = direction
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)


class KnobStripBuilder(StripBuilder):
    def __init__(
        self,
        knob: Knob,
        direction: StripDirection = StripDirection.VERTICAL,
    ):
        self.knob = knob
        
        super().__init__(direction=direction)
    
    def process(self, items: List[Image]) -> List[Image]:
        frames_count = int(self.knob.MAX_ANGLE / self.knob.step)
        angle = 0
        frames = []
        for item in items:
            for _ in range(frames_count):
                rotated_knob = item.rotate(angle * self.knob.rotation.value)
                frames.append(rotated_knob)
                angle += self.knob.step
        return frames
    
    def build(self, items: List[Image]) -> StripBuilderResult:
        result = super().build(items=items)
        result.metadata.extra['rotation'] = self.knob.rotation
        
        self.logger.info(result.metadata)
        return result
