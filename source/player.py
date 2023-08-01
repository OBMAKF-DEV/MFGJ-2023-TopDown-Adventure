from source.const import SCALE, PLAYER_ICONS
from source.const.icons import SWORD_PLAYER_ICONS
from source.const.icons import TOPBAR_ICONS
from source.utils.directions import *
from source.map import Tile
from source.items import Item
from source.items import InteractionObject
from source.const import GameState, EntityState, rgb
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
        self.equipped = None
    
    def on_death(self) -> None:
        self.state = EntityState.DEAD
        self.game.state = GameState.GAME_OVER
    
    def render_topbar(self) -> None:
        width, height = pygame.display.get_desktop_sizes()[0]
        bar = pygame.Surface((width, 80))
        bar.fill(rgb.GRAY)
        self.game.screen.blit(bar, (0, 0))
        
        health_display = pygame.Surface((350, 60))
        health_display.fill(rgb.GRAY)
        hp = self.game.fonts['HEALTH'].render(f"HP: {self.health} / {self.max_health}", 0, rgb.BLACK)
        health_display.blit(hp, (170, 30))
        
        heart = pygame.transform.scale(pygame.image.load(TOPBAR_ICONS['FULL_HEART']), (30, 30))
        
        match self.health:
            case 100:
                for i in range(5):
                    health_display.blit(heart, (30*i+10, 20))
        self.game.screen.blit(health_display, (10, 10))
    
    def render(self) -> None:
        """Render in the players icon."""
        scale = self.game.graphics['SCALE']
        self.render_topbar()
        
        # Create a surface for displaying icon.
        rect = pygame.rect.Rect(
            self.position[0] * scale - (scale * 2),
            self.position[1] * scale - (scale * 3) + 100,
            scale ** 4, scale ** 4)
        
        # Load and transform, the player icon.
        _icon = PLAYER_ICONS[self.facing_direction] if self.equipped is None else \
            SWORD_PLAYER_ICONS[self.facing_direction]
        icon = pygame.transform.scale(
            pygame.image.load(_icon), (scale*4, scale*4))
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

    def get_facing(self) -> tuple[int, int] | None:
        """Gets the coordinates of the tile that the player is facing."""
        if self.facing_direction == Directions.NORTH:
            x, y = north(self.position)
        elif self.facing_direction == Directions.SOUTH:
            x, y = south(self.position)
        elif self.facing_direction == Directions.WEST:
            x, y = west(self.position)
        else:
            x, y = east(self.position)
        return x, y
    
    def interact(self):
        x, y = self.get_facing()
        tile = self.game.map.tiles[y//4][x//4]
        if isinstance(tile, Tile):
            if tile.object is not None and tile.can_interact:
                return tile.object.interact()
        elif isinstance(tile, tuple):
            if isinstance(tile[0], Tile):
                if tile[0].object is not None and tile[0].can_interact:
                    return tile[0].object.interact()
            elif isinstance(tile[1], Tile):
                if tile[1].object is not None and tile[1].can_interact:
                    return tile[1].object.interact()

    def attack(self) -> None:
        x, y = self.get_facing()
        for npc_types in self.game.npc:
            for npc in npc_types:
                if npc.position != (x, y):
                    continue
                self.deal_damage(npc)
        ...  # todo - complete action
