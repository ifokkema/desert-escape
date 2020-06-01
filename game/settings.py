import os
import json

# Defining defaults.
WINDOW_WIDTH     = 1200
WINDOW_HEIGHT    = 800
WINDOW_SPEED_MAX = 100  # px/sec (max scrolling speed)


# The basic unit that players start with.
basic_unit = {
    'body': ['humans', 0],
    'turret_primary': ['humans', 0],
    'turret_secondary': [],
    'xp': 0,
    'xp_shots': 0,
}


# Savegame variables.
SAVEGAMES = {}
SAVEGAMES_FILE = os.path.join(os.path.dirname(__file__), 'savegames.json')


def deCreateNewPlayer(name):
    global SAVEGAMES
    # Creates a new player in the SAVEGAMES array,
    #  and then has the savegames written to disk.
    if name in SAVEGAMES['players']:
        raise ValueError('Player already exists!')

    SAVEGAMES['players'][name] = {
        'units': [basic_unit, basic_unit, basic_unit, basic_unit, basic_unit, basic_unit],
        'levels_completed': [],
    }
    SAVEGAMES['current_player'] = name
    deSaveSaveGames()
    return True


def deInitSaveGames():
    global SAVEGAMES, SAVEGAMES_FILE
    # Load our savegames.
    try:
        fp = open(SAVEGAMES_FILE, mode='r', encoding='UTF-8')
    except FileNotFoundError:
        open(SAVEGAMES_FILE, 'a').close()
        fp = open(SAVEGAMES_FILE, mode='r', encoding='UTF-8')

    try:
        SAVEGAMES = json.load(fp)
    except json.decoder.JSONDecodeError as e:
        SAVEGAMES = {}
    fp.close()

    # If SAVEGAMES is missing keys, add them.
    if 'current_player' not in SAVEGAMES:
        SAVEGAMES['current_player'] = ''
    if 'players' not in SAVEGAMES:
        SAVEGAMES['players'] = {}
    if SAVEGAMES['current_player'] not in SAVEGAMES['players'].keys():
        if len(SAVEGAMES['players']) > 0:
            SAVEGAMES['current_player'] = list(SAVEGAMES['players'].keys())[0]
        else:
            deCreateNewPlayer('Default')


def deSaveSaveGames():
    global SAVEGAMES, SAVEGAMES_FILE
    try:
        fp = open(SAVEGAMES_FILE, mode='w', encoding='UTF-8')
        json.dump(SAVEGAMES, fp, sort_keys=True, indent=4)
    except:
        raise OSError("Couldn't save SaveGame state!")


if len(SAVEGAMES) == 0:
    deInitSaveGames()
