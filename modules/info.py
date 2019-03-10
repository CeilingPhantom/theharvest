'''
Manages the Info screen
'''

#Import needed modules
import os
import pygame as pg
from pygame.locals import *
from modules.gamestate import Gamestate

class Info(Gamestate):
    def __init__(self):

        super(Info, self).__init__()

        self.title = self.font_title.render('Info', True, self.c_black)
        self.title_rect = self.title.get_rect(center=(self.screen_centerx, self.title_rect_centery))

        self.gameinfo_versiontxt_rect_centery = self.title_rect_centery+4*self.statinfo_ydist
        self.gameinfo_developertxt_rect_centery = (self.gameinfo_versiontxt_rect_centery+2*self.statinfo_ydist,
                                                   self.gameinfo_versiontxt_rect_centery+3*self.statinfo_ydist-self.statinfo_ydist/4,
                                                   self.gameinfo_versiontxt_rect_centery+4*self.statinfo_ydist-self.statinfo_ydist/2
                                                   )
        self.gameinfo_licencetxt_rect_centery = (self.gameinfo_developertxt_rect_centery[2]+2*self.statinfo_ydist,
                                                 self.gameinfo_developertxt_rect_centery[2]+3*self.statinfo_ydist-self.statinfo_ydist/4,
                                                 self.gameinfo_developertxt_rect_centery[2]+4*self.statinfo_ydist-self.statinfo_ydist/2,
                                                 self.gameinfo_developertxt_rect_centery[2]+5*self.statinfo_ydist-3*self.statinfo_ydist/4
                                                 )
        self.gameinfo_enquirybugtxt_rect_centery = (self.gameinfo_licencetxt_rect_centery[2]+2*self.statinfo_ydist,
                                                    self.gameinfo_licencetxt_rect_centery[2]+3*self.statinfo_ydist-self.statinfo_ydist/4,
                                                    self.gameinfo_licencetxt_rect_centery[2]+4*self.statinfo_ydist-self.statinfo_ydist/2,
                                                    self.gameinfo_licencetxt_rect_centery[2]+5*self.statinfo_ydist-3*self.statinfo_ydist/4
                                                   )

        self.gameinfo_versiontxt = self.font_body2.render('The Harvest v.1.00', True, self.c_black)
        self.gameinfo_versiontxt_rect = self.gameinfo_versiontxt.get_rect(midleft=(self.settingsstatinfo_xalignleft, self.gameinfo_versiontxt_rect_centery))

        self.gameinfo_developertxt = (self.font_body2.render('The Harvest', True, self.c_black),
                                      self.font_body2.render('developed in 2017,', True, self.c_black),
                                      self.font_body2.render('by James Luo', True, self.c_black)
                                     )
        self.gameinfo_developertxt_rect = (self.gameinfo_developertxt[0].get_rect(midleft=(self.                                   settingsstatinfo_xalignleft, self.gameinfo_developertxt_rect_centery[0])                                   ),
                                           self.gameinfo_developertxt[1].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.gameinfo_developertxt_rect_centery[1])),
                                           self.gameinfo_developertxt[2].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.gameinfo_developertxt_rect_centery[2]))
                                          )

        self.gameinfo_licencetxt = (self.font_body2.render('The Harvest is', True, self.c_black),
                                    self.font_body2.render('provided under the', True, self.c_black),
                                    self.font_body2.render('\'The Harvest', True, self.c_black),
                                    self.font_body2.render('Licence Agreement\'', True, self.c_black)
                                   )
        self.gameinfo_licencetxt_rect = (self.gameinfo_licencetxt[0].get_rect(midleft=(self.settingsstatinfo_xalignleft                                 , self.gameinfo_licencetxt_rect_centery[0])),
                                         self.gameinfo_licencetxt[1].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.gameinfo_licencetxt_rect_centery[1])),
                                         self.gameinfo_licencetxt[2].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.gameinfo_licencetxt_rect_centery[2])),
                                         self.gameinfo_licencetxt[3].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.gameinfo_licencetxt_rect_centery[3]))
                                        )

        self.gameinfo_enquirybugtxt = (self.font_body2.render('To make an enquiry,', True, self.c_black),
                                       self.font_body2.render('or report a bug,', True, self.c_black),
                                       self.font_body2.render('contact James via', True, self.c_black),
                                       self.font_body2.render('jameshcluo@gmail.com', True, self.c_black)
                                      )
        self.gameinfo_enquirybugtxt_rect = (self.gameinfo_enquirybugtxt[0].get_rect(midleft=(self.                                    settingsstatinfo_xalignleft, self.gameinfo_enquirybugtxt_rect_centery[0                                    ])),
                                            self.gameinfo_enquirybugtxt[1].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.gameinfo_enquirybugtxt_rect_centery[1])),
                                            self.gameinfo_enquirybugtxt[2].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.gameinfo_enquirybugtxt_rect_centery[2])), self.gameinfo_enquirybugtxt[3].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.gameinfo_enquirybugtxt_rect_centery[3])))

    def startup(self, persistent):

        self.persist = persistent

        self.background_img = pg.image.load(os.path.join('resources/temp', 'background.png')).convert()

    def get_event(self, event):

        if event.type == QUIT:
            self.quit = True

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.next_state = 'Options'
            self.done = True
            self.play_sfx(self.sfx_clicked)

        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.close_btn_farm(event)
            self.back_btn_options(event)

        elif event.type == USEREVENT+2:
            self.play_next_music()

    def draw(self, surface):

        #Draw backgrounf
        surface.blit(self.background_img, (0, 0))
        surface.blit(self.background_img_blackoverlay, (0, 0))

        #Draw containing box
        pg.draw.rect(surface, self.c_white, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h))
        pg.draw.rect(surface, self.c_black, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h), self.box_borderthick)

        #Draw text, close and back buttons
        surface.blit(self.title, self.title_rect)
        surface.blit(self.close_btntxt, self.close_btntxt_rect)
        surface.blit(self.back_btntxt, self.back_btntxt_rect)
        surface.blit(self.gameinfo_versiontxt, self.gameinfo_versiontxt_rect)
        surface.blit(self.gameinfo_developertxt[0], self.gameinfo_developertxt_rect[0])
        surface.blit(self.gameinfo_developertxt[1], self.gameinfo_developertxt_rect[1])
        surface.blit(self.gameinfo_developertxt[2], self.gameinfo_developertxt_rect[2])
        surface.blit(self.gameinfo_licencetxt[0], self.gameinfo_licencetxt_rect[0])
        surface.blit(self.gameinfo_licencetxt[1], self.gameinfo_licencetxt_rect[1])
        surface.blit(self.gameinfo_licencetxt[2], self.gameinfo_licencetxt_rect[2])
        surface.blit(self.gameinfo_licencetxt[3], self.gameinfo_licencetxt_rect[3])
        surface.blit(self.gameinfo_enquirybugtxt[0], self.gameinfo_enquirybugtxt_rect[0])
        surface.blit(self.gameinfo_enquirybugtxt[1], self.gameinfo_enquirybugtxt_rect[1])
        surface.blit(self.gameinfo_enquirybugtxt[2], self.gameinfo_enquirybugtxt_rect[2])
        surface.blit(self.gameinfo_enquirybugtxt[3], self.gameinfo_enquirybugtxt_rect[3])
