import pygame.display

from source.game import Game, GameState
from source.container import ContainerStates

if __name__ == '__main__':
    game = Game()
    while game.state != GameState.ENDED:
        game.clock.tick(60)
        game.update()
        
        for container in game.map_containers:
            if container.state == ContainerStates.OPEN:
                container.draw()
        
        if game.player.inventory.state == ContainerStates.OPEN:
            game.player.inventory.draw()
        
        pygame.display.flip()
