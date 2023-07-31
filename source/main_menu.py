import pygame

from source.const import MenuState, GameState, rgb


class MainMenu:
    state = MenuState.CLOSED
    selection_index: int = 0
    options = ["New Game", "Load Game", "Quit"]
    
    def __init__(self, game) -> None:
        self.game = game
        self.commands = [lambda: self.game.set_state(1), ..., lambda: self.game.set_state(2)]
        self.width, self.height = self.game.geometry
        self.widgets = {
            'border': pygame.Surface(((self.width / 3) + 10, 210)),
            'panel': pygame.Surface((self.width / 3, 200)),
            'button': pygame.Surface(((self.width / 3) - 10, 190)),
            'label': pygame.Surface((((self.width / 3) - 20), 185/3)),
        }
    
    def open(self) -> None:
        if self.state == MenuState.OPENED:
            return
        self.game.state = GameState.MAIN_MENU
        self.state = MenuState.OPENED
    
    def close(self) -> None:
        if self.state == MenuState.CLOSED:
            return
        self.state = MenuState.CLOSED
