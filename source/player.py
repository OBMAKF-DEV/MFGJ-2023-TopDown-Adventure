from source.const import SCALE, PLAYER_ICONS
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
            self, game, position: tuple[int, int] = (5, 6),
            health: int = 100, max_health: int = 100, damage: int = 5) -> None:
        super(Player, self).__init__(health, max_health, damage)
        
        self.game = game
        self.position = position

        self.state = EntityState.ALIVE
        self.facing_direction = Directions.SOUTH
        
        self.inventory = Inventory(self, [])
    
    def on_death(self) -> None:
        self.state = EntityState.DEAD
        self.game.state = GameState.GAME_OVER
    
    def render(self) -> None:
        """Render in the players icon."""
        scale = self.game.graphics['SCALE']
        
        # Create a surface for displaying icon.
        rect = pygame.rect.Rect(
            self.position[0] * scale - (scale * 2) + 100,
            self.position[1] * scale - (scale * 3) + 100,
            scale ** 4, scale ** 4)
        
        # Load and transform, the player icon.
        icon = pygame.transform.scale(
            pygame.image.load(
                PLAYER_ICONS[self.facing_direction]),
            (scale*4, scale*4))
        self.game.screen.blit(icon, rect)
    
    def face(self, direction):
        """Sets the direction that the player is facing."""
        if direction in Directions:
            self.facing_direction = direction
    
    def move(self, position):
        x, y = position
        asset = self.game.map.tiles[y//4][x//4]
        
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
        
        tile = self.game.map.tiles[y//4][x//4]
        if isinstance(tile, Tile):
            if tile.object is not None and tile.can_interact:
                return tile.object.interact()
