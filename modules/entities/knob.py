from typing import Tuple
import attr

from PIL.Image import Image as PILImage

from modules.enums import ArgumentHandledEnum

class KnobRotation(ArgumentHandledEnum):
    """
    Направление поворота кнопки. 
    Может быть по часовой стрелке (clockwise) и против часовой стрелки (counterclockwise).
    """
    CLOCKWISE = -1
    COUNTERCLOCKWISE = 1

    def __str__(self) -> str:
        return self.name.lower()

@attr.s(auto_attribs=True, frozen=True)
class Knob:
    """
    Knob - поворотная ручка на каком-нибудь устройстве (например, гитарная педаль).

    Attributes:
        `image: PILImage` - изображение кноба.
        `step: int` - шаг угла, на который будет повёрнуто каждое следующее изображение.
        `rotation: KnobRotation` - направление поворота кноба.
    """
    image: PILImage
    step: int = 10
    rotation: KnobRotation = KnobRotation.CLOCKWISE

    MAX_ANGLE: int = 270

    @property
    def size(self) -> Tuple[int, int]:
        """
        Размер изображения - кортеж (ширина, высота)
        """
        return self.image.size
    
    def rotate(self, angle: int) -> PILImage:
        """
        Функция возвращает новый кноб, повёрнутый на указанное количество градусов.
        Направление поворота (по/против часовой стрелки) функцией уже учитывается.

        Args:
            `angle: int` - количество градусов, на которое кноб будет повёрнут
        """
        return self.image.rotate(angle * self.rotation.value)