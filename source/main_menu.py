from source.const import MenuState, GameState


class MainMenu:
    state = MenuState.CLOSED
    selection_index: int = 0
    options = ["New Game", "Load Game", "Quit"]
    
    def __init__(self, game) -> None:
        self.game = game
        self.commands = [lambda: self.game.set_state(1), ..., lambda: self.game.set_state(2)]
    
    def open(self) -> None:
        if self.state == MenuState.OPENED:
            return
        self.game.state = GameState.MAIN_MENU
        self.state = MenuState.OPENED
        ...
    
    def close(self) -> None:
        if self.state == MenuState.CLOSED:
            return
        self.state = MenuState.CLOSED
        ...
