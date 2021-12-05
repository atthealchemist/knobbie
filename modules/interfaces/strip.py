from abc import ABCMeta, abstractmethod

from typing import List

from PIL.Image import Image

from modules.entities.builder import KnobStripBuilderResult, StripBuilderResult


class StripBuilderInterface(metaclass=ABCMeta):
    """
    Интерфейс, использующийся для построения стрипа.

    Methods:
        `build(self) -> StripBuilderResult` - генерация стрипа
    """
    
    @abstractmethod
    def build(self) -> StripBuilderResult:
        """
        Функция генерирует стрип

        Returns: `StripBuilderResult`
        """

class KnobStripBuilderInterface(StripBuilderInterface):

    @abstractmethod
    def build(self) -> KnobStripBuilderResult:
        """
        Функция генерирует стрип для кноба (полоску png для анимации кноба)

        Returns: `KnobStripBuilderResult`
        """

    @abstractmethod
    def process(self) -> List[Image]:
        """
        Функция выполняет необходимые преобразования с кнобом 
        (в данном случае используется для покадрового поворота кноба)

        Returns:
            `List[PIL.Image]` - Список преобразованных фреймов
        """