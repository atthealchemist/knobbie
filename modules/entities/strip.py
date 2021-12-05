import attr

from typing import List, Tuple

from PIL import Image  # PIL.Image object
from PIL.Image import Image as PILImage  # PIL.Image typing

from modules.enums import ArgumentHandledEnum


class StripDirection(ArgumentHandledEnum):
    """
    Направление стрипа. Может быть вертикальным (vertical) и горизонтальным (horizontal)
    """
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"

    def __str__(self) -> str:
        return self.value


@attr.s(auto_attribs=True)
class Strip:
    """
    Стрип - изображение с покадровым представлением кадров на нём

    Attributes:
        `direction: StripDirection - направление стрипа`
        `image: Image` - объект `PIL.Image` сгенерированного стрипа
    """
    direction: StripDirection = StripDirection.VERTICAL
    image: Image = None

    def _compute_size(self, items: List[PILImage]) -> Tuple[int, int]:
        """
        Функция вычисляет размер изображения сгенерированного стрипа.

        Расчёт производится на основе размера самого большого изображения в наборе.

        Args:
            `items: List[PILImage]` - набор изображений, из которых будет сгенерирован стрип

        Returns:
            `Tuple(int, int)` - кортеж со значениями ширины и высоты будущего стрипа.
        """
        items_count = len(items)
        max_sized_item = max(items, key=lambda i: i.size)
        width, height = max_sized_item.size
        return {
            "vertical": (width, height * items_count),
            "horizontal": (width * items_count, height)
        }.get(self.direction.value)
            
    def fill(self, items: List[PILImage]) -> None:
        """
        Функция создаёт стрип и заполняет его изображениями из переданного набора.

        Args:
            `items: List[PILImage]` - набор изображений, из которых будет сгенерирован стрип.
        """
        strip_image = Image.new(
            "RGBA", 
            size=self._compute_size(items)
        )
        for idx, frame in enumerate(items):
            width, height = frame.size
            directions = {
                "vertical": (0, height * idx),
                "horizontal": (width * idx, 0)
            }
            strip_image.paste(frame, directions.get(self.direction.value))

        self.image = strip_image