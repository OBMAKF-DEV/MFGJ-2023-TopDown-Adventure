from source.const import SCALE
from source.const import map_objects
from source.container import Container, InteractionObject, Item
from source.door import Door, OBJECTS, KeyItem
from enum import Enum
from typing import TextIO

import xml.etree.ElementTree as element
import pygame

OBJECTS = OBJECTS


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
    filename: str
    tiles: list[list[Tile]] = []
    current_map: TextIO = None
    current_file: str | bytes = None
    objects: list[object]
    doors: list
    containers: list[dict]
    
    def __init__(self, game) -> None:
        self.game = game
        self.element_data = None
    
    def load(self, filename: str) -> None:
        """Loads the `current_map` from a map file.
        
        Args:
            filename (str | bytes): The name of the files to read and load the map from.
        
        Raises:
            FileNotFoundError: If the file cant be found.
        """
        self.filename = filename

        self.containers = []
        self.doors = []
        
        tree = element.parse(f"resources/maps/data/{filename}.xml")
        
        self.element_data = tree.getroot()
        
        for data in self.element_data.findall('.//container'):
            container = dict()
            container['x'] = int(data.attrib['x'])
            container['y'] = int(data.attrib['y'])
            container['items'] = []
            for item_data in data.findall('.//object'):
                item = dict()
                item['name'] = item_data.attrib['name']
                item['image'] = item_data.attrib['image'] if \
                    item_data.attrib['image'] != 'None' else None
                if item_data.attrib['type'] == 'Item':
                    container['items'].append(Item(item['name'], item['image']))
                    continue
                container['items'].append(KeyItem(item['name'], item['image'], None))
            self.containers.append(container)
        
        for data in self.element_data.findall('.//door'):
            door = dict()
            door['x'] = int(data.attrib['x'])
            door['y'] = int(data.attrib['y'])
            door['state'] = data.attrib['state']
            door['key'] = data.attrib['key']
            door['destination'] = data.find('.//location').text
            door['spawn'] = dict()
            door['spawn']['x'] = int(data.find('.//spawn').attrib['x'])
            door['spawn']['y'] = int(data.find('.//spawn').attrib['y'])
            self.doors.append(door)
        
        try:
            with open(f"resources/maps/{filename}.txt", 'r', encoding='utf-8') as map_file:
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
                                #items = [Item(**item) for item in self.containers[(x, y)]['items']]
                                #key = KeyItem('key', None, self.game.map_doors[0])
                                #items.append(key)
                                #self.game.map_keys.append(key)
                                #container = Container(self.game, items)
                                for _data in self.containers:
                                    items = []
                                    if _data['x'] == x and _data['y'] == y:
                                        coords: tuple[int, int] = _data['x'], _data['y']
                                        items: list[KeyItem | Item] = _data['items']
                                container = Container(self.game, items)
                                tile = Tile(
                                    'resources/img/tiles/crate.png',
                                    False, True,container)
                                self.game.map_containers.append(container)
                            case '>':
                                for _data in self.doors:
                                    if _data['x'] == x and _data['y'] == y:
                                        lock_state = True if _data['state'] == 'locked' else False
                                        key = _data['key'] if _data['key'] != 'None' else None
                                        destination = _data['destination']
                                        spawn = _data['spawn']['x'], _data['spawn']['y']
                                door = Door(self.game, self.filename, (x, y), destination, spawn, key, lock_state)
                                tile = Tile(
                                    'resources/img/tiles/door.png', False, True, door)
                                self.game.map_doors.append(door)
                        row.append(tile)
                    self.tiles.append(row)
                self.current_map = map_file
            self.current_file = f"resources/maps/{filename}.txt"
        except FileNotFoundError as exc:
            raise FileNotFoundError(exc) from exc
        return self.get_objects()
    
    def update_objects(self, container: Container = None):  # todo... update values in the XML file.
        ...
    
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
