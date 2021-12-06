from abc import ABCMeta, abstractmethod

from typing import List

from PIL.Image import Image

from modules.entities.builder import StripBuilderResult


class StripBuilderInterface(metaclass=ABCMeta):
    """
    Интерфейс, использующийся для построения стрипа.

    Methods:
        `build(self) -> StripBuilderResult` - генерация стрипа
    """

    @abstractmethod
    def process(self, items: List[Image]) -> List[Image]:
        """
        Функция выполняет необходимые преобразования с изображениями для стрипа

        Args:
            `items: List[PIL.Image]` - набор изображений для стрипа

        Returns:
            `List[PIL.Image]` - Список преобразованных фреймов
        """
    
    @abstractmethod
    def build(self, items: List[Image]) -> StripBuilderResult:
        """
        Функция генерирует стрип

        Args:
            `items: List[PIL.Image]` - набор изображений для стрипа

        Returns: `StripBuilderResult`
        """
