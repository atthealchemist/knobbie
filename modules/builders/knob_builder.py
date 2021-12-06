from PIL.Image import Image
from modules.entities.builder import StripBuilderResult

from modules.entities.knob import Knob, KnobRotation
from modules.entities.strip import StripDirection

from .strip_builder import StripBuilder


class KnobStripBuilder(StripBuilder):
    def __init__(
        self,
        knob_image: Image,
        direction: str,
        rotation: str
    ):
        self.knob = Knob(
            image=knob_image,
            rotation=KnobRotation.from_argument(rotation)
        )
        
        super().__init__(
            items=[knob_image],
            direction=direction
        )
    
    def process(self) -> None:
        frames_count = int(self.knob.MAX_ANGLE / self.knob.step)
        angle = 0
        frames = []
        for item in self.items:
            for _ in range(frames_count):
                rotated_knob = item.rotate(angle * self.knob.rotation.value)
                frames.append(rotated_knob)
                angle += self.knob.step
        self.items = frames
    
    def build(self) -> StripBuilderResult:
        """
        Функция генерирует кноб стрип.

        Returns: `StripBuilderResult`
        """
        result = super().build()
        result.metadata.extra['rotation'] = self.knob.rotation
        return result
