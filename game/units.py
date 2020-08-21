# https://docs.python.org/3.6/library/__future__.html
from __future__ import division, print_function, unicode_literals

import cocos, pyglet

pyglet.resource.path.append('data/gfx')
pyglet.resource.reindex()


class LifeBar(cocos.layer.Layer):
    def __init__(self, max_value, width=100, height=2, value=None):
        super(LifeBar, self).__init__()
        self.max_value = max_value
        self.widget_width = width
        if value == None:
            value = max_value
        self.value = value

        # Build background and place it.
        self.oBackground = cocos.layer.ColorLayer(0, 0, 0, 255, (width + 2), (height + 2))
        self.add(self.oBackground, 0)

        # Build colored bar on top.
        self.oBar = cocos.layer.ColorLayer(0, 255, 0, 255, width, height)
        self.oBar.position = (1, 1)
        self.oBackground.add(self.oBar)

        # Add label.
        self.oLabel = cocos.text.Label(
            # '%d / %d' % (self.value, self.max_value),
            '%d' % self.value,
            font_name='Verdana',
            font_size=6,
            color=(0, 0, 0, 150),
            anchor_x='left',
            anchor_y='bottom'
        )
        self.oLabel.position = (0, 2)
        self.add(self.oLabel)

        # Add XP label.
        self.oXP = cocos.text.Label(
            '',
            font_name='Verdana',
            font_size=6,
            color=(200, 50, 0, 255),
            anchor_x='right',
            anchor_y='bottom'
        )
        self.oXP.position = (self.widget_width, 1)
        self.add(self.oXP)

    def on_enter(self):
        super(LifeBar, self).on_enter()
        self.updateWidth(self.value)

    def redrawBar(self):
        self.oBar._vertex_list.vertices[:] = [
            0, 0,
            0, self.oBar.height,
            self.oBar.width, self.oBar.height,
            self.oBar.width, 0
        ]

    def updateBar (self):
        if self.value < 0:
            self.value = 0
        nDiv = (float(self.value)/self.max_value)
        if nDiv >= 0.5:
            nGreen = 255
            nRed = int((1 - nDiv) * 2 * 255)
        else:
            nGreen = int(nDiv * 2 * 255)
            nRed = 255
        # Now draw it.
        self.oBar.color = (nRed, nGreen, 0)
        # self.oLabel.element.text = '%d / %d' % (self.value, self.max_value)
        self.oLabel.element.text = '%d' % self.value
        # And change width.
        self.updateWidth(self.value)
        # Add XP.
        if self.parent.aUnit['xp'] > 0:
            self.oXP.element.text = '*' * self.parent.aUnit['xp']

    def updateWidth(self, value):
        self.oBar.width = int(float(value) / self.max_value * self.widget_width)
        self.redrawBar()
