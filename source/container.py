import pygame.rect

from source.items import Item, InteractionObject
import tkinter as tk
import tkinter.ttk as ttk
from enum import Enum


class ContainerStates(Enum):
    CLOSED = 0
    OPEN = 1


class Container(InteractionObject):
    items = []
    state = ContainerStates.CLOSED
    
    def __init__(self, game, items: list[Item] | None):
        self.game = game
        self.items = []
        if isinstance(items, list):
            self.items = [item for item in items]
    
    def interact(self):
        if self.state == ContainerStates.CLOSED:
            return self.open()
    
    def open(self):
        if self.state == ContainerStates.OPEN:
            return
        self.state = ContainerStates.OPEN
    
    def close(self):
        if self.state == ContainerStates.CLOSED:
            return
        self.state = ContainerStates.CLOSED
        print('closed')
    
    def draw(self):
        if self.state == ContainerStates.OPEN:
            font = pygame.font.Font(None, 18)
            title = pygame.font.Font(None, 25)
            self.game.screen.fill((255, 255, 255))
            self.game.screen.blit(title.render(str(self), True, (0, 0, 0)), (150, 10))
            for i, item in enumerate(self.items):
                self.game.screen.blit(font.render(item.name, True, (0, 0, 0)), (0, (i * 10) + 20))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i and str(self) == 'Inventory':
                        self.close()
                    elif str(self) != 'Inventory':
                        if event.key == pygame.K_f:
                            self.close()
                        elif event.key == pygame.K_i:
                            for i, item in enumerate(self.items):
                                self.game.player.inventory.items.append(self.items.pop(i))
                            return self.take_all()
                    else:
                        self.draw()
    
    def take_all(self):
        for item in self.items:
            self.game.player.inventory.items.append(item)
        self.game.map.update_objects(self)
        self.items = []
        self.close()
    
    def __str__(self) -> str:
        return 'Container'
