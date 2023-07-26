from typing import BinaryIO, Any
import tomli


def toml_loader(func):
    """Simple toml decorator function for parsing files."""
    def wrapper(filename, header, **kwargs):
        class OpenToml:
            _file: BinaryIO

            def __init__(self, _filename):
                self.filename = _filename

            def __enter__(self) -> BinaryIO:
                self._file = open(self.filename, 'rb')
                return self._file

            def __exit__(self, exc_type, exc_val, exc_tb):
                self._file.close()

        func(**kwargs)

        with OpenToml(filename) as file:
            _config = tomli.load(file)
            try:
                return _config[header]
            except KeyError as exc:
                raise KeyError(exc) from exc
    return wrapper


class Settings:
    _file = 'settings.toml'

    def __int__(self, game):
        self.game = game

    def get_graphics(self) -> dict:
        return self._get_header(self._file, 'Graphics')

    def get_graphic(self, __kw) -> Any:
        try:
            return self.get_graphics()[__kw]
        except KeyError as exc:
            raise KeyError(exc) from exc

    @toml_loader
    def _get_header(self, file, header) -> Any | None:
        return

