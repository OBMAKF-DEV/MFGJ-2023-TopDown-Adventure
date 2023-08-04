from source.items import KeyItem, Item
import xml.etree.ElementTree as element
import tomli
import shutil
import os


def save_game(game, slot: int, save_name: str):
    """Provides access for saving game data to a save file via a game slot.
    
    Args:
        game (Game): The main game.
        slot (int): The slot to save the game data to.
        save_name (str): The name to assign the save files to.
    """
    print(game.player.inventory.items)
    DATA_FILES = ['test_map.xml', 'test_map2.xml', 'test_map2b.xml', 'cave_entrance.xml']
    with open('resources/maps/data/saves/index.toml', 'rb') as indexer:
        _data = tomli.load(indexer)['slots']
        slots = [_data[str(i)] for i in range(1, 5)]
        open_slot = slots[slot-1]
        game.savefile = save_name
        game.save_slot = slot-1
    
    # change the indexer value
    slots[slot-1] = save_name
    with open('resources/maps/data/saves/index.toml', 'w') as file:
        file.write('[slots]\n')
        for i, save in enumerate(slots):
            file.write(f'{i+1} = "{save}"\n')
    
    if not os.path.isdir(f'resources/maps/data/saves/{save_name}'):
        os.mkdir(f'resources/maps/data/saves/{save_name}')  # make the directory
    
    # save the datafiles
    
    for filename in DATA_FILES:
        shutil.copy2(
            f'resources/maps/data/{filename}',
            f'resources/maps/data/saves/{save_name}/{filename}')
    
    # write the current player data
    with open(f'resources/maps/data/saves/{save_name}/player_data.xml', 'w') as player_data:
        if game.player.equipped is not None:
            player_data.write(f'<player equipped = "{game.player.equipped}">\n')
        else:
            player_data.write(f'<player>\n')
        player_data.write(
            f'    <stats>\n' +
            f'        <health current="{game.player.health}" max="{game.player.max_health}"/>\n' +
            f'        <damage dmg="{game.player.damage}"/>\n' +
            f'    </stats>\n' +
            f'    <inventory>\n')
        if len(game.player.inventory.items) > 0:
            player_data.write('        <items>\n')
            for item in game.player.inventory.items:
                if isinstance(item, KeyItem):
                    player_data.write(f'            <object type="KeyItem" name="{item.name}" image="{item.image}"/>\n')
                    continue
                player_data.write(f'            <object type="Item" name="{item.name}" image="{item.image}"/>\n')
            player_data.write('        </items>\n')
        else:
            player_data.write('        <items/>\n')
        player_data.write('    </inventory>\n</player>')
    shutil.copy(
        f'resources/maps/data/saves/{save_name}/player_data.xml',
        'resources/maps/data/player_data.xml'
    )


def load_game(game, slot: int):
    """Sets the XML data files to load previously saved game data."""
    DATA_FILES = ['test_map.xml', 'test_map2.xml', 'test_map2b.xml', 'cave_entrance.xml', 'player_data.xml']
    print(str(slot))
    # set data files to the value stored in the slot
    with open('resources/maps/data/saves/index.toml', 'rb') as indexer:
        _data = tomli.load(indexer)['slots']
        game.save_slot = slot - 1
        game.savefile = _data[str(slot)]
    
    # load the data files
    try:
        for filename in DATA_FILES:
            shutil.copy2(
                f'resources/maps/data/saves/{game.savefile}/{filename}',
                f'resources/maps/data/{filename}')
    except FileNotFoundError as exc:
        raise FileNotFoundError(exc) from exc
    
    tree = element.parse(f'resources/maps/data/saves/{game.savefile}/player_data.xml')
    element_data = tree.getroot()
    
    # set the player attribute values.
    try:
        game.player.equipped = element_data.find('.//player').get('equipped')
    except AttributeError:
        game.player.equipped = None
    health = element_data.find('.//health')
    game.player.health = int(health.get('current'))
    game.player.max_health = int(health.get('max'))
    game.player.damage = int(element_data.find('.//damage').get('dmg'))
    _items = element_data.findall('.//object')
    items = []
    
    # set the player inventory items
    for item in _items:
        name = item.get('name')
        image = item.get('image') if item.get('image') != 'None' else None
        if item.get('type').lower() == 'keyitem':
            items.append(KeyItem(name, image, None))
        elif item.get('type').lower() == 'item':
            items.append(Item(name, None))
        print(items)
    game.player.inventory.items = items
    game.map.load('test_map')
