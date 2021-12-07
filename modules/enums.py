from enum import Enum


class ArgumentHandledEnum(Enum):
    """
    Перечисление, позволяющее парсить значение, пришедшее из строкового аргумента
    """

    @classmethod
    def from_argument(cls, argument: str):
        """
        Парсинг значения из строкового аргумента.

        Args:
            `argument: str` - строковый аргумент
        """
        return cls[argument.upper()]
