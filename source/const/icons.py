from source.utils import Directions
from source.const import SCALE
import pygame

PLAYER_ICONS = {
    Directions.SOUTH: 'resources/img/player.png',
    Directions.NORTH: 'resources/img/player_UP.png',
    Directions.WEST: 'resources/img/player_L.png',
    Directions.EAST: 'resources/img/player_R.png'}

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
}
