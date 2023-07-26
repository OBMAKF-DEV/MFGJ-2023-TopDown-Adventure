from source.entity import Entity
from source.const import EntityState


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

    def __init__(self, game, name: str, image: str | bytes, friendly: bool, health: int = 100, max_health: int = 100, damage: int = 0) -> None:
        super().__init__(health, max_health, damage)
        self.game = game
        self.name = name
        self.image = image
        self.is_friendly = friendly
    
    def on_death(self) -> None:
        self.state = EntityState.DEAD


class StoryNPC(NPC):
    """An NPC class that gives it functionality for prompting dialog upon interaction."""
    def __init__(self, game, name: str, image: str | bytes, dialog: list[str], health: int = 100, max_health: int = 100, damage: int = 0) -> None:
        super().__init__(game, name, image, True, health, max_health, damage)
        self.dialog = dialog
    
    def interact(self):
        """Gives the player a way of being able to interact with the NPC."""
        # todo -- create progress log for triggering interactable events (player / game???).
        pass
