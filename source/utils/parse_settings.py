"""This module provides accessability and functionality for parsing the ``.TOML`` settings file."""

from typing import BinaryIO, Any
import tomli



class Settings:
    """Gives a mothodology to be able to load and parse values from the ``settings.toml`` file."""
    _file = 'settings.toml'

    def __init__(self, game) -> None:
        self.game = game

    def get_graphics(self) -> dict[str, Any]:
        """Retrieves the graphical settings assigned for the application"""
        with open(self._file, 'rb') as config:
            _config = tomli.load(config)
        _dict = _config['Graphics']
        return _dict