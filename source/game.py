"""Main Game Module."""

from typing import Any
from source.map import Map
from source.player import Player
from source.utils import *
from source.const import GameState, ContainerState
from source.container import Container
import pygame
import multiprocessing
from pygame import Surface


class Game:
    """Base game class giving the user accessability to interact with the game.
    
    Attributes:
        maps (list[str | bytes]):           Contains all the map files for loading into areas.
        map_containers (list[Container]):   Holds all containers loaded into the current area. -- *updates the list when a map file is loaded.*
        map_doors (list[Door]):             Holds all doors loaded into the current area.
        map_keys (list[KeyItem]):           Contains all `KeyItem` objects as they are added into the world -- *doesn't update on map change.*
        state (Enum):                       Defines the current game state (*i.e.* ``RUNNING``... *etc.*)
        settings (dict):                    All parsed settings values int topics --> {```dict[topic][_Kw]```}.
        graphics (dict):                    Specifically the graphical settings --> {```dict[_Kw]```}.
        geometry (tuple[int, int]):         The set screen size from the graphical setting --> {```(Width, Height)```}.
        screen (Surface):                   The main screen display.
        clock (Clock):                      The internal clock, for handling frame refresh rates.
        player (Player):                    The main player object.
        map (Map):                          Contains methods for loading map files and rending the environment.
    """
    held_keys: dict[str, bool] = {'w': False, 'a': False, 's': False, 'd': False}
    process = None
    selected_index: int | None
    container: Container | None
    
    maps: list[str] = ['test_map', 'test_map2']
    map_containers = []
    map_doors = []
    map_keys = []
    state = GameState.NONE
    
    def __init__(self) -> None:
        """Initializes the `Game` class."""
        pygame.init()
        self.fonts = {'MENU': pygame.font.Font(None, 24)}
        self.settings = Settings(self)
        self.graphics = self.settings.get_graphics()
        self.geometry: tuple[int, int] = (int(self.graphics['Width']), int(self.graphics['Height']))
        
        #self.screen = pygame.display.set_mode(self.geometry)
        self.screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        self.clock = pygame.time.Clock()
        
        self.player = Player(self)
        self.map = Map(self)
        self.state = GameState.RUNNING
        
        self.set_area(0)
    
    def set_state(self, state: int) -> None:
        """Sets the game state from a numerical value."""
        if state == 0:
            self.state = GameState.NONE
        elif state == 1:
            self.state = GameState.RUNNING
        elif state == 2:
            self.state = GameState.ENDED
        elif state == 3:
            self.state = GameState.GAME_OVER
        elif state == 4:
            self.state = GameState.SUSPENDED
        elif state == 5:
            self.state = GameState.OPEN_MENU
    
    def set_area(self, index: int) -> None:
        """Sets the current map file (***** check usage...)"""
        try:
            if self.map.current_file == self.maps[index]:
                return
            self.map.load(self.maps[index])
        except IndexError as exc:
            raise IndexError(exc) from exc
    
    def render(self) -> None:
        """Groups together rendering methods to be called from the main event loop."""
        self.map.render()
        self.player.render()
        if self.state == GameState.OPEN_MENU:
            self.render_menu()
    
    def update(self) -> None:
        """Updates the current events and visual properties."""
        self.screen.fill((0, 0, 0))
        self.handle_events()
        self.render()
    
    def handle_events(self) -> Any:
        """Handles game events such player input.
        
        Note:
            IMPORTANT!!! 
            
            ~ provides event handler for closing the window **don't** remove! ~
        """
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.ENDED
            if self.state == GameState.RUNNING:
                if event.type == pygame.KEYUP:
                    match event.key:
                        case pygame.K_w | pygame.K_UP:
                            self.held_keys['w'] = False
                        case pygame.K_a | pygame.K_LEFT:
                            self.held_keys['a'] = False
                        case pygame.K_s | pygame.K_DOWN:
                            self.held_keys['s'] = False
                        case pygame.K_d | pygame.K_RIGHT:
                            self.held_keys['d'] = False
                
                elif event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.state = GameState.ENDED
                        case pygame.K_w | pygame.K_UP:
                            self.held_keys['w'] = True
                            self.player.face(Directions.NORTH)
                        case pygame.K_s | pygame.K_DOWN:
                            self.held_keys['s'] = True
                            self.player.face(Directions.SOUTH)
                        case pygame.K_a | pygame.K_LEFT:
                            self.held_keys['a'] = True
                            self.player.face(Directions.WEST)
                        case pygame.K_d | pygame.K_RIGHT:
                            self.held_keys['d'] = True
                            self.player.face(Directions.EAST)
                        case pygame.K_f | pygame.K_RETURN:
                            self.player.interact()
                        case pygame.K_i:
                            self.player.inventory.open()
                
            elif self.state == GameState.OPEN_MENU:
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_index = min(len(self.container.items) - 1, self.selected_index + 1)
                    
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_index = max(0, self.selected_index - 1)
                    
                    if event.key == pygame.K_RETURN:
                        if len(self.container.items) > 0:
                            self.player.inventory.items.append(self.container.items.pop(self.selected_index))
                    
                    if event.key == pygame.K_x:
                        for _ in self.container.items:
                            self.player.inventory.items.append(self.container.items.pop())
                        self.container.state = ContainerState.CLOSED
                        self.state = GameState.RUNNING
                    
                    if event.key == pygame.K_ESCAPE:
                        self.container.close()
                    
                    if self.container.__str__() == "Container":
                        if event.key == pygame.K_f:
                            self.container.close()
                    elif self.container.__str__() == "Inventory":
                        if event.key == pygame.K_i:
                            self.container.close()
    
    def render_menu(self):
        header = pygame.surface.Surface((110, 225))
        header.fill((50, 50, 50))
        header.blit(self.fonts['MENU'].render(str(self.container), True, (255, 255, 0)), (5, 5))
        menu = pygame.surface.Surface((100, 200))
        menu.fill((255, 255, 255))
        for i, item in enumerate(self.container.items):
            color = (255, 0, 0) if i == self.selected_index else (0, 0, 0)
            text = self.fonts['MENU'].render(item.name, True, color)
            menu.blit(text, (0, i * 25))
        scale = self.graphics["SCALE"]
        header.blit(menu, (5, 20))
        self.screen.blit(header, (
            (self.player.position[0] + 2) * scale,
            self.player.position[1] * scale))  #350, 200))
        pygame.display.flip()
    
    def open_container(self, container):
        self.container = container
        self.selected_index = 0
        self.state = GameState.OPEN_MENU
    
    def close_container(self, container):
        self.container = None
        self.selected_index = 0
        self.state = GameState.RUNNING
        self.update()
