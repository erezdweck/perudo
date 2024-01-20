from enum import Enum


class DiceOptions(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    JOKER = 6

    @classmethod
    def values(cls) -> list[int]:
        return [member.value for member in cls.__members__.values()]
