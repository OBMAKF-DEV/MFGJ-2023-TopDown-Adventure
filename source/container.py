import pygame.rect
from source.const import GameState, ContainerState
from source.items import Item, InteractionObject
import tkinter as tk
import tkinter.ttk as ttk
from enum import Enum


class Container(InteractionObject):
    """
    Base Class for any in-game container.
    Provides methodology for viewing and interacting with a container.
    
    Attributes:
        items (list[Item]): The items that are contained within the container.
        state (ContainerState): The current state of the container.
    
    Args:
        game (Game): The main game object.
        items (list[Item] | None): Any items that the container will initialize with.
    """
    items = []
    state = ContainerState.CLOSED
    
    def __init__(self, game, items: list[Item] | None):
        self.game = game
        self.items = []
        if isinstance(items, list):
            self.items = [item for item in items]
    
    def interact(self):
        if self.state == ContainerState.CLOSED:
            return self.open()
    
    def open(self):
        """
        Sets the state of the container as OPEN.
        """
        if self.state == ContainerState.OPEN:
            return
        self.state = ContainerState.OPEN
        self.game.open_container(self)
    
    def close(self):
        """
        Sets the state of the container as CLOSED.
        """
        if self.state == ContainerState.CLOSED:
            return
        self.state = ContainerState.CLOSED
        self.game.close_container(self)
        print('closed')
    
    def take_all(self):
        """
        Takes all the items from the container, appending them to the players inventory.
        """
        for item in self.items:
            self.game.player.inventory.items.append(item)
            self.game.map.remove_object_data(item)
        self.items = []
        self.close()
    
    def __str__(self) -> str:
        return 'Chest'
