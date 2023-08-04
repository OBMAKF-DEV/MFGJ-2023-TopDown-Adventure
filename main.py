import time
import pygame
import shutil
from time import sleep
from source.utils import *
from source import Game, InteractionObject
from source.const import GameState, ContainerState, rgb, TOTAL_PLAYER_ANIMATION_VALUE

DATA_FILES = ['test_map.xml', 'test_map2.xml', 'test_map2b.xml']


def main():
    """The main looping function."""
    game = Game()
    game.main_menu.open()
    
    while game.state != GameState.ENDED:
        
        game.screen.fill(rgb.BLACK)
        game.clock.tick(game.graphics['FPS']/game.graphics['SCALE']*4)
        game.update()
        
        if game.state == GameState.RUNNING:
            #pygame.display.set_caption(f"{game.clock.get_fps()} FPS")
            pygame.display.set_caption(f"{game.player.position[0] // 4}, {game.player.position[1] // 4}")
            
            if game.held_keys['w']:
                game.player.face(Directions.NORTH)
                game.player.move(north(game.player.position))
                
            elif game.held_keys['a']:
                game.player.face(Directions.WEST)
                game.player.move(west(game.player.position))
                
            elif game.held_keys['s']:
                game.player.face(Directions.SOUTH)
                game.player.move(south(game.player.position))
                
            elif game.held_keys['d']:
                game.player.face(Directions.EAST)
                game.player.move(east(game.player.position))
            
        pygame.display.flip()
    
    # Reset the data files to their default values.
    for filename in DATA_FILES:
        shutil.copy(
            f'resources/maps/data/defaults/{filename}',
            f'resources/maps/data/{filename}')
    
    pygame.quit()


if __name__ == '__main__':
    main()
