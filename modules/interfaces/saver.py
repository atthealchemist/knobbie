from abc import ABCMeta, abstractmethod
from PIL.Image import Image

class ImageSaverInterface(metaclass=ABCMeta):
    
    @abstractmethod
    def save(self, image: Image, file_path: str) -> None:
        """
        Функция сохраняет PIL.Image по указанному пути.

        Args:
            `image: Image` - объект PIL.Image
            `file_path: str` - путь, куда будет сохранено изображение
        """

