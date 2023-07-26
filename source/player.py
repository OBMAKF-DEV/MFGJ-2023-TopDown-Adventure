from source.const import SCALE
from source.utils.directions import *
from source.map import Tile
from source.items import Item
from source.items import InteractionObject
from source.const import GameState, EntityState
from source.entity import Entity
from source.container import Container
import pygame


class Inventory(Container):
    items = []
    
    def __init__(self, player, items: list[Item]) -> None:
        super(Inventory, self).__init__(player.game, items)
        self.player = player
    
    def __str__(self) -> str:
        return "Inventory"


class Player(Entity):
    inventory: Inventory
    
    def __init__(
            self, game, position: tuple[int, int] = (1, 1),
            health: int = 100, max_health: int = 100, damage: int = 5) -> None:
        super(Player, self).__init__(health, max_health, damage)
        self.state = EntityState.ALIVE
        self.game = game
        self.position = position
        self.facing_direction = Directions.SOUTH
        self.inventory = Inventory(self, [])
    
    def on_death(self) -> None:
        self.state = EntityState.DEAD
        self.game.state = GameState.GAME_OVER
    
    def render(self) -> None:
        icon = {
            Directions.SOUTH: 'resources/img/player.png',
            Directions.NORTH: 'resources/img/player_UP.png',
            Directions.WEST: 'resources/img/player_L.png',
            Directions.EAST: 'resources/img/player_R.png'
        }

        image = pygame.transform.scale(pygame.image.load(icon[self.facing_direction]), (SCALE, SCALE))
        rect = pygame.rect.Rect(self.position[0] * SCALE, self.position[1] * SCALE, SCALE, SCALE)
        self.game.screen.blit(image, rect)
    
    def face(self, direction):
        if direction in Directions:
            self.facing_direction = direction
    
    def move(self, position):
        x, y = position
        asset = self.game.map.tiles[y][x]
        if isinstance(asset, Tile):
            if asset.is_passable:
                self.position = position
    
    def interact(self):
        if self.facing_direction == Directions.NORTH:
            x, y = north(self.position)
        elif self.facing_direction == Directions.SOUTH:
            x, y = south(self.position)
        elif self.facing_direction == Directions.WEST:
            x, y = west(self.position)
        else:
            x, y = east(self.position)
        
        tile = self.game.map.tiles[y][x]
        if isinstance(tile, Tile):
            if tile.object is not None and tile.can_interact:
                return tile.object.interact()
