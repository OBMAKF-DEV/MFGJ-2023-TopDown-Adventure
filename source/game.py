from source.map import Map
from source.player import Player
from source.utils.directions import *
from enum import Enum
import pygame


class GameState(Enum):
    NONE = 0
    RUNNING = 1
    ENDED = 2
    GAME_OVER = 3


class Game:
    maps: list[str | bytes] = ['resources/maps/test_map.txt']
    map_containers = []
    map_doors = []
    map_keys = []
    state = GameState.NONE
    
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player = Player(self)
        self.map = Map(self)
        self.state = GameState.RUNNING
        self.set_area(0)
    
    def set_state(self, state: int) -> None:
        if state == 0:
            self.state = GameState.NONE
        elif state == 1:
            self.state = GameState.RUNNING
        elif state == 2:
            self.state = GameState.ENDED
        elif state == 3:
            self.state = GameState.GAME_OVER
    
    def set_area(self, index: int) -> None:
        try:
            if self.map.current_file == self.maps[index]:
                return
            self.map.load(self.maps[index])
        except IndexError as exc:
            raise IndexError(exc) from exc
    
    def render(self) -> None:
        self.map.render()
        self.player.render()
    
    def update(self) -> None:
        self.screen.fill((0, 0, 0))
        self.handle_events()
        self.render()
    
    def handle_events(self):
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
                ...
            ...
        ...
