from PIL.Image import Image

from modules.builders.strip_builder import StripBuilder
from modules.entities.builder import StripBuilderMetadata, StripBuilderResult
from modules.entities.knob import Knob, KnobRotation


class KnobStripBuilder(StripBuilder):
    """Cборщик стрипа кнобов"""

    def __init__(self, knob_image: Image, direction: str, rotation: str):
        """
        Создание стрипа кнобов.

        Args:
            `knob_image: PIL.Image` - изображение кноба
            `direction: str` - направление стрипа. Может быть "horizontal" и "vertical".
            `rotation: str` - направление поворота кнопки. Может быть "clockwise" и "counterclockwise".
        """
        self.knob = Knob(
            image=knob_image,
            rotation=KnobRotation.from_argument(rotation),
        )

        super().__init__(images=[knob_image], direction=direction)

    def process(self) -> None:
        """
        Функция вычисляет количество фреймов для кноба
        и разворачивает кноб в стрипе это самое количество раз.
        """
        frames_count = int(self.knob.max_angle / self.knob.step)
        angle = 0
        frames = []
        for image in self.images:
            for _ in range(frames_count):
                rotated_knob = image.rotate(angle * self.knob.rotation.value)
                frames.append(rotated_knob)
                angle += self.knob.step
        self.images = frames

    def build(self) -> StripBuilderResult:
        """
        Функция генерирует кноб стрип.

        Также мы обновляем метадату для сборки кноб стрипа.

        Returns: `StripBuilderResult`
        """
        build_result = super().build()

        return StripBuilderResult(
            strip=build_result.strip,
            metadata=StripBuilderMetadata(
                **{
                    **build_result.metadata.to_dict(),
                    "extra": {
                        "rotation": str(self.knob.rotation),
                    },
                },
            ),
        )
