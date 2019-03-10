'''
Contains the parent class for screens to inherit from
'''

#Import needed modules
import os
import base64
from random import randrange
import pygame as pg
from pygame.locals import *
import modules.backend as be
from modules.display import display

class Gamestate(object):
    '''
    Contains variables and methods common to screens
    '''
    def __init__(self):
        '''
        Initialise various variables used to layout the screen
        and other variables that are set upon starting up the game
        '''
        self.done = False
        self.quit = False
        self.next_state = None
        self.persist = {}

        #Initalise static data values from backend
        self.tiles = be.tiles
        self.tile_side = be.side
        self.cycle = be.cycle
        self.grid_w = be.grid_w
        self.grid_h = be.grid_h
        self.viewablegrid_w = be.viewablegrid_w
        self.viewablegrid_h = be.viewablegrid_h
        self.bordergfx_raw = be.bordergfx
        self.options_btnimg_raw = be.options_btnimg
        self.seasongfx_summer_raw = be.seasongfx_summer
        self.seasongfx_autumn_raw = be.seasongfx_autumn
        self.seasongfx_winter_raw = be.seasongfx_winter
        self.seasongfx_spring_raw = be.seasongfx_spring
        self.tilestobuya = be.tilestobuya
        self.tilestobuyb = be.tilestobuyb
        self.structures = be.structures
        self.structure_tierupgtxt = be.structure_tierupgtxt
        self.flavors = be.flavors
        self.start_money = be.start_money
        self.sfx_money = be.sfx_money
        self.sfx_denied = be.sfx_denied
        self.sfx_clicked = be.sfx_clicked
        self.music_list = be.music_list

        #Initialise values for screen layout
        self.screen_width = display.get_width()
        self.screen_height = display.get_height()
        self.screen_centerx = self.screen_width/2
        self.screen_centery = self.screen_height/2
        self.box_w = 220
        self.box_h = 600
        self.box_borderdist = 30
        self.box_topleftx = self.screen_centerx - self.box_w/2
        self.box_toplefty = (self.screen_height - self.box_h)/2

        self.btn_w = 160
        self.btn_h = 60
        self.btn_topleftx = self.screen_centerx - self.btn_w/2
        self.btn_ydist = 80

        self.title_rect_centery = self.box_toplefty + 2*self.box_borderdist

        self.settingsstatinfo_xalignleft = self.box_topleftx+self.box_borderdist
        self.settingsstatinfo_xalignright = self.box_topleftx+self.box_w-self.box_borderdist
        self.statinfo_ydist = 30

        self.box_borderthick = 3
        self.btn_borderthick = 2

        self.msgbox_bordershift = 40

        self.msgbox_2line_ya = self.screen_centery + self.msgbox_bordershift/5
        self.msgbox_2line_yb = self.screen_centery + 4*self.msgbox_bordershift/5

        self.msgbox_3line_ya = self.screen_centery
        self.msgbox_3line_yb = self.msgbox_3line_ya + self.msgbox_bordershift/2
        self.msgbox_3line_yc = self.msgbox_3line_yb + self.msgbox_bordershift/2

        #Fonts
        self.font_title = pg.font.Font(os.path.join('resources/fonts', 'VT323-Regular.ttf'), 60)
        self.font_title2 = pg.font.Font(os.path.join('resources/fonts', 'VT323-Regular.ttf'), 48)
        self.font_header = pg.font.Font(os.path.join('resources/fonts', 'VT323-Regular.ttf'), 48)
        self.font_body = pg.font.Font(os.path.join('resources/fonts', 'VT323-Regular.ttf'), 30)
        self.font_body2 = pg.font.Font(os.path.join('resources/fonts', 'VT323-Regular.ttf'), 20)
        self.font_body3 = pg.font.Font(os.path.join('resources/fonts', 'VT323-Regular.ttf'), 24)
        self.font_body4 = pg.font.Font(os.path.join('resources/fonts', 'VT323-Regular.ttf'), 18)
        self.font_ibody = pg.font.Font(os.path.join('resources/fonts', 'VT323-Regular.ttf'), 24)
        self.font_ibody2 = pg.font.Font(os.path.join('resources/fonts', 'VT323-Regular.ttf'), 20)
        self.font_ibody3 = pg.font.Font(os.path.join('resources/fonts', 'VT323-Regular.ttf'), 16)
        self.font_ibody.set_italic(True)
        self.font_ibody2.set_italic(True)
        self.font_ibody3.set_italic(True)

        #Colors
        self.c_black = pg.Color('black')
        self.c_white = pg.Color('white')
        self.c_blue = pg.Color('dodgerblue')
        self.c_red = pg.Color(139, 0, 0)
        self.c_lightgray = pg.Color(169, 169, 169)
        self.c_darkgray = pg.Color(50, 50, 50)
        self.c_brown = pg.Color(64, 36, 25)

        #Black overlay for the background image of the player's farm when not on the Farm screen
        self.background_img_blackoverlay = pg.Surface((self.screen_width, self.screen_height))
        self.background_img_blackoverlay.fill(self.c_black)
        self.background_img_blackoverlay.set_alpha(150)

        #Close Button
        self.close_btntxt = self.font_body.render('x', True, self.c_black)
        self.close_btntxt_rect = self.close_btntxt.get_rect(midright=(self.box_topleftx+self.box_w-self.box_borderdist/2, self.box_toplefty+3*self.box_borderdist/4))

        #Back Button
        self.back_btntxt = self.font_body2.render('Back|Esc', True, self.c_black)
        self.back_btntxt_rect = self.back_btntxt.get_rect(midleft=(self.box_topleftx+self.box_borderdist/2, self.box_toplefty+3*self.box_borderdist/4))

        #Set event for when music playback ends
        pg.mixer.music.set_endevent(USEREVENT+2)

    def startup(self, persistent):
        '''
        Called when a state resumes being active.
        Allows information to be passed between states.

        persistent: a dict passed from state to state
        '''
        self.persist = persistent

    def tile_exists(self, tilename):
        '''
        Checks if a certain type of tile exists on the player's farm
        '''
        for row in self.persist['grid']:
            for tile in row:
                if self.tiles[tile].displayname == tilename:
                    return True

    def set_total_money_highest_lowest(self):
        '''
        Stores the values for the highest and lowest amount of money/highest amount of debt the player has achieved
        '''
        if self.persist['money'] > self.persist['total_money_highest']:
            self.persist['total_money_highest'] = self.persist['money']
        elif self.persist['money'] < self.persist['total_money_lowest']:
            self.persist['total_money_lowest'] = self.persist['money']

    def close_btn_farm(self, event):
        '''
        Close button functionality for going back to the farm
        '''
        if self.box_topleftx+self.box_w-self.box_borderdist/2-self.close_btntxt_rect.w < event.pos[0] < self.box_topleftx+self.box_w-self.box_borderdist/2 and self.box_toplefty+3*self.box_borderdist/4-self.close_btntxt_rect.h/5 < event.pos[1] < self.box_toplefty+3*self.box_borderdist/4+3*self.close_btntxt_rect.h/10:
            self.persist['buytile'] = None
            self.done = True
            self.next_state = 'Farm'
            self.play_sfx(self.sfx_clicked)

    def back_btn_options(self, event):
        '''
        Back button fuctionality for going back to Options
        '''
        if self.box_topleftx+self.box_borderdist/2 < event.pos[0] < self.box_topleftx+self.back_btntxt_rect.w+self.box_borderdist/2 and self.box_toplefty+3*self.box_borderdist/4-self.back_btntxt_rect.h/2 < event.pos[1] < self.box_toplefty+3*self.box_borderdist/4+self.back_btntxt_rect.h/2:
            self.done = True
            self.next_state = 'Options'
            self.play_sfx(self.sfx_clicked)

    def back_btn_farm(self, event):
        '''
        Back functionality for going back to the farm
        '''
        if self.box_topleftx+self.box_borderdist/2 < event.pos[0] < self.box_topleftx+self.back_btntxt_rect.w+self.box_borderdist/2 and self.box_toplefty+3*self.box_borderdist/4-self.back_btntxt_rect.h/2 < event.pos[1] < self.box_toplefty+3*self.box_borderdist/4+self.back_btntxt_rect.h/2:
            self.persist['buytile'] = None
            self.done = True
            self.next_state = 'Farm'
            self.play_sfx(self.sfx_clicked)

    def save_background_img(self):
        '''
        Saves an image of the farm to be used as a background img for other screens
        '''
        pg.image.save(display, os.path.join('resources/temp', 'background.png'))

    def play_sfx(self, sfx):
        '''
        Plays SFX
        '''
        sfx.set_volume(self.persist['sfxvol'])
        sfx.play()

    def set_musicvol(self):
        '''
        Sets the volume of what music is to be played
        '''
        pg.mixer.music.set_volume(self.persist['musicvol'])

    def play_next_music(self):
        '''
        Plays the next music track
        '''
        if self.persist['music_queue'][self.persist['current_music_index']] == self.persist['music_queue'][-1]:
            self.persist['music_queue'] = self.create_music_queue()
            self.persist['current_music_index'] = 0
        else:
            self.persist['current_music_index'] += 1
        self.play_music()

    def play_music(self):
        '''
        Plays music
        '''
        pg.mixer.music.load(self.persist['music_queue'][self.persist['current_music_index']])
        self.set_musicvol()
        pg.mixer.music.play()

    def create_music_queue(self):
        '''
        Creates a new music queue
        '''
        music_queue = []
        for music in self.music_list:
            random_int = randrange(len(self.music_list))
            while self.music_list[random_int] in music_queue:
                random_int = randrange(len(self.music_list))
            music_queue.append(self.music_list[random_int])
        return music_queue

    def save(self,
             grid,
             grid_tilecycle,
             money,
             timer,
             days_total,
             days_seasonyear,
             year,
             plowingtiles_dict,
             sfxvol,
             musicvol,
             total_money_earned,
             total_money_spent,
             total_money_highest,
             total_money_lowest
            ):
        '''
        Saves the game
        '''
        #Open savefile
        savefile = open(os.path.join('savefile'), 'wb')

        #Encode grids
        grid_list = []
        grid_tilecycle_list = []
        for row in range(self.grid_h):
            for col in range(self.grid_w):
                grid_list.append(grid[row][col])
                grid_tilecycle_list.append(str(grid_tilecycle[row][col]))
        grid_string = ' '.join(grid_list)
        grid_tilecycle_string = ' '.join(grid_tilecycle_list)
        b64_grid = base64.b64encode(bytes(grid_string))
        b64_grid_tilecycle = base64.b64encode((bytes(grid_tilecycle_string)))

        #Encode money
        b64_money = base64.b64encode(bytes(money))

        #Encode timer
        b64_timer = base64.b64encode(bytes(timer))

        #Encode days_total
        b64_days_total = base64.b64encode(bytes(days_total))

        #Encode days_seasonyear
        b64_days_seasonyear = base64.b64encode(bytes(days_seasonyear))

        #Encode year
        b64_year = base64.b64encode(bytes(year))

        #Encode plowingtiles_dict
        plowingtile_keylist = []
        plowingtile_valuelist = []
        for key, values in plowingtiles_dict.iteritems():
            plowingtile_keylist.append(key)
            for value in values:
                plowingtile_valuelist.append(str(value))
        plowingtile_keystring = ' '.join(plowingtile_keylist)
        plowingtile_valuestring = ' '.join(plowingtile_valuelist)
        b64_plowingtiles_dict_keys = base64.b64encode(bytes(plowingtile_keystring))
        b64_plowingtiles_dict_values = base64.b64encode(bytes(plowingtile_valuestring))

        #Encode sfxvol
        b64_sfxvol = base64.b64encode(bytes(sfxvol))

        #Encode musicvol
        b64_musicvol = base64.b64encode(bytes(musicvol))

        #Encode total_money_earned
        b64_total_money_earned = base64.b64encode(bytes(total_money_earned))

        #Encode total_money_spent
        b64_total_money_spent = base64.b64encode(bytes(total_money_spent))

        #Encode total_money_highest
        b64_total_money_highest = base64.b64encode(bytes(total_money_highest))

        #Encode total_money_lowest
        b64_total_money_lowest = base64.b64encode(bytes(total_money_lowest))

        #Write to savefile
        savefile.write(b64_grid+'\n')
        savefile.write(b64_grid_tilecycle+'\n')
        savefile.write(b64_money+'\n')
        savefile.write(b64_timer+'\n')
        savefile.write(b64_days_total+'\n')
        savefile.write(b64_days_seasonyear+'\n')
        savefile.write(b64_year+'\n')
        savefile.write(b64_plowingtiles_dict_keys+'\n')
        savefile.write(b64_plowingtiles_dict_values+'\n')
        savefile.write(b64_sfxvol+'\n')
        savefile.write(b64_musicvol+'\n')
        savefile.write(b64_total_money_earned+'\n')
        savefile.write(b64_total_money_spent+'\n')
        savefile.write(b64_total_money_highest+'\n')
        savefile.write(b64_total_money_lowest+'\n')
        savefile.close()

    def get_event(self, event):
        '''
        Handles a single event passed by the Game object
        '''
        pass

    def update(self, dt):
        '''
        Updates the state; called by the Game object once per frame

        dt: time since last frame
        '''
        pass

    def draw(self, surface):
        '''
        Draw everything to the screen
        '''
        pass
