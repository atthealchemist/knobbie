from typing import List, Tuple

import attr
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

    def fill(self, images: List[PILImage]) -> None:
        """
        Функция создаёт стрип и заполняет его изображениями из переданного набора.

        Args:
            `items: List[PILImage]` - набор изображений, из которых будет сгенерирован стрип.
        """
        strip_image = Image.new("RGBA", size=self._compute_size(images))
        for idx, frame in enumerate(images):
            width, height = frame.size
            if self.direction == StripDirection.VERTICAL:
                width, height = 0, height * idx
            if self.direction == StripDirection.HORIZONTAL:
                width, height = width * idx, 0
            strip_image.paste(frame, (width, height))

        self.image = strip_image

    def _compute_size(self, images: List[PILImage]) -> Tuple[int, int]:
        """
        Функция вычисляет размер изображения сгенерированного стрипа.

        Расчёт производится на основе размера самого большого изображения в наборе.

        Args:
            `items: List[PILImage]` - набор изображений, из которых будет сгенерирован стрип

        Returns:
            `Tuple(int, int)` - кортеж со значениями ширины и высоты будущего стрипа.
        """
        items_count = len(images)
        max_sized_image = max(images, key=lambda image: image.size)
        width, height = max_sized_image.size
        if self.direction == StripDirection.HORIZONTAL:
            return (width * items_count, height)
        return (width, height * items_count)
