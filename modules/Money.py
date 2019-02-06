'''
Manages the Money screen
'''

# show (general and this turn's) total maintenance, total earnings and gross profit
# show total number of each crop, livestock, structure on farm

import os
import pygame as pg
from pygame.locals import *
from modules.Gamestate import Gamestate

class Money(Gamestate):
    def __init__(self):

        super(Money, self).__init__()

        self.box_h = self.box_w
        self.box_toplefty = (self.screen_height - self.box_h)/2

        #redefine because different box dimensions compared to other screens using the close and back buttons
        self.close_btntxt_rect = self.close_btntxt.get_rect(midright=(self.box_topleftx+self.box_w-self.box_borderdist/2, self.box_toplefty+3*self.box_borderdist/4))
        self.back_btntxt_rect = self.back_btntxt.get_rect(midleft=(self.box_topleftx+self.box_borderdist/2, self.box_toplefty+3*self.box_borderdist/4))
        

    def startup(self, persistent):

        self.persist = persistent

        #self.earnings = self.persist['']
        #self.earningstxt = self.font_body2.render('Earnings: '+str(self.))

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
        #Draw background image of player's farm
        surface.blit(self.background_img, (0, 0))
        surface.blit(self.background_img_blackoverlay, (0, 0))

        #Draw containing box
        pg.draw.rect(surface, self.c_white, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h))
        pg.draw.rect(surface, self.c_black, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h), self.box_borderthick)

        #Draw text, close and back buttons
        surface.blit(self.close_btntxt, self.close_btntxt_rect)
        surface.blit(self.back_btntxt, self.back_btntxt_rect)