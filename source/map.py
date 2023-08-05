import xml.etree.ElementTree as element
from xml.etree.ElementTree import Element

from source.const import SCALE
from source.const.icons import TILE_ICONS
from source.container import Container, InteractionObject, Item
from source.door import Door, KeyItem
from source.npc import StoryNPC, EnemyNPC

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
    def __init__(
            self, image, passable: bool, can_interact: bool,
            _object: object | InteractionObject = None) -> None:
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
        GRASS (TILE): Passable, un-interactive `Tile` containing the imaging for rendering floor.
    """
    FRONT_RIGHT_WALL = Tile(TILE_ICONS['FRONT_RIGHT_WALL'], False, False, None)
    FRONT_LEFT_WALL = Tile(TILE_ICONS['FRONT_LEFT_WALL'], False, False, None)
    RIGHT_WALL = Tile(TILE_ICONS['RIGHT_WALL'], False, False, None)
    BACK_ROOFTOP = Tile(TILE_ICONS['BACK_ROOFTOP'], False, False, None)
    LEFT_WALL = Tile(TILE_ICONS['LEFT_WALL'], False, False, None)
    BACK_WALL = Tile(TILE_ICONS['BACK_WALL'], False, False, None)
    ROCK_WALL = Tile(TILE_ICONS['ROCK_WALL'], False, False, None)
    ROOFTOP = Tile(TILE_ICONS['ROOFTOP'], False, False, None)
    WALL = Tile(TILE_ICONS['WALL'], False, False, None)
    GRASS = Tile(TILE_ICONS['GRASS'], True, False, None)
    TILES = Tile(TILE_ICONS['TILES'], True, False, None)
    PATH_H = Tile(TILE_ICONS['PATH_H'], True, False, None)
    TREE = Tile(TILE_ICONS['TREE'], False, False, None)


class Map:
    """Game map.
    
    Contains methods and logic for loading and rendering game environments from a file.
    FLOOR
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
    doors: list[dict]
    containers: list[dict]
    friendly_npc: list[dict]
    enemy_npc: list[dict]
    element_data: Element | None
    
    def __init__(self, game) -> None:
        self.game = game
    
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
        self.friendly_npc = []
        self.enemy_npc = []
        self.game.npc = []
        
        tree = element.parse(f"resources/maps/data/{filename}.xml")
        
        self.element_data = tree.getroot()
        
        # Get all container data
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
        
        # Get all door data
        for data in self.element_data.findall('.//door'):
            obj_attributes = ['x', 'y', 'state', 'key']  # Surface level attributes
            
            door = dict()
            for key in obj_attributes:
                door[key] = int(data.attrib[key]) if data.attrib[key].isnumeric() \
                    else data.attrib[key]
            door['destination'] = data.find('.//location').text
            
            door['spawn'] = dict()
            door['spawn']['x'] = int(data.find('.//spawn').attrib['x'])
            door['spawn']['y'] = int(data.find('.//spawn').attrib['y'])
            
            self.doors.append(door)
        
        # Get all friendly NPC data
        for data in self.element_data.findall('.//friendly'):
            obj_attributes = [
                'x', 'y', 'image', 'name', 'dialog',
                'line', 'health', 'max_health', 'damage']
            
            friendly = dict()
            for key in obj_attributes:
                friendly[key] = int(data.attrib[key]) if data.attrib[key].isnumeric() \
                    else data.attrib[key]
            scripts = []
            
            for script in data.findall('.//script'):
                scripts.append(script.attrib['file'])
            friendly['scripts'] = scripts
            
            self.friendly_npc.append(friendly)

        # Get all enemy NPC data.
        for data in self.element_data.findall('.//enemy'):
            obj_attributes = [
                'x', 'y', 'image', 'name',
                'health', 'max_health', 'damage']

            enemy = dict()

            for key in obj_attributes:
                enemy[key] = int(data.attrib[key]) if data.attrib[key].isnumeric() \
                    else data.attrib[key]
            scripts = []

            for script in data.findall('.//script'):
                scripts.append(script.attrib['file'])
            enemy['scripts'] = scripts

            self.enemy_npc.append(enemy)
        
        # Generate NPC's
        friendly_npcs = []
        for npc_data in self.friendly_npc:
            image = pygame.transform.scale(
                pygame.image.load(
                    f"resources/img/npc/{npc_data['image']}.png"),
                (self.game.graphics['SCALE']**4, self.game.graphics['SCALE']**4))
            name = npc_data['name']
            scripts = npc_data['scripts']
            position = npc_data['x'], npc_data['y']
            
            friendly_npcs.append(StoryNPC(
                self.game, friendly=True, name=name, image=image,
                scripts=scripts, position=position, dialog=npc_data['dialog'], line=npc_data['line'],
                health=npc_data['health'], max_health=npc_data['max_health'], damage=npc_data['damage']
            ))

        enemy_npcs = []
        for npc_data in self.enemy_npc:
            image = pygame.transform.scale(
                pygame.image.load(
                    f"resources/img/npc/{npc_data['image']}.png"),
                (self.game.graphics['SCALE'] ** 4, self.game.graphics['SCALE'] ** 4))
            name = npc_data['name']
            position = npc_data['x'], npc_data['y']

            friendly_npcs.append(EnemyNPC(
                self.game, name=name, image=image, position=position,
                health=npc_data['health'], max_health=npc_data['max_health'], damage=npc_data['damage']
            ))
        
        self.game.npc.append(enemy_npcs)
        
        self.tiles = []
        
        try:
            with open(f"resources/maps/{filename}.txt", 'r', encoding='utf-8') as map_file:
                for y, line in enumerate(map_file.readlines()):
                    row = []
                    for x, char in enumerate(line.strip()):
                        tile: Tile | tuple | None = None
                        match char:
                            case '#':
                                tile = MapTiles.BACK_WALL
                            
                            case '[':
                                tile = MapTiles.LEFT_WALL
                            
                            case ']':
                                tile = MapTiles.RIGHT_WALL
                                
                            case '{':
                                tile = MapTiles.FRONT_LEFT_WALL
                            
                            case '}':
                                tile = MapTiles.FRONT_RIGHT_WALL
                            
                            case '-':
                                tile = MapTiles.TILES
                            
                            case '%':
                                tile = (MapTiles.GRASS, MapTiles.RIGHT_WALL)
                            
                            case '&':
                                tile = (MapTiles.GRASS, MapTiles.LEFT_WALL)
                            
                            case '$':
                                tile = (MapTiles.BACK_WALL, MapTiles.LEFT_WALL)
                            
                            case ')':
                                tile = (MapTiles.GRASS, MapTiles.FRONT_RIGHT_WALL)
                            
                            case '(':
                                tile = (MapTiles.GRASS, MapTiles.FRONT_LEFT_WALL)
                            
                            case '^':
                                tile = MapTiles.GRASS
                            
                            case 'r':
                                tile = MapTiles.ROOFTOP
                            
                            case 'p':
                                tile = MapTiles.PATH_H
                            
                            case '*':
                                tile = MapTiles.TREE
                            
                            case 'R':
                                tile = MapTiles.BACK_ROOFTOP
                            
                            case '"':
                                tile = MapTiles.ROCK_WALL
                            
                            case '+':
                                for _data in self.containers:
                                    items = []
                                    if _data['x'] == x and _data['y'] == y:
                                        coords: tuple[int, int] = _data['x'], _data['y']
                                        items: list[KeyItem | Item] = _data['items']
                                
                                container = Container(self.game, items)
                                tile = Tile(TILE_ICONS['CRATE'], False, True, container)
                                #self.game.map_containers.append(container)
                            
                            case 'P':
                                for _data in self.doors:
                                    if _data['x'] == x and _data['y'] == y:
                                        lock_state = False
                                        key = 'test_key'
                                        destination = _data['destination']
                                        spawn = _data['spawn']['x'], _data['spawn']['y']
                                        image = TILE_ICONS['PATH_H']
                                        door = Door(
                                            game=self.game,
                                            location=self.filename,
                                            position=(x, y),
                                        destination=destination,
                                        spawn=spawn,
                                        key=_data['key'],
                                        locked=lock_state)
                                        tile = Tile(image, False, True, door)
                            
                            case '>':
                                key = None
                                for _data in self.doors:
                                    if _data['x'] == x and _data['y'] == y:
                                        lock_state = True if _data['state'] == 'locked' else False
                                        key = _data['key'] if _data['key'] != 'None' else None
                                        destination = _data['destination']
                                        spawn = _data['spawn']['x'], _data['spawn']['y']
                                image = TILE_ICONS['LEFT_DOOR']
                                try:
                                    _check = line.strip()[y][x-1]
                                    if _check != '?':
                                        image = TILE_ICONS['RIGHT_DOOR']
                                except IndexError:
                                    ...
                                finally:
                                    door = Door(self.game, self.filename, (x, y), destination, spawn, key, lock_state)
                                    tile = Tile(image, False, True, door)
                            
                            case '/':
                                key = None
                                for _data in self.doors:
                                    if _data['x'] == x and _data['y'] == y:
                                        lock_state = True if _data['state'] == 'locked' else False
                                        key = _data['key'] if _data['key'] != 'None' else None
                                        destination = _data['destination']
                                        spawn = _data['spawn']['x'], _data['spawn']['y']
                                image = TILE_ICONS['CAVE_DOOR']
                                try:
                                    _check = line.strip()[y][x-1]
                                    if _check != '?':
                                        image = TILE_ICONS['CAVE_DOOR']
                                except IndexError:
                                    ...
                                finally:
                                    door = Door(self.game, self.filename, (x, y), destination, spawn, key, lock_state)
                                    tile = Tile(image, False, True, door)
                            
                            case '@':
                                key = None
                                for _data in self.doors:
                                    if _data['x'] == x and _data['y'] == y:
                                        lock_state = True if _data['state'] == 'locked' else False
                                        key = _data['key'] if _data['key'] != 'None' else None
                                        destination = _data['destination']
                                        spawn = _data['spawn']['x'], _data['spawn']['y']
                                image = TILE_ICONS['LEFT_DOOR']
                                try:
                                    _check = line.strip()[y][x-1]
                                    if _check != '?':
                                        image = TILE_ICONS['RIGHT_DOOR']
                                except IndexError:
                                    ...
                                finally:
                                    door = Door(self.game, self.filename, (x, y), destination, spawn, key, lock_state)
                                    tile = (MapTiles.GRASS, Tile(image, False, True, door))
                        row.append(tile)
                    self.tiles.append(row)
                self.current_map = map_file
            self.current_file = f"resources/maps/{filename}.txt"
        
        except FileNotFoundError as exc:
            raise FileNotFoundError(exc) from exc
    
    def remove_object_data(self, item: Item | KeyItem):
        """Removes the session XML data values containing an object."""
        container = self.element_data.find('.//container')
        
        # Search for the item in the data file & remove the value.
        try:
            for _item in container.findall('.//object'):
                if _item.attrib.get('name') == item.name:
                    container.find('.//items').remove(_item)
                    break
        except AttributeError:
            pass
        
        # Save the current session data into the corresponding data file.
        with open(f"resources/maps/data/{self.filename}.xml", 'wb') as file:
            file.write(element.tostring(self.element_data))
    
    def render(self) -> None:
        """Renders the environment from the loaded tiles."""
        scale = self.game.settings.get_graphics()["SCALE"]
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if not isinstance(tile, Tile):
                    if isinstance(tile, tuple):
                        _rect = pygame.Rect(x * SCALE, y * SCALE + 100, scale**4, scale**4)
                        try:
                            self.game.screen.blit(tile[0].texture, _rect)
                            self.game.screen.blit(tile[1].texture, _rect)
                        except AttributeError:
                            self.game.screen.blit(tile[1].texture, _rect)
                            continue
                    continue
                rect = pygame.Rect(x * SCALE, y * SCALE  + 100, scale**4, scale**4)
                self.game.screen.blit(tile.texture, rect)
