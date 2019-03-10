'''
Manages the Tutorial and Help screen
'''

import os
import pygame as pg
from pygame.locals import *
from modules.gamestate import Gamestate

class Tutorial(Gamestate):
    def __init__(self):

        super(Tutorial, self).__init__()

        self.title = (self.font_title2.render('Tutorial', True, self.c_black), self.font_title2.render('and Help', True, self.c_black))
        self.title_rect = (self.title[0].get_rect(center=(self.screen_centerx, self.title_rect_centery)), self.title[1].get_rect(center=(self.screen_centerx, self.title_rect_centery+self.title[0].get_height())))

        self.controlstxt_rect_centery = (self.title_rect[1].centery+2*self.statinfo_ydist,
                                         self.title_rect[1].centery+3*self.statinfo_ydist-self.statinfo_ydist/4,
                                         self.title_rect[1].centery+4*self.statinfo_ydist-self.statinfo_ydist/2,
                                         self.title_rect[1].centery+5*self.statinfo_ydist-self.statinfo_ydist,
                                         self.title_rect[1].centery+6*self.statinfo_ydist-5*self.statinfo_ydist/4,
                                         self.title_rect[1].centery+7*self.statinfo_ydist-3*self.statinfo_ydist/2,
                                         self.title_rect[1].centery+8*self.statinfo_ydist-7*self.statinfo_ydist/4,
                                         self.title_rect[1].centery+9*self.statinfo_ydist-9*self.statinfo_ydist/4,
                                         self.title_rect[1].centery+10*self.statinfo_ydist-11*self.statinfo_ydist/4,
                                         self.title_rect[1].centery+11*self.statinfo_ydist-13*self.statinfo_ydist/4
                                        )
        self.yourfarmtxt_rect_centery = (self.controlstxt_rect_centery[9]+2*self.statinfo_ydist,
                                         self.controlstxt_rect_centery[9]+3*self.statinfo_ydist-self.statinfo_ydist/4,
                                         self.controlstxt_rect_centery[9]+4*self.statinfo_ydist-self.statinfo_ydist/2,
                                         self.controlstxt_rect_centery[9]+5*self.statinfo_ydist-self.statinfo_ydist,
                                         self.controlstxt_rect_centery[9]+6*self.statinfo_ydist-5*self.statinfo_ydist/4,
                                         self.controlstxt_rect_centery[9]+7*self.statinfo_ydist-3*self.statinfo_ydist/2,
                                         self.controlstxt_rect_centery[9]+8*self.statinfo_ydist-2*self.statinfo_ydist,
                                         self.controlstxt_rect_centery[9]+9*self.statinfo_ydist-9*self.statinfo_ydist/4,
                                         self.controlstxt_rect_centery[9]+10*self.statinfo_ydist-11*self.statinfo_ydist/4
                                        )

        self.controlstxt = (self.font_body.render('Controls', True, self.c_black),
                            self.font_body2.render('Left Mouse Button', True, self.c_black),
                            self.font_body4.render('Associated action', True, self.c_black),
                            self.font_body4.render('To Object screen', True, self.c_black),
                            self.font_body2.render('Right Mouse Button', True, self.c_black),
                            self.font_body4.render('Deselect tile', True, self.c_black),
                            self.font_body2.render('Escape', True, self.c_black),
                            self.font_body4.render('Back a screen', True, self.c_black),
                            self.font_body4.render('To Options', True, self.c_black),
                            self.font_body4.render('Deselect tile', True, self.c_black)
                           )
        self.controlstxt_rect = (self.controlstxt[0].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.controlstxt_rect_centery[0])),
                                 self.controlstxt[1].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.controlstxt_rect_centery[1])),
                                 self.controlstxt[2].get_rect(midright=(self.settingsstatinfo_xalignright, self.controlstxt_rect_centery[2])),
                                 self.controlstxt[3].get_rect(midright=(self.settingsstatinfo_xalignright, self.controlstxt_rect_centery[3])),
                                 self.controlstxt[4].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.controlstxt_rect_centery[4])),
                                 self.controlstxt[5].get_rect(midright=(self.settingsstatinfo_xalignright, self.controlstxt_rect_centery[5])),
                                 self.controlstxt[6].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.controlstxt_rect_centery[6])),
                                 self.controlstxt[7].get_rect(midright=(self.settingsstatinfo_xalignright, self.controlstxt_rect_centery[7])),
                                 self.controlstxt[8].get_rect(midright=(self.settingsstatinfo_xalignright, self.controlstxt_rect_centery[8])),
                                 self.controlstxt[9].get_rect(midright=(self.settingsstatinfo_xalignright, self.controlstxt_rect_centery[9]))
                                )

        self.yourfarmtxt = (self.font_body.render('Your Farm', True, self.c_black),
                            self.font_body2.render('Every day:', True, self.c_black),
                            self.font_body4.render('Minus farm\'s total', True, self.c_black),
                            self.font_body4.render('maintenance', True, self.c_black),
                            self.font_body2.render('Every 10th day:', True, self.c_black),
                            self.font_body4.render('Plus farm\'s total', True, self.c_black),
                            self.font_body4.render('earnings', True, self.c_black),
                            self.font_body4.render('Tiles in development', True, self.c_black),
                            self.font_body4.render('advance 1 stage', True, self.c_black)
                           )
        self.yourfarmtxt_rect = (self.yourfarmtxt[0].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.yourfarmtxt_rect_centery[0])),
                                 self.yourfarmtxt[1].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.yourfarmtxt_rect_centery[1])),
                                 self.yourfarmtxt[2].get_rect(midright=(self.settingsstatinfo_xalignright, self.yourfarmtxt_rect_centery[2])),
                                 self.yourfarmtxt[3].get_rect(midright=(self.settingsstatinfo_xalignright, self.yourfarmtxt_rect_centery[3])),
                                 self.yourfarmtxt[4].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.yourfarmtxt_rect_centery[4])),
                                 self.yourfarmtxt[5].get_rect(midright=(self.settingsstatinfo_xalignright, self.yourfarmtxt_rect_centery[5])),
                                 self.yourfarmtxt[6].get_rect(midright=(self.settingsstatinfo_xalignright, self.yourfarmtxt_rect_centery[6])),
                                 self.yourfarmtxt[7].get_rect(midright=(self.settingsstatinfo_xalignright, self.yourfarmtxt_rect_centery[7])),
                                 self.yourfarmtxt[8].get_rect(midright=(self.settingsstatinfo_xalignright, self.yourfarmtxt_rect_centery[8]))
                                )

    def startup(self, persistent):

        self.persist = persistent

        self.background_img = pg.image.load(os.path.join('resources/temp', 'background.png')).convert()

    def get_event(self, event):

        if event.type == QUIT:
            self.quit = True

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.next_state = 'Farm'
            self.done = True
            self.play_sfx(self.sfx_clicked)

        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.close_btn_farm(event)
            self.back_btn_farm(event)

    def draw(self, surface):

        #Draw background
        surface.blit(self.background_img, (0, 0))
        surface.blit(self.background_img_blackoverlay, (0, 0))

        #Draw containing box
        pg.draw.rect(surface, self.c_white, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h))
        pg.draw.rect(surface, self.c_black, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h), self.box_borderthick)

        #Draw text, close and back buttons
        surface.blit(self.title[0], self.title_rect[0])
        surface.blit(self.title[1], self.title_rect[1])
        surface.blit(self.close_btntxt, self.close_btntxt_rect)
        surface.blit(self.back_btntxt, self.back_btntxt_rect)
        surface.blit(self.controlstxt[0], self.controlstxt_rect[0])
        surface.blit(self.controlstxt[1], self.controlstxt_rect[1])
        surface.blit(self.controlstxt[2], self.controlstxt_rect[2])
        surface.blit(self.controlstxt[3], self.controlstxt_rect[3])
        surface.blit(self.controlstxt[4], self.controlstxt_rect[4])
        surface.blit(self.controlstxt[5], self.controlstxt_rect[5])
        surface.blit(self.controlstxt[6], self.controlstxt_rect[6])
        surface.blit(self.controlstxt[7], self.controlstxt_rect[7])
        surface.blit(self.controlstxt[8], self.controlstxt_rect[8])
        surface.blit(self.controlstxt[9], self.controlstxt_rect[9])
        surface.blit(self.yourfarmtxt[0], self.yourfarmtxt_rect[0])
        surface.blit(self.yourfarmtxt[1], self.yourfarmtxt_rect[1])
        surface.blit(self.yourfarmtxt[2], self.yourfarmtxt_rect[2])
        surface.blit(self.yourfarmtxt[3], self.yourfarmtxt_rect[3])
        surface.blit(self.yourfarmtxt[4], self.yourfarmtxt_rect[4])
        surface.blit(self.yourfarmtxt[5], self.yourfarmtxt_rect[5])
        surface.blit(self.yourfarmtxt[6], self.yourfarmtxt_rect[6])
        surface.blit(self.yourfarmtxt[7], self.yourfarmtxt_rect[7])
        surface.blit(self.yourfarmtxt[8], self.yourfarmtxt_rect[8])
