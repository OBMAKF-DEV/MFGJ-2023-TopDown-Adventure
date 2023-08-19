from enum import Enum


class GameState(Enum):
    """
    Enumerator containing all the different game flags.
    Indicates what state the game should run.
    """
    NONE = 0
    RUNNING = 1
    ENDED = 2
    GAME_OVER = 3
    SUSPENDED = 4
    OPEN_MENU = 5
    MAIN_MENU = 6
    DIALOG_OPEN = 7


class ContainerState(Enum):
    """
    Enumerator containing the different flags for a container.
    """
    CLOSED = 0
    OPEN = 1


class EntityState(Enum):
    """
    Enumerator containing the different flags for an Entity.
    """
    DEAD = 0
    ALIVE = 1


class NPCState(Enum):
    """
    Enumerator containing the different flags for NPC's.
    """
    NONE = 0
    OPEN_INVENTORY = 1


class DialogState(Enum):
    """
    Enumerator containing the different flags for dialogs.
    """
    NONE = 0
    IN_DIALOG = 1


class DoorState(Enum):
    """
    Enumerator containing the different states for a doors accessability.
    """
    LOCKED = 0
    UNLOCKED = 1


class MenuState(Enum):
    """
    Enumerator containing the different states for the main menu.
    """
    CLOSED = 0
    OPENED = 1
    LOAD = 2
    SAVE = 3
    CREATE_SAVE = 4
