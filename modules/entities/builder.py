import attr
import logging

from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Dict, List, Union

from .strip import Strip


@attr.s(frozen=True, auto_attribs=True)
class StripBuilderMetadata:
    """
    Данные, использованные при построении стрипа

    Attributes:
        `frames_count: int` - количество кадров в стрипе.
        `file_paths: List[str]` - путь к исходным файлам, из которых был построен стрип.
        `extra: Dict` - дополнительная информация о построении стрипа
    """
    frames_count: int
    file_paths: List[str] = []
    extra: Dict = {}

class StripBuilderResultSaverInterface(metaclass=ABCMeta):
    
    @abstractmethod
    def save(self, file_path: str) -> None:
        """
        Функция сохраняет `StripBuilderResult` по указанному пути.

        Args:
            `file_path: str` - путь, куда будет сохранено изображение
        """


@attr.s(frozen=True, auto_attribs=True)
class StripBuilderResult(StripBuilderResultSaverInterface):
    """
    Результат построения стрипа

    Attributes:
        `strip: Strip` - готовый стрип
        `metadata: StripBuilderMetadata` - данные, использованные при пострроении стрипа
    """
    strip: Strip
    metadata: StripBuilderMetadata
    
    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(self.__class__.__name__)
    
    def __str__(self) -> str:
        file_paths_str = ', '.join([str(p) for p in self.metadata.file_paths])
        return f"""Successfully built new {self.strip.direction} strip
        from '{file_paths_str}' on {self.metadata.frames_count} frames""".strip()

    def save(self, file_path: Union[str, Path]) -> None:
        self.strip.image.save(file_path)
        self.logger.info(f"Saved strip to '{Path(file_path).absolute()}'")
