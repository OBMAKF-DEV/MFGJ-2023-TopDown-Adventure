from typing import Type

OBJECTS = {
    'resources/maps/test_map.txt': {
        'doors': {(14, 3): ({  # test_map
            'location': 'resources/maps/test_map.txt',
            'position': (14, 3),
            'destination': 'resources/maps/test_map2.txt'}, (1, 1))},
        'containers': {(13, 4): ({
            'items': [{'name': 'Apple', 'image': None}],
            'keys': [{'name': 'key', 'image': None}]
        })}
    },
    
    'resources/maps/test_map2.txt': {
        'doors': {(0, 1): ({  # test_map2
            'location': 'resources/maps/test_map2.txt',
            'position': (0, 1),
            'destination': 'resources/maps/test_map.txt'}, (13, 3))},
    },
}
