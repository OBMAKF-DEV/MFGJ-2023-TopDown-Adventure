from abc import ABC, abstractmethod
from typing import Type


class Item(ABC):
    """
    Base class for all in-game items.
    
    Args:
        name (str): The name of the item.
        image (str | bytes): The image to be displayed for the item.
    """
    def __init__(self, name: str, image):
        self.name = name
        self.image = image


class InteractionObject(ABC):
    """
    Base class for any intractable in-game item.
    """
    @abstractmethod
    def interact(self):
        """
        Abstract method determining what happens when the player interacts with the item.
        """
        pass


Door: InteractionObject = Type['Door']


class KeyItem(Item):
    """
    Key item for unlocking doors.
    
    Attributes:
        parent (Door): The door that the key unlocks.
    """
    parent: Door
    
    def __init__(self, name, image, parent: Door) -> None:
        super(KeyItem, self).__init__(name, image)
        self.set_parent(parent)
    
    def set_parent(self, door: Door):
        """
        Sets the parent of the key.
        
        Args:
            door (Door): The door for the key to unlock.
        """
        self.parent = door
