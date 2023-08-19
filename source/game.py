"""Main Game Module."""

from typing import Any
from source.map import Map
from source.player import Player
from source.main_menu import MainMenu
from source.utils import *
from source.const import GameState, ContainerState, MenuState, Color
from source.container import Container
from source.utils.save_handling import load_game, save_game
import pygame
import multiprocessing
from pygame import Surface
import tomli


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
    savefile = 'default'
    save_slot = None
    slots = []
    
    user_text = ''
    
    held_keys: dict[str, bool] = {'w': False, 'a': False, 's': False, 'd': False}
    process = None
    selected_index: int | None = 0
    container: Container | None
    
    maps: list[str] = ['test_map', 'test_map2', 'test_map2b', 'cave_entrance']
    map_containers = []
    map_doors = []
    map_keys = []
    npc = []
    state = GameState.NONE
    
    def __init__(self) -> None:
        """Initializes the `Game` class."""
        # set the save / load slots
        with open('resources/maps/data/saves/index.toml', 'rb') as indexes:
            slots = tomli.load(indexes)['slots']
            self.slots = [slots[str(i)] for i in range(1, 5)]
        
        # initialize pygame
        pygame.init()
        
        # create fonts
        self.fonts = {
            'MENU': pygame.font.Font(None, 24),
            'MAIN_MENU': pygame.font.Font(None, 50),
            'MAIN': pygame.font.SysFont('Jetbrains Mono', 50, True),
            'HEALTH': pygame.font.Font(None, 30),
            'DIALOG': pygame.font.Font(None, 20),
        }
        
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
        
        #self.state = GameState.MAIN_MENU
        
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
            case 6:
                self.state = GameState.MAIN_MENU
    
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
        for npc_type in self.npc:
            for npc in npc_type:
                npc.render()
        
        if self.state == GameState.OPEN_MENU or self.state == GameState.MAIN_MENU:
            self.render_menu()
    
    def update(self) -> None:
        """Updates the current events and visual properties."""
        self.screen.fill(Color.RGB.BLACK)
        if self.state == GameState.RUNNING:
            self.main_menu.options[0] = "Continue"
            self.main_menu.options[1] = "Save Game"
        elif self.state == GameState.MAIN_MENU:
            if self.main_menu.state == MenuState.LOAD or \
                    self.main_menu.state == MenuState.SAVE:
                self.main_menu.options = []
                for savefile in self.slots:
                    if savefile == 'default':
                        self.main_menu.options.append("Empty")
                        continue
                    self.main_menu.options.append(savefile)
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
                            self.main_menu.open()
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
                            if item.name == 'sword':
                                self.player.equipped = 'sword'
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
                    print(self.main_menu.state)
                    if self.main_menu.state == MenuState.CREATE_SAVE:
                        if event.key == pygame.K_RETURN:
                            save_game(self, self.selected_index+1, self.user_text)
                            self.user_text = ""
                            self.main_menu.close()
                        elif event.key == pygame.K_ESCAPE:
                            self.user_text = ""
                            self.set_state(1)
                            self.main_menu.open()
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if len(self.user_text) < 16:
                                self.user_text += event.unicode
                    else:
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
                            if self.main_menu.state == MenuState.OPENED:
                                return self.main_menu.commands[self.main_menu.options[self.selected_index]]()
                            
                            elif self.main_menu.state == MenuState.SAVE:
                                self.save_slot = self.selected_index + 1
                                self.main_menu.set_state(4)
                            
                            else:
                                load_game(self, self.selected_index+1)
                            
                            if self.main_menu.options[self.selected_index] != 'Empty':
                                self.main_menu.close()
                        
                        if event.key == pygame.K_ESCAPE:
                            if self.main_menu.state == MenuState.LOAD or \
                                    self.main_menu.state == MenuState.SAVE:
                                self.main_menu.set_state(1)
    
    def render_menu(self):
        scale = self.graphics["SCALE"]
        
        # Container and Inventory rendering
        if self.state == GameState.OPEN_MENU:
            header = pygame.surface.Surface((110, 225))
            header.fill(Color.RGB.CHARCOAL)
            header.blit(self.fonts['MENU'].render(
                str(self.container).center(20), True, Color.RGB.YELLOW), (5, 5))
            
            menu = pygame.surface.Surface((100, 200))
            menu.fill(Color.RGB.WHITE)
            
            for i, item in enumerate(self.container.items):
                color = Color.RGB.RED if i == self.selected_index else Color.RGB.BLACK
                text = self.fonts['MENU'].render(item.name, True, color)
                menu.blit(text, (0, i * 25))
            header.blit(menu, (5, 20))
            if self.player.position[0] <= 152:
                self.screen.blit(header, ((self.player.position[0] + 2) * scale, self.player.position[1] * scale))
                return
            self.screen.blit(header, ((self.player.position[0] - 20) * scale, self.player.position[1] * scale))
        
        # Main Menu rendering
        elif self.state == GameState.MAIN_MENU:
            # Render MainMenu
            _rect = pygame.Rect(0, 0, self.geometry[0]*4, self.geometry[1]*4)
            img = pygame.transform.scale(
                pygame.image.load('resources/img/stoneface.png'),
                (self.geometry[0]*2, self.geometry[1]*1.5))
            self.screen.blit(img, _rect)
            #self.screen.fill(rgb.CRIMSON)
            screen_width, screen_height = pygame.display.get_window_size()
            
            if self.main_menu.state == MenuState.LOAD or self.main_menu.state == MenuState.SAVE or \
                    self.main_menu.state == MenuState.CREATE_SAVE:
                self.screen.blit(self.main_menu.widgets['title'], ((screen_width/9) - 5, 45))
            
            _ = self.main_menu.widgets['border']
            _.fill(Color.RGB.TAUPE)
            self.screen.blit(_, ((screen_width/3) - 5, 95))
            
            _ = self.main_menu.widgets['panel']
            _.fill(Color.RGB.BLACK)
            self.screen.blit(_, (screen_width / 3, 100))
            
            _ = self.main_menu.widgets['button']
            _.fill(Color.RGB.TAUPE if self.main_menu.state != MenuState.CREATE_SAVE else Color.RGB.BLACK)
            self.screen.blit(_, ((screen_width/3) + 5, 105))
            
            if self.main_menu.state == MenuState.CREATE_SAVE:
                self.screen.blit(
                    self.fonts['MAIN_MENU'].render(self.user_text, 0, Color.RGB.YELLOW, Color.RGB.MAUVE),
                    ((screen_width/3) + 10, 120)
                )
            else:
                for i, item in enumerate(self.main_menu.options):
                    color = Color.RGB.MAUVE if self.selected_index == i else Color.RGB.CHARCOAL
                    
                    _ = self.main_menu.widgets['label']
                    _.fill(color)
                    self.screen.blit(_, ((screen_width/3) + 10, 110 + ((175/3) * i)))
                    
                    color = Color.RGB.BLACK if self.selected_index == i else Color.RGB.GRAY
                    self.screen.blit(self.fonts['MAIN_MENU'].render(item, 0, color), (
                        (screen_width/3) + 10, 110 + ((170/3) * i + ((170/3)/3))))
            
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
