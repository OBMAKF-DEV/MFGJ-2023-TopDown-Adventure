import time
import pygame
import shutil
from time import sleep
from source.utils import *
from source import Game, InteractionObject
from source.const import GameState, ContainerState, rgb


keys = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
DATA_FILES = ['test_map.xml', 'test_map2.xml']

PLAYER_SPEED = 2
DELAY = 0.5

def main():
    game = Game()
    game.state = GameState.RUNNING
    
    while game.state != GameState.ENDED:
        game.screen.fill(rgb.BLACK)
        #pygame.display.set_caption(str(game.clock.get_fps()))
        game.clock.tick(game.graphics['FPS']/game.graphics['SCALE']*4)
        game.update()
        if game.state == GameState.RUNNING:
            if game.held_keys['w']:
                game.player.face(Directions.NORTH)
                game.player.move(north(game.player.position), None)
                
            elif game.held_keys['a']:
                game.player.face(Directions.WEST)
                game.player.move(west(game.player.position), None)
                
            elif game.held_keys['s']:
                game.player.face(Directions.SOUTH)
                game.player.move(south(game.player.position), None)
                
            elif game.held_keys['d']:
                game.player.face(Directions.EAST)
                game.player.move(east(game.player.position), None)
            
        pygame.display.flip()
    # Reset the data files to their default values.
    for filename in DATA_FILES:
        shutil.copy(
            f'resources/maps/data/defaults/{filename}',
            f'resources/maps/data/{filename}')
    pygame.quit()


if __name__ == '__main__':
    main()
