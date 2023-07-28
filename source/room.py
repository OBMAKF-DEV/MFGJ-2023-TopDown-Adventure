import tomli
from typing import Any

# Todo - design Room class and move settings across...
#      ...

class Room:
    data = {}
    
    def __init__(self, game, name: str, map_file: str | bytes, object_data_file: str | bytes):
        self.game = game
        self.name = name
        self.map_file = map_file
        self.object_data_file = object_data_file

    def load_data(self, _key: str) -> Any:
        with open(self.object_data_file, 'rb') as _data_file:
            _data = tomli.load(_data_file)
        self.data = _data[self.name]
        return _data[_key]
