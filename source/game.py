"""Main Game Module."""

from typing import Any
from source.map import Map
from source.player import Player
from source.main_menu import MainMenu
from source.utils import *
from source.const import GameState, ContainerState, rgb
from source.container import Container
import pygame
import multiprocessing
from pygame import Surface


class Game:
    """Base game class giving the user accessibility to interact with the game.
    
    Attributes:
        maps (list[str | bytes]):           Contains all the map files for loading into areas.
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
    selected_index: int | None = 0
    container: Container | None
    
    maps: list[str] = ['test_map', 'test_map2']
    map_containers = []
    map_doors = []
    map_keys = []
    state = GameState.NONE
    
    def __init__(self) -> None:
        """Initializes the `Game` class."""
        pygame.init()
        self.fonts = {'MENU': pygame.font.Font(None, 24), 'MAIN_MENU': pygame.font.Font(None, 50)}
        self.settings = Settings(self)
        self.graphics = self.settings.get_graphics()
        self.geometry: tuple[int, int] = (
            int(self.graphics['Width']),
            int(self.graphics['Height'])
        )
        self.screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        self.clock = pygame.time.Clock()
        
        self.player = Player(self)
        self.map = Map(self)
        self.main_menu = MainMenu(self)
        
        self.state = GameState.MAIN_MENU
        
        self.set_area(0)
    
    def set_state(self, state: int) -> None:
        """Sets the game state from a numerical value."""
        match state:
            case 0:
                self.state = GameState.NONE
                return
            case 1:
                self.state = GameState.RUNNING
                return
            case 2:
                self.state = GameState.ENDED
                return
            case 3:
                self.state = GameState.GAME_OVER
                return
            case 4:
                self.state = GameState.SUSPENDED
                return
            case 5:
                self.state = GameState.OPEN_MENU
                return
    
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
        if self.state == GameState.OPEN_MENU or self.state == GameState.MAIN_MENU:
            self.render_menu()
    
    def update(self) -> None:
        """Updates the current events and visual properties."""
        self.screen.fill(rgb.BLACK)
        if self.state == GameState.RUNNING:
            self.main_menu.options[0] = "Continue"
            self.main_menu.options[1] = "Save Game"
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
                            self.state = GameState.MAIN_MENU
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
                            item = self.container.items.pop(self.selected_index)
                            self.player.inventory.items.append(item)
                            self.map.remove_object_data(item)
                            self.selected_index -= 1
                    
                    if event.key == pygame.K_x:
                        for _ in self.container.items:
                            item = self.container.items.pop()
                            self.player.inventory.items.append(item)
                            self.map.remove_object_data(item)
                        self.container.state = ContainerState.CLOSED
                        self.state = GameState.RUNNING
                    
                    if event.key == pygame.K_ESCAPE:
                        self.container.close()
                    
                    if self.container.__str__() == "Chest":
                        if event.key == pygame.K_f:
                            self.container.close()
                    elif self.container.__str__() == "Inventory":
                        if event.key == pygame.K_i:
                            self.container.close()
            
            elif self.state == GameState.MAIN_MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or \
                            event.key == pygame.K_s:
                        if self.selected_index >= len(self.main_menu.options)-1:
                            continue
                        self.selected_index += 1
                    
                    if event.key == pygame.K_UP or \
                            event.key == pygame.K_d:
                        if self.selected_index <= 0:
                            continue
                        self.selected_index -= 1
                    
                    if event.key == pygame.K_RETURN:
                        self.main_menu.commands[self.selected_index]()
                        self.main_menu.close()
    
    def render_menu(self):
        scale = self.graphics["SCALE"]
        
        if self.state == GameState.OPEN_MENU:
            header = pygame.surface.Surface((110, 225))
            header.fill(rgb.CHARCOAL)
            header.blit(self.fonts['MENU'].render(str(self.container).center(20), True, rgb.YELLOW), (5, 5))
            
            menu = pygame.surface.Surface((100, 200))
            menu.fill(rgb.WHITE)
            
            for i, item in enumerate(self.container.items):
                color = rgb.RED if i == self.selected_index else rgb.BLACK
                text = self.fonts['MENU'].render(item.name, True, color)
                menu.blit(text, (0, i * 25))
            header.blit(menu, (5, 20))
            
            self.screen.blit(header, ((self.player.position[0] + 2) * scale, self.player.position[1] * scale))
        
        elif self.state == GameState.MAIN_MENU:
            self.screen.fill(rgb.CHARCOAL)
            screen_width, screen_height = pygame.display.get_window_size()
            for i, item in enumerate(self.main_menu.options):
                color = rgb.YELLOW if i == self.selected_index else rgb.GRAY
                self.screen.blit(self.fonts['MAIN_MENU'].render(item, True, color), (0, i * 30))
            
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
