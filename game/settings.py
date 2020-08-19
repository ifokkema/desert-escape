import os
import json

# Defining defaults.
WINDOW_WIDTH     = 1200
WINDOW_HEIGHT    = 800
WINDOW_SPEED_MAX = 100  # px/sec (max scrolling speed)


XP_LEVELS = [
    {  # Level 0.
        'chance_to_hit'   : 0.75,  # Your chance to hit your target, when your target is at your maximum range.
        'damage_factor'   : 0.75,  # The damage you're doing is multiplied by this factor.
        'timeout_factor'  : 1.25,  # The waiting time until the next shot is multiplied by this much.
        'rotation_factor' : 0.75,  # Your turret's rotation speed is multiplied by this factor.
        'hitpoints_factor': 0.75,  # Your maximum health is multiplied by this factor.
        'maximum_shots'   : 10,    # After this many shots, you are upgraded.
    },
    {  # Level 1.
        'chance_to_hit'   : 0.80,  # Your chance to hit your target, when your target is at your maximum range.
        'damage_factor'   : 0.80,  # The damage you're doing is multiplied by this factor.
        'timeout_factor'  : 1.20,  # The waiting time until the next shot is multiplied by this much.
        'rotation_factor' : 0.80,  # Your turret's rotation speed is multiplied by this factor.
        'hitpoints_factor': 0.80,  # Your maximum health is multiplied by this factor.
        'maximum_shots'   : 20,    # After this many shots, you are upgraded.
    },
    {  # Level 2.
        'chance_to_hit'   : 0.85,  # Your chance to hit your target, when your target is at your maximum range.
        'damage_factor'   : 0.85,  # The damage you're doing is multiplied by this factor.
        'timeout_factor'  : 1.15,  # The waiting time until the next shot is multiplied by this much.
        'rotation_factor' : 0.85,  # Your turret's rotation speed is multiplied by this factor.
        'hitpoints_factor': 0.85,  # Your maximum health is multiplied by this factor.
        'maximum_shots'   : 30,    # After this many shots, you are upgraded.
    },
    {  # Level 3.
        'chance_to_hit'   : 0.90,  # Your chance to hit your target, when your target is at your maximum range.
        'damage_factor'   : 0.90,  # The damage you're doing is multiplied by this factor.
        'timeout_factor'  : 1.10,  # The waiting time until the next shot is multiplied by this much.
        'rotation_factor' : 0.90,  # Your turret's rotation speed is multiplied by this factor.
        'hitpoints_factor': 0.90,  # Your maximum health is multiplied by this factor.
        'maximum_shots'   : 50,    # After this many shots, you are upgraded.
    },
    {  # Level 4.
        'chance_to_hit'   : 0.95,  # Your chance to hit your target, when your target is at your maximum range.
        'damage_factor'   : 0.95,  # The damage you're doing is multiplied by this factor.
        'timeout_factor'  : 1.05,  # The waiting time until the next shot is multiplied by this much.
        'rotation_factor' : 0.95,  # Your turret's rotation speed is multiplied by this factor.
        'hitpoints_factor': 0.95,  # Your maximum health is multiplied by this factor.
        'maximum_shots'   : 75,    # After this many shots, you are upgraded.
    },
    {  # Level 5.
        'chance_to_hit'   : 1,     # Your chance to hit your target, when your target is at your maximum range.
        'damage_factor'   : 1,     # The damage you're doing is multiplied by this factor.
        'timeout_factor'  : 1,     # The waiting time until the next shot is multiplied by this much.
        'rotation_factor' : 1,     # Your turret's rotation speed is multiplied by this factor.
        'hitpoints_factor': 1,     # Your maximum health is multiplied by this factor.
        'maximum_shots'   : 0,     # You are not upgraded.
    },
]


# Define the parts we need to build units.
BODIES = {
    'humans': [
        {  # Human 0 (no armor, no helmet).
            'type': 'ground',
            'subtype': 'human',
            'image_us': 'human_body_1_us.png',
            'image_them': 'human_body_1_them.png',
            'image_sheet_width': 12,
            'height': 2,
            'hitpoints': 100,
            'turrets': {
                'primary': {
                    'location': [0, 6],
                    'supported': {
                        'humans': [0, 1],
                    },
                },
                'secondary': {},
            },
            'death_animation_us': 'human_1_death_ani_us.png',
            'death_animation_them': 'human_1_death_ani_them.png',
            'death_animation_sheet_width': 5,
            'dead_image_us': 'human_1_dead_us.png',
            'dead_image_them': 'human_1_dead_them.png',
        },
        {}, # Armor, no helmet.
        {}, # Armor, helmet.
    ],
    'tanks': [
        {  # Tank 0.
            'type': 'ground',                      # { ground | air }
            'subtype': 'tank',                     # { mine | human | tank | bunker } | { drone | helicopter }
            'image_us': 'tank_body_1_us.png',      # Image of body, if part of our team.
            'image_them': 'tank_body_1_them.png',  # Image of body, if part of their team.
            'image_sheet_width': 1,                # For animation, the size of the sprite sheet.
            'height': 5,                           # For determining the shadow's offset. { 0 - 10 }
            'hitpoints': 1000,                     # Amount of damage this body can take.
            'turrets': {
                'primary': {
                    'location': [0, 10],           # Location on the body where to place the center of the turret.
                    'supported': {
                        'tanks': [0, 1],
                    },
                },
                'secondary': {},
            },
            # Animations for destruction (no loop), and images for destroyed state.
            'death_animation_us': 'tank_body_1_death_ani_us.png',
            'death_animation_them': 'tank_body_1_death_ani_them.png',
            'death_animation_sheet_width': 12,
            'dead_image_us': 'tank_body_1_dead_us.png',
            'dead_image_them': 'tank_body_1_dead_them.png',
        },
    ],
    'drones': [
        {}
    ],
}


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
