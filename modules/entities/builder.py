import logging
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Dict, List, Union

import attr

from modules.entities.strip import Strip


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

    def to_dict(self):
        """
        Функция преобразует объект метадаты в словарь.
        """
        return attr.asdict(self)


class StripBuilderResultSaverInterface(metaclass=ABCMeta):
    """
    Сохранение результата сборки стрипа
    """

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
        """
        Создаёт логгер, соответствующий имени текущего класса.
        """
        return logging.getLogger(self.__class__.__name__)

    def __str__(self) -> str:
        file_paths_str = ", ".join([str(path) for path in self.metadata.file_paths])
        return "Successfully built new {direction} strip from '{paths}' on {frames_count} frames".format(
            direction=self.strip.direction,
            paths=file_paths_str,
            frames_count=self.metadata.frames_count,
        )

    def save(self, file_path: Union[str, Path]) -> None:
        """
        Функция сохраняет результат сборки стрипа в файл по указанному пути.

        Args:
            `file_path: Union[str, Path]` - по какому пути будет сохранён файл.
        """
        self.strip.image.save(file_path)
        self.logger.info(f"Saved strip to '{file_path}'")
