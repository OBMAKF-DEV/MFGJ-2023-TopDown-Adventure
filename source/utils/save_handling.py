import tomli


def save_game(game, slot):
    """Provides access for saving game data to a save file via a game slot.
    
    Args:
        game (Game): The main game.
        slot (int): The slot to save the game data to.
    """
    with open('resources/maps/data/saves/index.toml', 'rb') as indexer:
        _data = tomli.load(indexer)['slots']
        open_slot = _data[slot]
        if open_slot != "default":
            ... # warn the user (overwrite)
    
    ... # todo -- save the game data to a file into the `index.toml` slot


def load_game(game, slot: int):
    """Sets the XML data files to load previously saved game data."""
    ...


def new_game(game, slot: int):
    """Overwrites a slot to be the default XML data."""
