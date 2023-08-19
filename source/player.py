from source.const import SCALE, PLAYER_ICONS, TOTAL_PLAYER_ANIMATION_VALUE
from source.const.icons import SWORD_PLAYER_ICONS
from source.const.icons import TOPBAR_ICONS
from source.utils.directions import *
from source.map import Tile
from source.items import Item
from source.items import InteractionObject
from source.const import GameState, EntityState, rgb, Color
from source.entity import Entity
from source.container import Container
import pygame


class Inventory(Container):
    """
    Represents a Player Inventory system.
    
    Attributes:
        items (list[Item | KeyItem]): A list containing all items stored in the inventory.
    """
    items = []
    
    def __init__(self, player, items: list[Item]) -> None:
        """
        Initializes an instance of the Inventory class.
        Args:
            player (Player): The player that the inventory system belongs to.
            items (list[Item]): A list containing and items that the player is to start with.
        """
        super(Inventory, self).__init__(player.game, items)
        self.player = player
    
    def __str__(self) -> str:
        return "Inventory"


class Player(Entity):
    """Main Player (Entity) Class.
    
    Groups all player related logic together.
    
    Attributes:
        inventory (Inventory): The players Inventory, for storing items.
        animation_value (int): An integer value representing the current frame that the player is on.
    """
    inventory: Inventory
    animation_value = 0
    
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
        """
        Displays the top bar containing the players health and location status.
        """
        width, height = pygame.display.get_desktop_sizes()[0]
        bar = pygame.Surface((width, 80))
        bar.fill(Color.RGB.GRAY)
        bar.blit(
            self.game.fonts['HEALTH'].render(
                f"Location: {str(self.game.map.filename).replace('_', ' ').title()}", 0, Color.RGB.BLACK),
            ((width / 6) * 4, 30))
        self.game.screen.blit(bar, (0, 0))
        
        # Health Bar
        health_display = pygame.Surface((350, 60))
        health_display.fill(Color.RGB.GRAY)
        hp = self.game.fonts['HEALTH'].render(f"HP: {self.health} / {self.max_health}", 0, Color.RGB.BLACK)
        health_display.blit(hp, (170, 30))
        
        heart = pygame.transform.scale(pygame.image.load(TOPBAR_ICONS['FULL_HEART']), (30, 30))
        n = 0
        if 80 < self.health <= self.max_health:
            n = 5
        elif 60 < self.health <= 80:
            n = 4
        elif 40 < self.health <= 60:
            n = 3
        elif 20 < self.health <= 40:
            n = 2
        elif 0 < self.health <= 20:
            n = 1
        
        if n > 0:
            for i in range(n):
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
        
        _x, _y = self.get_facing()
        try:
            tile = self.game.map.tiles[_y//4][_x//4]
        except IndexError:
            return
        
        if (self.game.held_keys['s'] is True or
            self.game.held_keys['w'] is True or
            self.game.held_keys['a'] is True or
            self.game.held_keys['d'] is True) and isinstance(tile, Tile) and tile.is_passable:
            self.animation_value += 1
            if self.animation_value > TOTAL_PLAYER_ANIMATION_VALUE:
                self.animation_value = 0
        
        # Load and transform, the player icon.
        _icon = PLAYER_ICONS[self.facing_direction][int(self.animation_value/2)]
        #_icon = PLAYER_ICONS[self.facing_direction] if self.equipped is None else \
        #    SWORD_PLAYER_ICONS[self.facing_direction]
        icon = pygame.transform.scale(
            pygame.transform.scale(pygame.image.load(_icon), (scale*4, scale*4)), (40, 40))
        self.game.screen.blit(icon, rect)
    
    def face(self, direction):
        """Sets the direction that the player is facing."""
        if direction in Directions:
            self.facing_direction = direction
    
    def move(self, position) -> None:
        """Move the players position if the tile space permits them."""
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
        """
        Method for interacting with objects in front of the player based off the
        direction and location that the player is standing.
        """
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
        """Represents a strike or attack on an entity by the player."""
        x, y = self.get_facing()
        for npc_types in self.game.npc:
            for npc in npc_types:
                if npc.position != (x, y):
                    continue
                self.deal_damage(npc)
        ...  # todo - complete action
