from enum import Enum


class GameState(Enum):
    NONE = 0
    RUNNING = 1
    ENDED = 2
    GAME_OVER = 3
    SUSPENDED = 4
    OPEN_MENU = 5


class ContainerState(Enum):
    CLOSED = 0
    OPEN = 1


class EntityState(Enum):
    DEAD = 0
    ALIVE = 1


class DoorState(Enum):
    LOCKED = 0
    UNLOCKED = 1
