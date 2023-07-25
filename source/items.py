from abc import ABC, abstractmethod
from typing import Type


class Item(ABC):
    def __init__(self, name: str, image):
        self.name = name
        self.image = image


class InteractionObject(ABC):
    @abstractmethod
    def interact(self):
        pass


Door: InteractionObject = Type['Door']


class KeyItem(Item):
    parent: Door
    
    def __init__(self, name, image, parent: Door) -> None:
        super(KeyItem, self).__init__(name, image)
        self.set_parent(parent)
    
    def set_parent(self, door: Door):
        self.parent = door
