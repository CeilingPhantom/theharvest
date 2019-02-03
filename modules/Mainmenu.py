'''
Manages the Mainmenu screen, which is a splash screen

Also initialises variables
'''

#Import needed modules
import pygame as pg
from pygame.locals import *
import modules.Backend as be
from modules.Gamestate import Gamestate

class Mainmenu(Gamestate):
    def __init__(self):
        super(Mainmenu, self).__init__()

        #Initalise data values that need to be passed between states
        self.persist['grid'] = be.grid
        self.persist['grid_tilecycle'] = be.grid_tilecycle
        self.persist['viewablegrid_topleft'] = {'x': 0, 'y': 0}   #save topleft into savefile
        self.persist['money'] = be.money
        self.persist['select_col'] = None
        self.persist['select_row'] = None
        self.persist['buytile'] = None
        self.persist['timer'] = be.timer
        self.persist['days_total'] = be.days_total
        self.persist['days_seasonyear'] = be.days_seasonyear
        self.persist['year'] = be.year
        self.persist['plowingtiles_dict'] = be.plowingtiles_dict
        self.persist['plowingtile_counter'] = 0
        self.persist['plowingtimer'] = 0
        self.persist['current_season'] = None
        self.persist['select_sidebar_tilestab1'] = True
        self.persist['greenhouse_tiles_season_all'] = None
        self.persist['shed_tiles_reduced_plow'] = None
        self.persist['silo_tiles_livestock_can'] = None
        self.persist['greenhouse_affectedtiles_lvl3'] = None
        self.persist['shed_affectedtiles_lvl3'] = None
        self.persist['silo_affectedtiles_lvl3'] = None
        self.persist['tile_imgs'] = None
        self.persist['sfxvol'] = be.sfxvol
        self.persist['musicvol'] = be.musicvol
        self.persist['total_money_earned'] = be.total_money_earned
        self.persist['total_money_spent'] = be.total_money_spent
        self.persist['total_money_highest'] = be.total_money_highest
        self.persist['total_money_lowest'] = be.total_money_lowest
        self.persist['autosavetimer'] = 0
        self.persist['saved'] = False
        self.persist['music_queue'] = self.create_music_queue()
        self.persist['current_music_index'] = 0

        self.title = self.font_title.render('The Harvest', True, self.c_black)
        self.title_rect = self.title.get_rect(center=(self.screen_centerx, self.screen_centery))

        self.subtitle_y = self.screen_height/2 + self.title_rect_centery
        self.subtitle = self.font_body.render('Press Anywhere to Start', True, self.c_black)
        self.subtitle_rect = self.subtitle.get_rect(center=(self.screen_centerx, self.subtitle_y))

        self.play_music()

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

        elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
            self.done = True
            self.next_state = 'Farm'
            self.play_sfx(self.sfx_clicked)

        elif event.type == USEREVENT+2:
            self.play_next_music()

    def draw(self, surface):
        #Draw background
        surface.fill(self.c_white)

        #Draw text
        surface.blit(self.title, self.title_rect)
        surface.blit(self.subtitle, self.subtitle_rect)
