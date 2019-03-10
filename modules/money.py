'''
Manages the Money screen
'''

# show (avg and this turn's) total maintenance, total earnings and gross profit
# show total number of each crop, livestock, structure on farm

import os
import pygame as pg
from pygame.locals import *
from modules.gamestate import Gamestate

class Money(Gamestate):
    def __init__(self):

        super(Money, self).__init__()

        self.box_h = 340
        self.box_toplefty = (self.screen_height - self.box_h)/2
        self.thisdaytxt_rect_centery = self.box_toplefty + 2*self.box_borderdist

        #redefine because different box dimensions compared to other screens using the close and back buttons
        self.close_btntxt_rect = self.close_btntxt.get_rect(midright=(self.box_topleftx+self.box_w-self.box_borderdist/2, self.box_toplefty+3*self.box_borderdist/4))
        self.back_btntxt_rect = self.back_btntxt.get_rect(midleft=(self.box_topleftx+self.box_borderdist/2, self.box_toplefty+3*self.box_borderdist/4))

        self.thisdaytxt_rect_centery = (self.thisdaytxt_rect_centery,
                                        self.thisdaytxt_rect_centery+self.statinfo_ydist,
                                        self.thisdaytxt_rect_centery+2*self.statinfo_ydist,
                                        self.thisdaytxt_rect_centery+3*self.statinfo_ydist
                                        )

        self.avgtxt_rect_centery = (self.thisdaytxt_rect_centery[2]+2*self.statinfo_ydist+self.statinfo_ydist/3,
                                        self.thisdaytxt_rect_centery[2]+3*self.statinfo_ydist+self.statinfo_ydist/3,
                                        self.thisdaytxt_rect_centery[2]+4*self.statinfo_ydist+self.statinfo_ydist/3,
                                        self.thisdaytxt_rect_centery[2]+5*self.statinfo_ydist+self.statinfo_ydist/3,
                                        self.thisdaytxt_rect_centery[2]+6*self.statinfo_ydist+self.statinfo_ydist/3
                                       )

        self.profit = 0
        self.profit_sign = ' $'
        self.profittxt_color = self.c_black

    def startup(self, persistent):

        self.persist = persistent

        self.grid = self.persist['grid']

        self.thisday_earnings = self.persist['thisday_earnings']
        self.thisday_maintenance = self.persist['thisday_maintenance']
        print str(self.thisday_earnings)
        print str(self.thisday_maintenance)

        self.set_display_profit(self.thisday_earnings, self.thisday_maintenance)

        self.thisdaytxt = (self.font_body.render('This Day', True, self.c_black),
                           self.font_body2.render('Earnings: $'+str(int(self.thisday_earnings)), True, self.c_black),
                           self.font_body2.render('Maint.:  -$'+str(int(self.thisday_maintenance)), True, self.c_black),
                           self.font_body2.render('Profit:  '+self.profit_sign+str(int(self.profit)), True, self.profittxt_color)
                           )

        self.thisdaytxt_rect = (self.thisdaytxt[0].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.thisdaytxt_rect_centery[0])),
                                self.thisdaytxt[1].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.thisdaytxt_rect_centery[1])),
                                self.thisdaytxt[2].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.thisdaytxt_rect_centery[2])),
                                self.thisdaytxt[3].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.thisdaytxt_rect_centery[3]))
                               )

        avg_earnings_maintenance = self.calc_avg_earnings_maintenance()
        self.set_display_profit(avg_earnings_maintenance[0], avg_earnings_maintenance[1])

        self.avgtxt = (self.font_body.render('Avg per Day', True, self.c_black),
                           self.font_body.render('(All Tiles)', True, self.c_black),
                           self.font_body2.render('Earnings: $'+str(avg_earnings_maintenance[0]), True, self.c_black),
                           self.font_body2.render('Maint.:  -$'+str(avg_earnings_maintenance[1]), True, self.c_black),
                           self.font_body2.render('Profit:  '+self.profit_sign+str(self.profit), True, self.profittxt_color)
                          )

        self.avgtxt_rect = (self.avgtxt[0].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.avgtxt_rect_centery[0])),
                                self.avgtxt[1].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.avgtxt_rect_centery[1])),
                                self.avgtxt[2].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.avgtxt_rect_centery[2])),
                                self.avgtxt[3].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.avgtxt_rect_centery[3])),
                                self.avgtxt[4].get_rect(midleft=(self.settingsstatinfo_xalignleft, self.avgtxt_rect_centery[4]))
                               )

        self.background_img = pg.image.load(os.path.join('resources/temp', 'background.png')).convert()

    def set_display_profit(self, earnings, maintenance):
        self.profit = earnings-maintenance
        if self.profit < 0:
            self.profit_sign = '-$'
            self.profit = abs(self.profit)
            self.profittxt_color = self.c_red
        else:
            self.profit_sign = ' $'
            self.profittxt_color = self.c_black

    def calc_avg_earnings_maintenance(self):
        avg_earnings = 0
        avg_maintenance = 0
        for row in range(self.grid_h):
            for col in range(self.grid_w):
                avg_earnings += self.tiles[self.grid[row][col]].earnings
                avg_maintenance += self.tiles[self.grid[row][col]].maintenance
        return (avg_earnings, avg_maintenance)

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
        surface.blit(self.thisdaytxt[0], self.thisdaytxt_rect[0])
        surface.blit(self.thisdaytxt[1], self.thisdaytxt_rect[1])
        surface.blit(self.thisdaytxt[2], self.thisdaytxt_rect[2])
        surface.blit(self.thisdaytxt[3], self.thisdaytxt_rect[3])
        surface.blit(self.avgtxt[0], self.avgtxt_rect[0])
        surface.blit(self.avgtxt[1], self.avgtxt_rect[1])
        surface.blit(self.avgtxt[2], self.avgtxt_rect[2])
        surface.blit(self.avgtxt[3], self.avgtxt_rect[3])
        surface.blit(self.avgtxt[4], self.avgtxt_rect[4])
