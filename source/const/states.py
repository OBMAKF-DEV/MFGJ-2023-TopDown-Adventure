from enum import Enum


class GameState(Enum):
    NONE = 0
    RUNNING = 1
    ENDED = 2
    GAME_OVER = 3
    SUSPENDED = 4
    OPEN_MENU = 5
    MAIN_MENU = 6
    DIALOG_OPEN = 7


class ContainerState(Enum):
    CLOSED = 0
    OPEN = 1


class EntityState(Enum):
    DEAD = 0
    ALIVE = 1


class DialogState(Enum):
    NONE = 0
    IN_DIALOG = 1


class DoorState(Enum):
    LOCKED = 0
    UNLOCKED = 1


class MenuState(Enum):
    CLOSED = 0
    OPENED = 1
