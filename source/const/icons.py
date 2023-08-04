from source.utils import Directions
from source.const import SCALE
import pygame

PLAYER_ICONS = {
    Directions.SOUTH: [f'resources/img/player/south/player0{i}.png' for i in range(6)],
    Directions.NORTH: [f'resources/img/player/north/player0{i}.png' for i in range(6)],
    Directions.WEST : [f'resources/img/player/west/player0{i}.png' for i in range(6)],
    Directions.EAST : [f'resources/img/player/east/player0{i}.png' for i in range(6)]
}


SWORD_PLAYER_ICONS = {
    Directions.SOUTH: 'resources/img/player_sword.png',
    Directions.NORTH: 'resources/img/player_UP_sword.png',
    Directions.WEST: 'resources/img/player_L_sword.png',
    Directions.EAST: 'resources/img/player_R_sword.png'
}

TOPBAR_ICONS = {
    'FULL_HEART': 'resources/img/full_heart.png'
}

TILE_ICONS = {
    'WALL': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/red_brick.png'),
        (SCALE, SCALE)),
    'GRASS': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/grass1.png'),
        (SCALE, SCALE)),
    'TILES': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/tiles.png'),
        (SCALE, SCALE)),
    'BACK_WALL': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/back_wall.png'),
        (SCALE, SCALE)),
    'LEFT_WALL': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/left_wall.png'),
        (SCALE, SCALE)),
    'RIGHT_WALL': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/right_wall.png'),
        (SCALE, SCALE)),
    'FRONT_LEFT_WALL': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/front_left_wall.png'),
        (SCALE, SCALE)),
    'FRONT_RIGHT_WALL': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/front_right_wall.png'),
        (SCALE, SCALE)),
    'DOOR': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/tiles.png'),
        (SCALE, SCALE)),
    'LEFT_DOOR': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/left_door.png'),
        (SCALE, SCALE)),
    'RIGHT_DOOR': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/right_door.png'),
        (SCALE, SCALE)),
    'CRATE': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/crate.png'),
        (SCALE, SCALE)),
    'ROOFTOP': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/rooftop.png'),
        (SCALE, SCALE)),
    'BACK_ROOFTOP': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/back_rooftop.png'),
        (SCALE, SCALE)),
    'PATH_H': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/dirt_path.png'),
        (SCALE, SCALE)),
    'TREE': pygame.transform.scale(
        pygame.image.load('resources/img/tiles/tree.png'),
        (SCALE, SCALE)),
}
