import pygame
import multiprocessing
from source import Game, InteractionObject
from source.const import GameState, ContainerState
from source.utils import *
from time import sleep

keys = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]


def background_task(task):
    while True:
        sleep(2)
        task()

def main():
    game = Game()
    game.state = GameState.RUNNING
    
    while game.state != GameState.ENDED:
        game.clock.tick(game.graphics['FPS']/game.graphics['SCALE']*2)
        game.update()
        
        if game.state == GameState.RUNNING:
            posx, posy = game.player.position
            while True:
                if game.held_keys['w']:
                    game.player.move(north(game.player.position))
                    break
                if game.held_keys['a']:
                    game.player.move(west(game.player.position))
                    break
                if game.held_keys['s']:
                    game.player.move(south(game.player.position))
                    break
                if game.held_keys['d']:
                    game.player.move(east(game.player.position))
                    break
                break
            
        pygame.display.flip()
    
    pygame.quit()


if __name__ == '__main__':
    main()
