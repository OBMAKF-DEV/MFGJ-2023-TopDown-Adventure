from enum import Enum


class Directions(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


def north(position: tuple[int, int]) -> tuple[int, int]:
    x, y = position
    return x, y - 1


def south(position: tuple[int, int]) -> tuple[int, int]:
    x, y = position
    return x, y + 1


def west(position: tuple[int, int]) -> tuple[int, int]:
    x, y = position
    return x - 1, y


def east(position: tuple[int, int]) -> tuple[int, int]:
    x, y = position
    return x + 1, y
