"""Main Game Module."""

from typing import Any
from source.map import Map
from source.player import Player
from source.utils import *
from source.const import GameState
import pygame
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
    maps: list[str] = ['test_map', 'test_map2']
    map_containers = []
    map_doors = []
    map_keys = []
    state = GameState.NONE
    
    def __init__(self) -> None:
        """Initializes the `Game` class."""
        pygame.init()
        
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
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.state = GameState.ENDED
                    case pygame.K_w:
                        self.player.face(Directions.NORTH)
                        self.player.move(north(self.player.position))
                    case pygame.K_s:
                        self.player.face(Directions.SOUTH)
                        self.player.move(south(self.player.position))
                    case pygame.K_a:
                        self.player.face(Directions.WEST)
                        self.player.move(west(self.player.position))
                    case pygame.K_d:
                        self.player.face(Directions.EAST)
                        self.player.move(east(self.player.position))
                    case pygame.K_f:
                        self.player.interact()
                    case pygame.K_i:
                        self.player.inventory.open()
