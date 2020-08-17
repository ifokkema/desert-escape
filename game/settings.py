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


def deGetUnitLocations(aUnits):
    # Based on the unit types and their strengths, calculate which unit goes where.
    aXP = []
    aPositions = []  # Positions of units, in the order in which the units were given.
    nXOffset = 350   # Where to start putting units.
    nYDistance = 40  # Y distance between units.

    if (len(aUnits) not in (6, 3, 2, 1)):
        print("Player's savegame is currupt; unit count is not 6, 3, 2, or 1.")
        exit(1)

    # Python's lists/dicts/tuples are very frustrating if you come from PHP...
    # I would just collect the unit's keys and their values, then sort on the values and keep the keys, but no...
    # Even looping over a simple list, keeping index, is super complicated, and requires the list to be converted.
    for (nKey, aUnit) in enumerate(aUnits):
        aXP.append((nKey, ((aUnit['xp'] * 100) + aUnit['xp_shots'])) * (1 if (aUnit['body'][0] == 'humans') else (10 if (aUnit['body'][0] == 'tanks') else 100)))

    # "sort" the XP list, so I know in which order I need to place these units.
    aXP = sorted(aXP, key=lambda x: x[1], reverse=True)
    # [(index, XP), (index, XP), (index, XP), ...]

    if len(aUnits) == 6:
        aYs = [-0.5, 0.5, -1.5, 1.5, -2.5, 2.5]
        i = 0
        for (nKey, nXP) in aXP:
            # nKey here is the key in the aUnits, not the current key (i).
            if i == 2 or i == 4:
                nXOffset -= (0.5 * nYDistance)
            aPositions.append((nKey, nXOffset, (WINDOW_HEIGHT/2) + (aYs[i]) * nYDistance))
            i += 1

    elif len(aUnits) == 3:
        aYs = [0, -2.5, 2.5]
        i = 0
        for (nKey, nXP) in aXP:
            # nKey here is the key in the aUnits, not the current key (i).
            if i == 1:
                nXOffset -= nYDistance
            aPositions.append((nKey, nXOffset, (WINDOW_HEIGHT/2) + (aYs[i]) * nYDistance))
            i += 1

    elif len(aUnits) == 2:
        i = 0
        for (nKey, nXP) in aXP:
            # nKey here is the key in the aUnits, not the current key (i).
            if i == 1:
                nXOffset /= 2
            aPositions.append((nKey, nXOffset, (WINDOW_HEIGHT/2)))
            i += 1

    else:
        aPositions.append((0, nXOffset, (WINDOW_HEIGHT/2)))

    return aPositions


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
