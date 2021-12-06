from typing import Dict, List
from PIL.Image import Image
import attr

from .strip import StripDirection


@attr.s(frozen=True, auto_attribs=True)
class StripBuilderMetadata:
    """
    Данные, использованные при построении стрипа

    Attributes:
        `frames_count: int` - количество кадров в стрипе.
        `direction: StripDirection` - направление стрипа
        `file_path: str` - путь к исходному файлу, из которого был построен стрип.
    """
    frames_count: int
    direction: StripDirection
    file_paths: List[str] = []
    extra: Dict = {}

    def __str__(self) -> str:
        file_paths_str = ', '.join([str(p) for p in self.file_paths])
        return f"""Successfully built new {self.direction} strip 
        from '{file_paths_str}' on {self.frames_count} frames""".strip()


@attr.s(frozen=True, auto_attribs=True)
class StripBuilderResult:
    """
    Результат построения стрипа

    Attributes:
        `image: Image` - объект типа `PIL.Image`, готовое изображение стрипа.
        `metadata: StripBuilderMetadata` - данные, использованные при пострроении стрипа
    """
    image: Image
    metadata: StripBuilderMetadata


# @attr.s(frozen=True, auto_attribs=True)
# class KnobStripBuilderMetadata(StripBuilderMetadata):
#     """
#     Данные, использованные при построении стрипа для кнобов

#     Attributes:
#         `frames_count: int` - количество кадров в стрипе.
#         `direction: StripDirection` - направление стрипа
#         `file_paths: str` - путь к исходным файлам, из которого был построен стрип.
#         `rotation: KnobRotation` - направление поворота кноба
#     """
#     rotation: KnobRotation = KnobRotation.CLOCKWISE

#     def __str__(self) -> str:
#         return f"{super().__str__()} rotated {self.rotation}"


# @attr.s(frozen=True, auto_attribs=True)
# class KnobStripBuilderResult(StripBuilderResult):
#     """
#     Результат построения стрипа кнобов

#     Attributes:
#         `image: Image` - объект типа `PIL.Image`, готовое изображение стрипа кнобов.
#         `metadata: KnobBuilderMetadata` - данные, использованные при пострроении стрипа кнобов.
#     """
#     metadata: KnobStripBuilderMetadata
