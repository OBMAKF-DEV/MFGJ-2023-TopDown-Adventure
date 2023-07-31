import pygame

from source.entity import Entity
from source.const import EntityState
from pygame.surface import Surface, SurfaceType
from source.const import GameState
from source.const.states import DialogState


class NPC(Entity):
    """Base NPC class.
    
    Giving structure to all NPC objects.
    
    Attributes:
        game (Game):            The base class object.
        name (str):             The name used to identify the NPC.
        image (str | bytes):    The image used to display 
        is_friendly (bool):     Whether the NPC is friendly or not.
        (see `Entity` class for more info.)    
    """
    state = EntityState.ALIVE

    def __init__(
            self, game, name: str, image: str | bytes | Surface | SurfaceType, friendly: bool, position: tuple[int, int],
            health: int = 100, max_health: int = 100, damage: int = 0) -> None:
        super().__init__(health, max_health, damage)
        self.game = game
        self.name = name
        self.image = image
        self.is_friendly = friendly
        self.position = position
    
    def on_death(self) -> None:
        self.state = EntityState.DEAD
    
    def render(self):
        # Todo -- Provide a generic method for rendering in the NPC sprite.
        pass


class StoryNPC(NPC):
    """An NPC class that gives it functionality for prompting dialog upon interaction."""
    state = DialogState.NONE
    
    def __init__(
            self, game, name: str, friendly: bool, image: str | bytes | Surface | SurfaceType,
            scripts: list[str | bytes], position: tuple[int, int], dialog: int = 0, line: int = 0,
            health: int = 100, max_health: int = 100,
            damage: int = 0) -> None:
        super().__init__(game, name, image, friendly, position, health, max_health, damage)
        self.scripts = scripts
        self.dialog_index = dialog
        self.current_script = scripts[dialog]
        self.line = line
    
    def get_speech(self) -> str:
        with open(f"resources/npc/dialog/{self.scripts[self.dialog_index]}.txt") as script:
            _speech = script.readlines()[self.line]
            self.next_line()
            return _speech
    
    def interact(self):
        """Gives the player a way of being able to interact with the NPC."""
        if self.game.state == GameState.RUNNING:
            if self.state == DialogState.NONE:
                self.open_dialog()
        elif self.game.state == GameState.DIALOG_OPEN:
            if self.state == DialogState.IN_DIALOG:
                self.next_line()
    
    def open_dialog(self):
        if self.state == DialogState.IN_DIALOG:
            return
        self.state = DialogState.IN_DIALOG
        self.game.state = GameState.DIALOG_OPEN
    
    def close_dialog(self):
        if self.state == DialogState.NONE:
            return
        self.state = DialogState.NONE
        self.game.state = GameState.RUNNING
    
    def next_line(self):
        with open(f"resources/npc/dialog/{self.scripts[self.dialog_index]}.txt") as script:
            if len(script.readlines()) > self.line:
                self.line += 1
    
    def render(self):
        # Render the NPC when game state is running.
        if self.state == DialogState.NONE:
            return super(StoryNPC, self).render()
        elif self.state == DialogState.IN_DIALOG:
            conversation = self.get_speech()
            # todo - render in dialog box...
        return
