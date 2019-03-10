'''
Manages the Stats screen
'''

#Import needed modules
import os
import pygame as pg
from pygame.locals import *
from modules.gamestate import Gamestate

class Stats(Gamestate):
    def __init__(self):

        super(Stats, self).__init__()

        self.title = self.font_title.render('Stats', True, self.c_black)
        self.title_rect = self.title.get_rect(center=(self.screen_centerx, self.title_rect_centery))

        self.ingametxt_rect_centery = self.title_rect_centery+2*self.statinfo_ydist
        self.ingame_totaltimetxt_rect_centery = (self.ingametxt_rect_centery+self.statinfo_ydist+self.statinfo_ydist/8,
                                                 self.ingametxt_rect_centery+2*self.statinfo_ydist-self.statinfo_ydist/8
                                                )
        self.ingame_totalmoneyearnedtxt_rect_centery = (self.ingame_totaltimetxt_rect_centery[1]+self.statinfo_ydist+                                                self.statinfo_ydist/8,
                                                        self.ingame_totaltimetxt_rect_centery[1]+2*self.statinfo_ydist-self.statinfo_ydist/8
                                                       )
        self.ingame_totalmoneyspenttxt_rect_centery = (self.ingame_totalmoneyearnedtxt_rect_centery[1]+self.                                               statinfo_ydist+self.statinfo_ydist/8,
                                                       self.ingame_totalmoneyearnedtxt_rect_centery[1]+2*self.statinfo_ydist-self.statinfo_ydist/8
                                                      )
        self.ingame_totalmoneyhighesttxt_rect_centery = (self.ingame_totalmoneyspenttxt_rect_centery[1]+self.                                                 statinfo_ydist+self.statinfo_ydist/8,
                                                         self.ingame_totalmoneyspenttxt_rect_centery[1]+2*self.statinfo_ydist-self.statinfo_ydist/8
                                                        )
        self.ingame_totalmoneylowesttxt_rect_centery = (self.ingame_totalmoneyhighesttxt_rect_centery[1]+self.                                                statinfo_ydist+self.statinfo_ydist/8,
                                                        self.ingame_totalmoneyhighesttxt_rect_centery[1]+2*self.statinfo_ydist-self.statinfo_ydist/8
                                                       )
        self.inreallifetxt_rect_centery = self.ingame_totalmoneylowesttxt_rect_centery[1]+2*self.statinfo_ydist
        self.inreallife_totaltimetxt_rect_centery = (self.inreallifetxt_rect_centery+self.statinfo_ydist+self.                                            statinfo_ydist/8,
                                                    self.inreallifetxt_rect_centery+2*self.statinfo_ydist-self.statinfo_ydist/8,
                                                    self.inreallifetxt_rect_centery+3*self.statinfo_ydist-3*self.statinfo_ydist/8,
                                                    self.inreallifetxt_rect_centery+4*self.statinfo_ydist-5*self.statinfo_ydist/8
                                                    )

    def startup(self, persistent):

        self.persist = persistent
        self.money = self.persist['money']
        self.timer = self.persist['timer']
        self.total_days = self.persist['days_total']
        self.total_money_earned = self.persist['total_money_earned']
        self.total_money_spent = self.persist['total_money_spent']
        self.total_money_highest = self.persist['total_money_highest']
        self.total_money_lowest = self.persist['total_money_lowest']

        if self.total_money_lowest < 0:
            total_money_lowest = abs(self.total_money_lowest)
            total_money_lowesttxt = 'Highest Debt:'
        else:
            total_money_lowest = self.total_money_lowest
            total_money_lowesttxt = 'Lowest Total Money:'

        self.background_img = pg.image.load(os.path.join('resources/temp', 'background.png')).convert()

        (self.total_years,
         self.current_year_total_days
        ) = self.calc_total_time_spent_ingame()

        (self.inreallife_totaldays,
         self.inreallife_totalhours,
         self.inreallife_totalminutes,
         self.inreallife_totalseconds,
         self.inreallife_hours_mod_hoursinday,
         self.inreallife_minutes_mod_minutesinhour,
         self.inreallife_seconds_mod_secondsinminute
        ) = self.calc_total_time_spent_real()

        self.ingametxt = self.font_body.render('In-Game', True, self.c_black)
        self.ingametxt_rect = self.ingametxt.get_rect(center=(self.screen_centerx, self.ingametxt_rect_centery))

        if self.total_years == 1:
            ingame_yeartxt = ' Year, '
        else:
            ingame_yeartxt = ' Years, '
        if self.current_year_total_days == 1:
            ingame_daytxt = ' Day'
        else:
            ingame_daytxt = ' Days'
        self.ingame_totaltimetxt = (self.font_body2.render('Total Time On Farm:', True, self.c_black),
                                    self.font_body2.render(str(self.total_years)+ingame_yeartxt+str(self.current_year_total_days)+ingame_daytxt, True, self.c_black)
                                   )
        self.ingame_totaltimetxt_rect = (self.ingame_totaltimetxt[0].get_rect(midleft=(self.settingsstatinfo_xalignleft                                 , self.ingame_totaltimetxt_rect_centery[0])),
                                         self.ingame_totaltimetxt[1].get_rect(midright=(self.settingsstatinfo_xalignright, self.ingame_totaltimetxt_rect_centery[1]))
                                        )

        self.ingame_totalmoneyearnedtxt = (self.font_body2.render('Total Money Earned:', True, self.c_black),
                                           self.font_body2.render('$'+str(int(self.total_money_earned)), True, self.c_black)
                                          )
        self.ingame_totalmoneyearnedtxt_rect = (self.ingame_totalmoneyearnedtxt[0].get_rect(midleft=(self.                                        settingsstatinfo_xalignleft, self.                                        ingame_totalmoneyearnedtxt_rect_centery[0])),
                                                self.ingame_totalmoneyearnedtxt[1].get_rect(midright=(self.settingsstatinfo_xalignright, self.ingame_totalmoneyearnedtxt_rect_centery[1]))
                                               )

        self.ingame_totalmoneyspenttxt = (self.font_body2.render('Total Money Spent:', True, self.c_black),
                                          self.font_body2.render('$'+str(int(self.total_money_spent)), True, self.c_black)
                                         )
        self.ingame_totalmoneyspenttxt_rect = (self.ingame_totalmoneyspenttxt[0].get_rect(midleft=(self.                                       settingsstatinfo_xalignleft, self.                                       ingame_totalmoneyspenttxt_rect_centery[0])),
                                               self.ingame_totalmoneyspenttxt[1].get_rect(midright=(self.settingsstatinfo_xalignright, self.ingame_totalmoneyspenttxt_rect_centery[1]))
                                              )

        self.ingame_totalmoneyhighesttxt = (self.font_body2.render('Highest Total Money:', True, self.c_black),
                                            self.font_body2.render('$'+str(int(self.total_money_highest)), True, self.c_black)
                                           )
        self.ingame_totalmoneyhighesttxt_rect = (self.ingame_totalmoneyhighesttxt[0].get_rect(midleft=(self.                                         settingsstatinfo_xalignleft, self.                                         ingame_totalmoneyhighesttxt_rect_centery[0])),
                                                 self.ingame_totalmoneyhighesttxt[1].get_rect(midright=(self.settingsstatinfo_xalignright, self.ingame_totalmoneyhighesttxt_rect_centery[1]))
                                                )

        self.ingame_totalmoneylowesttxt = (self.font_body2.render(total_money_lowesttxt, True, self.c_black),
                                           self.font_body2.render('$'+str(int(total_money_lowest)), True, self.c_black)
                                          )
        self.ingame_totalmoneylowesttxt_rect = (self.ingame_totalmoneylowesttxt[0].get_rect(midleft=(self.                                        settingsstatinfo_xalignleft, self.                                        ingame_totalmoneylowesttxt_rect_centery[0])),
                                                self.ingame_totalmoneylowesttxt[1].get_rect(midright=(self.settingsstatinfo_xalignright, self.ingame_totalmoneylowesttxt_rect_centery[1]))
                                               )

        self.inreallifetxt = self.font_body.render('In Real Life', True, self.c_black)
        self.inreallifetxt_rect = self.inreallifetxt.get_rect(center=(self.screen_centerx, self.inreallifetxt_rect_centery))

        if self.inreallife_totaldays == 1:
            inreallife_daytxt = ' Day, '
        else:
            inreallife_daytxt = ' Days, '
        if self.inreallife_hours_mod_hoursinday == 1:
            inreallife_hourtxt = ' Hour,'
        else:
            inreallife_hourtxt = ' Hours,'
        if self.inreallife_minutes_mod_minutesinhour == 1:
            inreallife_minutetxt = ' Minute,'
        else:
            inreallife_minutetxt = ' Minutes,'
        if self.inreallife_seconds_mod_secondsinminute == 1:
            inreallife_secondtxt = ' Second'
        else:
            inreallife_secondtxt = ' Seconds'
        self.inreallife_totaltimetxt = (self.font_body2.render('Total Time On Farm:', True, self.c_black),
                                        self.font_body2.render(str(self.inreallife_totaldays)+inreallife_daytxt+str(self.inreallife_hours_mod_hoursinday)+inreallife_hourtxt, True, self.c_black),
                                        self.font_body2.render(str(self.inreallife_minutes_mod_minutesinhour)+inreallife_minutetxt, True, self.c_black),
                                        self.font_body2.render(str(self.inreallife_seconds_mod_secondsinminute)+inreallife_secondtxt, True, self.c_black)
                                       )
        self.inreallife_totaltimetxt_rect = (self.inreallife_totaltimetxt[0].get_rect(midleft=(self.                                     settingsstatinfo_xalignleft, self.inreallife_totaltimetxt_rect_centery                                     [0])),
                                             self.inreallife_totaltimetxt[1].get_rect(midright=(self.settingsstatinfo_xalignright, self.inreallife_totaltimetxt_rect_centery[1])),
                                             self.inreallife_totaltimetxt[2].get_rect(midright=(self.settingsstatinfo_xalignright, self.inreallife_totaltimetxt_rect_centery[2])),
                                             self.inreallife_totaltimetxt[3].get_rect(midright=(self.settingsstatinfo_xalignright, self.inreallife_totaltimetxt_rect_centery[3]))
                                            )

    def calc_total_time_spent_ingame(self):
        '''
        Calculates how much ingame time the player has spent on their farm
        '''
        total_years = 0
        days = 0
        current_year_total_days = self.total_days
        while days <= current_year_total_days:
            if days == 0 and current_year_total_days == 0:
                break
            elif days == 365 and (total_years+1)%4 != 0:
                total_years += 1
                current_year_total_days -= 365
                days = 0
            elif days == 366 and (total_years+1)%4 == 0:
                total_years += 1
                current_year_total_days -= 366
                days = 0
            days += 1
        return (total_years, current_year_total_days)

    def calc_total_time_spent_real(self):
        '''
        Calculates how much time in real life the player has spent on their farm
        '''
        inreallife_totalseconds = self.total_days*3 + self.timer%3
        inreallife_totalminutes = inreallife_totalseconds/60
        inreallife_totalhours = inreallife_totalminutes/60
        inreallife_totaldays = inreallife_totalhours/24
        inreallife_hours_mod_hoursinday = inreallife_totalhours%24
        inreallife_minutes_mod_minutesinhour = inreallife_totalminutes%60
        inreallife_seconds_mod_secondsinminute = inreallife_totalseconds%60
        return (inreallife_totaldays,
                inreallife_totalhours,
                inreallife_totalminutes,
                inreallife_totalseconds,
                inreallife_hours_mod_hoursinday,
                inreallife_minutes_mod_minutesinhour,
                inreallife_seconds_mod_secondsinminute
               )

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

        #Draw background
        surface.blit(self.background_img, (0, 0))
        surface.blit(self.background_img_blackoverlay, (0, 0))

        #Draw containing box
        pg.draw.rect(surface, self.c_white, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h))
        pg.draw.rect(surface, self.c_black, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h), self.box_borderthick)

        #Draw text, close and back buttons
        surface.blit(self.title, self.title_rect)
        surface.blit(self.close_btntxt, self.close_btntxt_rect)
        surface.blit(self.back_btntxt, self.back_btntxt_rect)
        surface.blit(self.ingametxt, self.ingametxt_rect)
        surface.blit(self.ingame_totaltimetxt[0], self.ingame_totaltimetxt_rect[0])
        surface.blit(self.ingame_totaltimetxt[1], self.ingame_totaltimetxt_rect[1])
        surface.blit(self.ingame_totalmoneyearnedtxt[0], self.ingame_totalmoneyearnedtxt_rect[0])
        surface.blit(self.ingame_totalmoneyearnedtxt[1], self.ingame_totalmoneyearnedtxt_rect[1])
        surface.blit(self.ingame_totalmoneyspenttxt[0], self.ingame_totalmoneyspenttxt_rect[0])
        surface.blit(self.ingame_totalmoneyspenttxt[1], self.ingame_totalmoneyspenttxt_rect[1])
        surface.blit(self.ingame_totalmoneyhighesttxt[0], self.ingame_totalmoneyhighesttxt_rect[0])
        surface.blit(self.ingame_totalmoneyhighesttxt[1], self.ingame_totalmoneyhighesttxt_rect[1])
        surface.blit(self.ingame_totalmoneylowesttxt[0], self.ingame_totalmoneylowesttxt_rect[0])
        surface.blit(self.ingame_totalmoneylowesttxt[1], self.ingame_totalmoneylowesttxt_rect[1])
        surface.blit(self.inreallifetxt, self.inreallifetxt_rect)
        surface.blit(self.inreallife_totaltimetxt[0], self.inreallife_totaltimetxt_rect[0])
        surface.blit(self.inreallife_totaltimetxt[1], self.inreallife_totaltimetxt_rect[1])
        surface.blit(self.inreallife_totaltimetxt[2], self.inreallife_totaltimetxt_rect[2])
        surface.blit(self.inreallife_totaltimetxt[3], self.inreallife_totaltimetxt_rect[3])
