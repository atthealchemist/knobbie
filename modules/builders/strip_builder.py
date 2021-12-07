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
        Функция выполняет необходимые преобразования с изображениями,
        переданными при инициализации билдера

        Returns: `None`
        """

    @abstractmethod
    def build(self) -> StripBuilderResult:
        """
        Функция генерирует стрип из изображений,
        переданных при инициализации билдера.

        Returns: `StripBuilderResult`
        """


class StripBuilder(StripBuilderInterface):
    """
    Создание стрипа.
    """

    def __init__(self, images: List[Image], direction: str):
        """
        Создание стрипа.

        Args:
            `images: List[PIL.Image]` - набор изображений, из которых будет собран стрип.
            `direction: str` - направление стрипа.
            Может быть вертикальным (vertical) и горизонтальным (horizontal).
        """
        self.images = images
        self.direction = StripDirection.from_argument(direction)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

    def process(self) -> None:
        """
        Непосредственно в этой функции никакой обработки изображений стрипа
        не происходит, зато она может быть в сущностях, наследуемых от StripBuilder.
        """

    def build(self) -> StripBuilderResult:
        """
        Функция генерирует стрип из изображений,
        переданных при инициализации билдера.

        Returns: `StripBuilderResult`
        """
        file_paths = self.file_paths()
        self.process()

        strip = Strip(direction=self.direction)
        strip.fill(self.images)

        return StripBuilderResult(
            strip=strip,
            metadata=StripBuilderMetadata(
                file_paths=file_paths,
                frames_count=len(self.images),
            ),
        )

    def file_paths(self) -> List[str]:
        """
        Функция возвращает список путей к файлам изображений в стрипе

        Returns:
            `List[str]` - список путей к файлам изображений в стрипе
        """
        return [str(Path(image.filename).absolute()) for image in self.images]
