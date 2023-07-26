import pygame
from source import Game, GameState, ContainerStates


def main():
    game = Game()
    while game.state != GameState.ENDED:
        game.clock.tick(game.graphics['FPS'])
        game.update()

        for container in game.map_containers:
            if container.state == ContainerStates.OPEN:
                container.draw()

        if game.player.inventory.state == ContainerStates.OPEN:
            game.player.inventory.draw()

        pygame.display.flip()


if __name__ == '__main__':
    main()
