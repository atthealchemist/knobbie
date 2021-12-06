from enum import Enum


class ArgumentHandledEnum(Enum):
    @classmethod
    def from_argument(cls, argument):
        return cls[argument.upper()]
