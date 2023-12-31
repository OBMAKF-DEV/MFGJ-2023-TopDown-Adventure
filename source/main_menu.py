import pygame

from source.const import MenuState, GameState, Color


class MainMenu:
    """
    The main menu for the game.
    
    Attributes:
        state (MenuState): Flag indicating the state of the menu.
        selection_index (int): The index indicating what option is currently in focus.
        options (list[str]): The name of each option that can be selected.
        commands (dict[str, func]): A dictionary containing the commands that
            can be executed on selecting from the menu.
    
    Args:
        game (Game): The main game object.
    """
    state = MenuState.CLOSED
    selection_index: int = 0
    options = ["New Game", "Load Game", "Quit"]
    
    def __init__(self, game) -> None:
        self.game = game
        self.commands = {
            "New Game": lambda: self.set_state(0),
            "Continue": lambda: self.set_state(0),
            "Load Game": lambda: self.set_state(2),
            "Save Game": lambda: self.set_state(3),
            "Quit": lambda: self.game.set_state(2)
        }
        self.width, self.height = self.game.geometry
        self.widgets = {
            'border': pygame.Surface(((self.width / 3) + 10, 210)),
            'panel': pygame.Surface((self.width / 3, 200)),
            'button': pygame.Surface(((self.width / 3) - 10, 190)),
            'label': pygame.Surface((((self.width / 3) - 20), 185/3)),
        }
    
    def set_state(self, index: int) -> None:
        """
        Sets the state of the menu and handles what the display and options should be.
        Args:
            index (int): Number indicating what the menu state should be.
        """
        match index:
            case 0:
                self.state = MenuState.CLOSED
                if self.game.state != GameState.ENDED:
                    self.game.set_state(1)
            case 1:
                self.state = MenuState.OPENED
                self.options = ["New Game", "Load Game", "Quit"]
                self.widgets = {
                    'border': pygame.Surface(((self.width / 3) + 10, 210)),
                    'panel' : pygame.Surface((self.width / 3, 200)),
                    'button': pygame.Surface(((self.width / 3) - 10, 190)),
                    'label' : pygame.Surface((((self.width / 3) - 20), 185 / 3)),
                }
            case 2:
                self.state = MenuState.LOAD
                self.widgets = {
                    'border': pygame.Surface(((self.width / 3) + 10, 270)),
                    'panel' : pygame.Surface((self.width / 3, 260)),
                    'button': pygame.Surface(((self.width / 3) - 10, 250)),
                    'label' : pygame.Surface((((self.width / 3) - 20), 245 / 4)),
                    'title' : self.game.fonts['MAIN_MENU'].render("Load Game", 0, Color.RGB.GOLD),
                }
                self.game.update()
            case 3:
                self.state = MenuState.SAVE
                self.widgets = {
                    'border': pygame.Surface(((self.width / 3) + 10, 270)),
                    'panel' : pygame.Surface((self.width / 3, 260)),
                    'button': pygame.Surface(((self.width / 3) - 10, 250)),
                    'label' : pygame.Surface((((self.width / 3) - 20), 245 / 4)),
                    'title' : self.game.fonts['MAIN_MENU'].render("Save Game", 0, Color.RGB.GOLD),
                }
            case 4:
                self.state = MenuState.CREATE_SAVE
                
                self.widgets = {
                    'border': pygame.Surface(((self.width / 6) * 3 + 10, 90)),
                    'panel' : pygame.Surface(((self.width / 6) * 3, 80)),
                    'button': pygame.Surface(((self.width / 6) * 3 - 10, 70)),
                    'title' : self.game.fonts['MAIN_MENU'].render("Create Save", 0, Color.RGB.GOLD),
                }
        self.game.update()
    
    def open(self) -> None:
        """
        Sets the menu state to OPENED.
        """
        if self.state == MenuState.OPENED:
            return
        self.set_state(1)
        self.game.state = GameState.MAIN_MENU
        #self.state = MenuState.OPENED
    
    def close(self) -> None:
        """
        Sets the menu state to CLOSED.
        """
        if self.state == MenuState.CLOSED:
            return
        self.set_state(0)
