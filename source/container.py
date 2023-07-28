import pygame.rect
from source.const import GameState, ContainerState
from source.items import Item, InteractionObject
import tkinter as tk
import tkinter.ttk as ttk
from enum import Enum


class Container(InteractionObject):
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
        if self.state == ContainerState.OPEN:
            return
        self.state = ContainerState.OPEN
        self.game.open_container(self)
    
    def close(self):
        if self.state == ContainerState.CLOSED:
            return
        self.state = ContainerState.CLOSED
        self.game.close_container(self)
        print('closed')
    
    def take_all(self):
        for item in self.items:
            self.game.player.inventory.items.append(item)
        self.game.map.update_objects(self)
        self.items = []
        self.close()
    
    def __str__(self) -> str:
        return 'Chest'
