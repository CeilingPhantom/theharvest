'''
For optimal source code reading and editing experience, view
with 120 word wrap column, in a text editor like Sublime Text

 _____ _            _   _                           _
|_   _| |          | | | |                         | |
  | | | |__   ___  | |_| | __ _ _ ____   _____  ___| |_
  | | | '_ \ / _ \ |  _  |/ _` | '__\ \ / / _ \/ __| __|
  | | | | | |  __/ | | | | (_| | |   \ V /  __/\__ \ |_
  \_/ |_| |_|\___| \_| |_/\__,_|_|    \_/ \___||___/\__|

------------------------------------------------------------

The Harvest v1.00

The Harvest developed in 2017, by James Luo

Licence agreement for The Harvest is provided

To make an enquiry, or report a bug,
contact James via jameshcluo@gmail.com

'''
#Import needed modules
import os
import sys
import pygame as pg
from pygame.locals import *

#Set icon and display
pg.display.set_icon(pg.image.load(os.path.join('resources/imgs/tiles', 'wheat1_0.png')))
from modules.Display import display

#Import screens
from modules.Mainmenu import Mainmenu
from modules.Farm import Farm
from modules.Tile import Tile
from modules.Options import Options
from modules.Settings import Settings
from modules.Stats import Stats
from modules.Info import Info
from modules.Tutorial import Tutorial

class Game(object):
    '''
    Responsible for managing which game state is active and
    keeping it updated. Manages the event queue, framerate,
    updating of the display and drawing to the display;
    run method serves as the 'game loop'
    '''
    def __init__(self, screen, states, start_state):
        '''
        screen: the display surface
        states: a dict mapping state names to GameState objects
        start_state: name of the first active state
        '''
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 45
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        '''
        Handles events for the current state
        '''
        for event in pg.event.get():
            self.state.get_event(event)

    def flip_state(self):
        '''
        Switch to the next game state
        '''
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        '''
        Check for state flip and update active state

        dt: milliseconds since last frame
        '''
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        '''
        Handles what needs to be drawn on
        the display for the current state
        '''
        self.state.draw(self.screen)

    def run(self):
        '''
        Pretty much the entirety of the game's runtime
        will be spent inside this while loop
        '''
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('The Harvest')
    screens = {'Mainmenu': Mainmenu(),
               'Farm': Farm(),
               'Tile': Tile(),
               'Options': Options(),
               'Settings': Settings(),
               'Stats': Stats(),
               'Info': Info(),
               'Tutorial': Tutorial()
              }
    game = Game(display, screens, 'Mainmenu')
    game.run()
    pg.quit()
    sys.exit()
