# https://docs.python.org/3.6/library/__future__.html
from __future__ import division, print_function, unicode_literals

from cocos.menu import *
from cocos.layer import *

# My own files.
from game.units import *


class MenuScene(cocos.scene.Scene):
    def __init__(self):
        super(MenuScene, self).__init__()
        self.add(MainMenu(), z=2)


class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Desert Escape')

        # Overriding the font settings.
        # Title font, Unlearned 2 by Brian Kent.
        # https://www.dafont.com/unlearned.font
        self.font_title['font_name'] = 'Unlearned 2 BRK'
        self.font_title['font_size'] = 80

        # Items font, Zeroes Three by Ray Larabie.
        # https://www.dafont.com/zero-threes.font
        self.font_item['font_name'] = 'Zeroes Three',
        self.font_item['color'] = (200, 200, 200, 200)
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Zeroes Three'
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item_selected['font_size'] = 34

        # Add the menu items.
        aPlayers = list(SAVEGAMES['players'].keys())
        items = [
            MultipleMenuItem('Current Player: ', self.choose_player, aPlayers,
                             aPlayers.index(SAVEGAMES['current_player'])),
            MenuItem('Create new player', self.create_new_player),
            ToggleMenuItem('Sound: ', self.toggle_sound, True),
            MenuItem('Quit', self.on_quit),
        ]

        # I don't want the menu vertically centered, so the only choice Cocos seems to give me,
        #  is to create a fixedPositionMenuLayout.
        self.create_menu(items, layout_strategy=fixedPositionMenuLayout(
            [(WINDOW_WIDTH / 2, 200),
             (WINDOW_WIDTH / 2, 150),
             (WINDOW_WIDTH / 2, 100),
             (WINDOW_WIDTH / 2, 50)]))

    def choose_player(self, value):
        SAVEGAMES['current_player'] = list(SAVEGAMES['players'].keys())[value]
        print("We'll be playing as user ", SAVEGAMES['current_player'])
        deSaveSaveGames()

    def create_new_player(self):
        # Adds a new Menu to the layer, meant for the user to enter their name.
        title = cocos.text.Label(
            'Type your player name',
            font_size=40,
            font_name='Zeroes Three',
            color=(255, 255, 255, 255),
            anchor_x=CENTER
        )
        # Place title just below our game's title.
        title.position = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.25)
        self.parent.add(ColorLayer(0, 0, 0, 200).add(title), z=3, name='NewPlayerBackground')
        self.parent.add(NewPlayerMenu(), z=4)
        return True

    def on_quit(self):
        # Method has to be named this way, the Escape key maps to it.
        pyglet.app.exit()

    def toggle_sound(self, value):
        # STUB.
        print("Sound toggle: ", value)
        return True


class NewPlayerMenu(Menu):
    def __init__(self):
        super(NewPlayerMenu, self).__init__('')

        self.player_name = ''

        # Overriding the font settings for items.
        self.font_item['font_name'] = 'Zeroes Three',
        self.font_item['color'] = (200, 200, 200, 200)
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Zeroes Three'
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item_selected['font_size'] = 34

        self.create_menu([
            EntryMenuItem('', self.on_typing, '<NewPlayer>', max_length=15),
            MenuItem('OK', self.on_confirm),
            MenuItem('Cancel', self.on_quit),
        ])

    def on_confirm(self):
        # User has added their name, now we'll store it.
        if len(self.player_name) == 0:
            pass

        elif self.player_name in SAVEGAMES['players']:
            # Player name already exists!
            label = cocos.text.Label(
                'Player name ' + self.player_name + ' already exists!',
                font_size=20,
                font_name='Zeroes Three',
                color=(255, 150, 150, 255),
                anchor_x=CENTER
            )
            # Place label below this layer's label, which is below the game's title.
            label.position = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.4)
            label.do(FadeOut(3) + CallFunc(label.kill))
            self.parent.get('NewPlayerBackground').add(label)
            return False

        else:
            print('Creating a new user: ', self.player_name)
            if deCreateNewPlayer(self.player_name):
                # Reload the entire Menu.
                director.replace(MenuScene())
                return True

    def on_typing(self, value):
        self.player_name = value

    def on_quit(self):
        # Method has to be named this way, the Escape key maps to it.
        # User wants to cancel.
        self.parent.remove('NewPlayerBackground')
        self.kill()
