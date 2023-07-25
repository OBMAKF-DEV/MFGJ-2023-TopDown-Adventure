from source.const import SCALE
from source.const import map_objects
from source.container import Container, InteractionObject, Item
from source.door import Door, OBJECTS, KeyItem
from enum import Enum
from typing import TextIO
import pygame


class Tile:
    """Base tile class for `MapTiles`.
    
    Holds property data relating to an area on the map.
    
    Attributes:
        texture: The texture to be rendered.
        is_passable (bool): Whether the player can pass through the area.
        can_interact (bool): Whether the player can interact with the area.
    """
    def __init__(self, image, passable: bool, can_interact: bool, _object: object | InteractionObject = None) -> None:
        """Initializes the `Tile`.
        
        Args:
            image: The image to display when rendered.
            passable (bool): Whether the player can pass through the area.
            can_interact (bool): Whether the player can interact with the area.
            _object (object): Linked item to the tile.
        """
        self.texture = image
        self.is_passable = passable
        self.can_interact = can_interact
        self.object = _object


class MapTiles:
    """Collection containing all the different map `Tile` objects.
    
    Attributes:
        WALL (Tile): Un-passable, un-interactive `Tile` containing the imaging for rendering walls.
        FLOOR (TILE): Passable, un-interactive `Tile` containing the imaging for rendering floor.
        CONTAINER (Tile): Un-passable, interactive `Tile` containing the imaging for rendering containers.
    """
    WALL = Tile('resources/img/tiles/path_center.png', False, False, None)
    FLOOR = Tile('resources/img/tiles/grass1.png', True, False, None)
    #CONTAINER = Tile('resources/img/tiles/crate.png', False, True, Container([Item('Apple', None)]))


class Map:
    """Game map.
    
    Contains methods and logic for loading and rendering game environments from a file.
    
    Attributes:
        tiles (list[list[Tile]]): Nested array of `Tiles` loaded from the map file.
        current_map (TextIO): Open text stream of the map file containing the current map layout.
        current_file (str | bytes): The filename of the current map file.
        objects (list[object]): List containing objects to be rendered in.
        game (Game): The main game object.
    """
    tiles: list[list[Tile]] = []
    current_map: TextIO = None
    current_file: str | bytes = None
    objects: list[object]
    doors: dict[tuple[int, int], Door]
    containers: dict[tuple[int, int], dict]
    
    def __init__(self, game) -> None:
        self.game = game
    
    def load(self, file: str | bytes) -> None:
        """Loads the `current_map` from a map file.
        
        Args:
            file (str | bytes): The file to read and load the map from.
        
        Raises:
            FileNotFoundError: If the file cant be found.
        """
        self.game.map_doors = []
        try:
            self.doors = OBJECTS[file]['doors']
        except KeyError:
            self.doors = {}
        self.game.map_containers = []
        try:
            self.containers = OBJECTS[file]['containers']
        except KeyError:
            self.containers = {}
        try:
            with open(file, 'r', encoding='utf-8') as map_file:
                for y, line in enumerate(map_file.readlines()):
                    row = []
                    for x, char in enumerate(line.strip()):
                        tile: Tile | None = None
                        match char:
                            case '#':
                                tile = MapTiles.WALL
                            case '-':
                                tile = MapTiles.FLOOR
                            case '+':
                                items = [Item(**item) for item in self.containers[(x, y)]['items']]
                                key = KeyItem('key', None, self.game.map_doors[0])
                                items.append(key)
                                self.game.map_keys.append(key)
                                container = Container(self.game, items)
                                tile = Tile(
                                    'resources/img/tiles/crate.png', False, True,
                                    container)
                                self.game.map_containers.append(container)
                            case '>':
                                door = Door(self.game, **self.doors[(x, y)][0])
                                tile = Tile(
                                    'resources/img/tiles/door.png', False, True, door)
                                self.game.map_doors.append(door)
                        row.append(tile)
                    self.tiles.append(row)
                self.current_map = map_file
            self.current_file = file
        except FileNotFoundError as exc:
            raise FileNotFoundError(exc) from exc
        return self.get_objects()
    
    def get_objects(self):
        ...
    
    def render(self) -> None:
        """Renders the environment from the loaded tiles."""
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if not isinstance(tile, Tile):
                    continue
                image = pygame.transform.scale(pygame.image.load(tile.texture), (SCALE, SCALE))
                rect = pygame.Rect(x * SCALE, y * SCALE, SCALE, SCALE)
                self.game.screen.blit(image, rect)
