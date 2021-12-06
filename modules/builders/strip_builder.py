import logging
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import List

from PIL.Image import Image

from modules.entities.builder import StripBuilderMetadata, StripBuilderResult
from modules.entities.strip import Strip, StripDirection


class StripBuilderInterface(metaclass=ABCMeta):
    """
    Интерфейс, использующийся для построения стрипа.
    """

    @abstractmethod
    def process(self) -> None:
        """
        Функция выполняет необходимые преобразования с изображениями, переданными при инициализации билдера

        Returns: `None`
        """

    @abstractmethod
    def build(self) -> StripBuilderResult:
        """
        Функция генерирует стрип из изображений, переданных при инициализации билдера.

        Returns: `StripBuilderResult`
        """


class StripBuilder(StripBuilderInterface):
    """
    Создание стрипа.
    """

    def file_paths(self) -> List[str]:
        """
        Функция возвращает список путей к файлам изображений в стрипе

        Returns:
            `List[str]` - список путей к файлам изображений в стрипе
        """
        return [str(Path(i.filename).absolute()) for i in self.items]

    def process(self) -> None:
        pass

    def build(self) -> StripBuilderResult:
        file_paths = self.file_paths()
        self.process()

        strip = Strip(direction=self.direction)
        strip.fill(items=self.items)

        result = StripBuilderResult(
            strip=strip,
            metadata=StripBuilderMetadata(
                file_paths=file_paths, frames_count=len(self.items)
            ),
        )
        return result

    def __init__(self, items: List[Image], direction: str):
        self.items = items
        self.direction = StripDirection.from_argument(direction)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
