"""This module provides accessability and functionality for parsing the ``.TOML`` settings file."""

from typing import BinaryIO, Any
import tomli


def toml_loader(func):
    """Simple toml decorator function for parsing files."""
    def wrapper(filename, header, **kwargs):
        """Inner Wrapper function."""
        class OpenToml(object):
            """Context-Manager for handling the open binary stream."""
            _file: BinaryIO

            def __init__(self, _filename):
                self.filename = _filename

            def __enter__(self) -> BinaryIO:
                self._file = open(self.filename, 'rb')
                return self._file

            def __exit__(self, exc_type, exc_val, exc_tb):
                self._file.close()

        func(**kwargs) # execute the decorated function.
        

        with OpenToml(filename) as file:
            _config = tomli.load(file)
            try:
                return _config[header]
            except KeyError as exc:
                raise KeyError(exc) from exc
    return wrapper


class Settings:
    """Gives a mothodology to be able to load and parse values from the ``settings.toml`` file."""
    _file = 'settings.toml'

    def __init__(self, game) -> None:
        self.game = game

    def get_graphics(self) -> dict[str, Any]:
        """Retrieves the graphical settings assigned for the application"""
        _dict = self._get_header(self._file, 'Graphics')
        return _dict

    @toml_loader
    def _get_header(self, file: str | bytes, header: str) -> dict | None:
        """Retrieves a parsed dictionary from a specific header.

        Returns:
            dict:   The settings values base off a header topic
        """
        print(f"Accessing `{header}` from {file}")
        return
