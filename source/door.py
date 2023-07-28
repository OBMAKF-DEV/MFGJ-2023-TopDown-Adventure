import tkinter.messagebox as msg
from source.items import InteractionObject, KeyItem
from source.const.map_objects import OBJECTS
from source.const import DoorState


class Door(InteractionObject):
    """Base `Door` Structure.
    
    Allows the player to travel across into different playable areas.
    
    Note:
        - `state`: The door can be in locked state that requires player to hold the specific paired key to be able to gain access.
    
    Attributes:
        game (Game):                    The base game object.
        location (str | bytes):         The current map file that the player will travel from.
        position (tuple[int, int]):     The coordinates that the door will be rendered at.
        destination (str | bytes):      The map file that the door will take the player.
        key (KeyItem | None):           The paired key that unlocks access to the door -- **default is** ``None.``
        state (Enum | None):            Whether the `Door` is ``UNLOCKED`` or ``LOCKED``.
    """
    def __init__(self, game, location, position: tuple[int, int], destination: str | bytes, spawn: tuple[int, int], key: KeyItem = None, locked: bool = False):
        """Initializes the `Door`.
        
        Args:
            game (Game):                    The base game object.
            location (str | bytes):         The current map file that the player will travel from.
            position (tuple[int, int]):     The coordinates that the door will be rendered at.
            destination (str | bytes):      The map file that the door will take the player.
            key (KeyItem | None):           The paired key that unlocks access to the door -- **default is** ``None.``
            locked (Enum | None):            Whether the `Door` is ``LOCKED`` -- **default is** ``False``.
        """
        self.game = game
        self.location = location
        self.position = position
        self.destination = destination
        self.spawn = spawn
        self.key = key
        self.state = DoorState.LOCKED if locked else DoorState.UNLOCKED
        self.state = DoorState.LOCKED
    
    def interact(self) -> None | str:
        """Gives functionality to interact with the door.
        
        Returns:
            str: If the `Door` is locked and the player doesn't have the key.
            None: If the `Door` is unlocked. (Transports the player to the other map.)
        """
        if self.state == DoorState.LOCKED:
            for item in self.game.player.inventory.items:
                if isinstance(item, KeyItem):
                    if item.name != self.key:
                        continue
                    self.state = DoorState.UNLOCKED
                    return self.interact()
                continue
            return msg.showinfo("Knock Knock...", "The door appears to be locked!")
        
        self.game.map.tiles = []
        self.game.map.load(self.destination)  # Travel to next room.
        self.game.player.position = self.spawn
