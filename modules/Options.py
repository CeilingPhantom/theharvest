'''
Manages the Options screen
'''

#Import needed modules
import os
import pygame as pg
from pygame.locals import *
from modules.Gamestate import Gamestate

class Options(Gamestate):
    def __init__(self):

        super(Options, self).__init__()

        self.resumetxt_rect_centery = self.title_rect_centery + self.btn_ydist
        self.savetxt_rect_centery = self.resumetxt_rect_centery + self.btn_ydist
        self.settingstxt_rect_centery = self.savetxt_rect_centery + self.btn_ydist
        self.statstxt_rect_centery = self.settingstxt_rect_centery + self.btn_ydist
        self.gameinfotxt_rect_centery = self.statstxt_rect_centery + self.btn_ydist
        self.exittxt_rect_centery = self.gameinfotxt_rect_centery + self.btn_ydist

        self.msgbox_bordershift = 40

        self.saved_msgtxt = self.font_body.render('Sucessfully Saved', True, self.c_lightgray)
        self.saved_msgtxt_rect = self.saved_msgtxt.get_rect(center=(self.screen_centerx, self.msgbox_2line_ya))
        self.saved_msgtxt_ok = self.font_body2.render('Click to Return', True, self.c_lightgray)
        self.saved_msgtxt_ok_rect = self.saved_msgtxt_ok.get_rect(center=(self.screen_centerx, self.msgbox_2line_yb))

        self.msgbox = pg.Surface((self.saved_msgtxt_rect.w+self.msgbox_bordershift, self.saved_msgtxt_rect.h+self.msgbox_bordershift))
        self.msgbox.fill(self.c_darkgray)

        self.exit_msgtxt_yes_x = self.screen_centerx-self.msgbox.get_width()/6
        self.exit_msgtxt_no_x = self.screen_centerx+self.msgbox.get_width()/6
        self.exit_msgtxt_yesno_y = self.screen_centery+3*self.msgbox_bordershift/4

        self.exit_msgtxt = self.font_body.render('Are You Sure?', True, self.c_lightgray)
        self.exit_msgtxt_rect = self.exit_msgtxt.get_rect(center=(self.screen_centerx, self.screen_centery))
        self.exit_msgtxt_yes = self.font_body2.render('Yes', True, self.c_lightgray)
        self.exit_msgtxt_yes_rect = self.exit_msgtxt_yes.get_rect(center=(self.exit_msgtxt_yes_x, self.exit_msgtxt_yesno_y))
        self.exit_msgtxt_no = self.font_body2.render('No', True, self.c_lightgray)
        self.exit_msgtxt_no_rect = self.exit_msgtxt_no.get_rect(center=(self.exit_msgtxt_no_x, self.exit_msgtxt_yesno_y))

        #Options title
        self.title = self.font_title.render('Options', True, self.c_black)
        self.title_rect = self.title.get_rect(center=(self.screen_centerx, self.title_rect_centery))

        #Resume Game text and button
        self.resumetxt = self.font_body.render('Resume Game', True, self.c_black)
        self.resumetxt_rect = self.resumetxt.get_rect(center=(self.screen_centerx, self.resumetxt_rect_centery))

        #Save Game text and button
        self.savetxt = self.font_body.render('Save Game', True, self.c_black)
        self.savetxt_rect = self.savetxt.get_rect(center=(self.screen_centerx, self.savetxt_rect_centery))

        #Settings text and button
        self.settingstxt = self.font_body.render('Settings', True, self.c_black)
        self.settingstxt_rect = self.settingstxt.get_rect(center=(self.screen_centerx, self.settingstxt_rect_centery))

        #Stats text and button
        self.statstxt = self.font_body.render('Stats', True, self.c_black)
        self.statstxt_rect = self.statstxt.get_rect(center=(self.screen_centerx, self.statstxt_rect_centery))

        #Game Info text and button
        self.gameinfotxt = self.font_body.render('Info', True, self.c_black)
        self.gameinfotxt_rect = self.gameinfotxt.get_rect(center=(self.screen_centerx, self.gameinfotxt_rect_centery))

        #Exit Game text and button
        self.exittxt = self.font_body.render('Exit Game', True, self.c_black)
        self.exittxt_rect = self.exittxt.get_rect(center=(self.screen_centerx, self.exittxt_rect_centery))

    def startup(self, persistent):

        self.persist = persistent

        self.background_img = pg.image.load(os.path.join('resources/temp', 'background.png')).convert()

        self.saved_msg = False
        self.exit_msg = False

    def get_event(self, event):

        if event.type == QUIT:
            self.quit = True

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            if self.saved_msg or self.exit_msg:
                self.saved_msg = False
                self.exit_msg = False
                self.play_sfx(self.sfx_clicked)
            else:
                self.next_state = 'Farm'
                self.done = True
                self.play_sfx(self.sfx_clicked)

        elif event.type == MOUSEBUTTONDOWN and event.button == 1:

            if self.saved_msg or self.exit_msg:

                #Return to Options screen after saving
                if self.screen_centerx-self.msgbox.get_width()/2 < event.pos[0] < self.screen_centerx+self.msgbox.get_width()/2 and self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2 < event.pos[1] < self.screen_centery+self.msgbox.get_height()/2+self.msgbox_bordershift/2 and self.saved_msg:
                    self.saved_msg = False
                    self.play_sfx(self.sfx_clicked)

                #Confirmation for whether or not the player wants to exit
                elif self.exit_msgtxt_yesno_y-self.exit_msgtxt_yes.get_height()/2 < event.pos[1] < self.exit_msgtxt_yesno_y+self.exit_msgtxt_yes.get_height()/2 and self.exit_msg:
                    #Press Yes
                    if self.exit_msgtxt_yes_x-self.exit_msgtxt_yes.get_width()/2-self.btn_borderthick < event.pos[0] < self.exit_msgtxt_yes_x+self.exit_msgtxt_yes.get_width()/2+self.btn_borderthick:
                        self.quit = True
                        self.play_sfx(self.sfx_clicked)
                    #Press No
                    elif self.exit_msgtxt_no_x-self.exit_msgtxt_yes.get_width()/2-self.btn_borderthick < event.pos[0] < self.exit_msgtxt_no_x+self.exit_msgtxt_yes.get_width()/2+self.btn_borderthick:
                        self.exit_msg = False
                        self.play_sfx(self.sfx_clicked)

            else:
                self.close_btn_farm(event)
                self.back_btn_farm(event)

                #Functionality for buttons to Resume Game, Save Game, Settings, Stats, Info, Exit Game, respectively
                if self.screen_centerx-self.btn_w/2 < event.pos[0] < self.screen_centerx+self.btn_w/2:
                    #Resume Game
                    if self.resumetxt_rect_centery-self.btn_h/2 < event.pos[1] < self.resumetxt_rect_centery+self.btn_h/2:
                        self.next_state = 'Farm'
                        self.done = True
                        self.play_sfx(self.sfx_clicked)
                    #Save Game
                    elif self.savetxt_rect_centery-self.btn_h/2 < event.pos[1] < self.savetxt_rect_centery+self.btn_h/2:
                        self.save(self.persist['grid'],
                                  self.persist['grid_tilecycle'],
                                  self.persist['money'],
                                  self.persist['timer'],
                                  self.persist['days_total'],
                                  self.persist['days_seasonyear'],
                                  self.persist['year'],
                                  self.persist['plowingtiles_dict'],
                                  self.persist['sfxvol'],
                                  self.persist['musicvol'],
                                  self.persist['total_money_earned'],
                                  self.persist['total_money_spent'],
                                  self.persist['total_money_highest'],
                                  self.persist['total_money_lowest']
                                 )
                        self.saved_msg = True
                        self.persist['saved'] = True
                        self.play_sfx(self.sfx_clicked)
                    #Settings
                    elif self.settingstxt_rect_centery-self.btn_h/2 < event.pos[1] < self.settingstxt_rect_centery+self.btn_h/2:
                        self.next_state = 'Settings'
                        self.done = True
                        self.play_sfx(self.sfx_clicked)
                    #Stats
                    elif self.statstxt_rect_centery-self.btn_h/2 < event.pos[1] < self.statstxt_rect_centery+self.btn_h/2:
                        self.next_state = 'Stats'
                        self.done = True
                        self.play_sfx(self.sfx_clicked)
                    #Game Info
                    elif self.gameinfotxt_rect_centery-self.btn_h/2 < event.pos[1] < self.gameinfotxt_rect_centery+self.btn_h/2:
                        self.next_state = 'Info'
                        self.done = True
                        self.play_sfx(self.sfx_clicked)
                    #Exit Game
                    elif self.exittxt_rect_centery-self.btn_h/2 < event.pos[1] < self.exittxt_rect_centery+self.btn_h/2:
                        self.exit_msg = True
                        self.play_sfx(self.sfx_clicked)

        elif event.type == USEREVENT+2:
            self.play_next_music()

    def draw(self, surface):

        #Draw background image of player's farm
        surface.blit(self.background_img, (0, 0))
        surface.blit(self.background_img_blackoverlay, (0, 0))

        #Draw containing box
        pg.draw.rect(surface, self.c_white, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h))
        pg.draw.rect(surface, self.c_black, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h), self.box_borderthick)

        #Draw button to Resume Game
        pg.draw.rect(surface, self.c_black, (self.btn_topleftx, self.resumetxt_rect_centery - self.btn_h/2, self.btn_w, self.btn_h), self.btn_borderthick)
        #Draw button to Save Game
        pg.draw.rect(surface, self.c_black, (self.btn_topleftx, self.savetxt_rect_centery - self.btn_h/2, self.btn_w, self.btn_h), self.btn_borderthick)
        #Draw button to Settings
        pg.draw.rect(surface, self.c_black, (self.btn_topleftx, self.settingstxt_rect_centery - self.btn_h/2, self.btn_w, self.btn_h), self.btn_borderthick)
        #Draw button to Stats
        pg.draw.rect(surface, self.c_black, (self.btn_topleftx, self.statstxt_rect_centery - self.btn_h/2, self.btn_w, self.btn_h), self.btn_borderthick)
        #Draw button to Game Info
        pg.draw.rect(surface, self.c_black, (self.btn_topleftx, self.gameinfotxt_rect_centery - self.btn_h/2, self.btn_w, self.btn_h), self.btn_borderthick)
        #Draw button to Exit Game
        pg.draw.rect(surface, self.c_black, (self.btn_topleftx, self.exittxt_rect_centery - self.btn_h/2, self.btn_w, self.btn_h), self.btn_borderthick)

        #Draw text, close and back buttons
        surface.blit(self.title, self.title_rect)
        surface.blit(self.close_btntxt, self.close_btntxt_rect)
        surface.blit(self.back_btntxt, self.back_btntxt_rect)
        surface.blit(self.resumetxt, self.resumetxt_rect)
        surface.blit(self.savetxt, self.savetxt_rect)
        surface.blit(self.statstxt, self.statstxt_rect)
        surface.blit(self.settingstxt, self.settingstxt_rect)
        surface.blit(self.gameinfotxt, self.gameinfotxt_rect)
        surface.blit(self.exittxt, self.exittxt_rect)

        #Draw popup for after game is saved
        if self.saved_msg:
            surface.blit(self.msgbox, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2))
            pg.draw.rect(surface, self.c_black, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2, self.msgbox.get_width(), self.msgbox.get_height()), self.box_borderthick)
            surface.blit(self.saved_msgtxt, self.saved_msgtxt_rect)
            surface.blit(self.saved_msgtxt_ok, self.saved_msgtxt_ok_rect)

        #Draw confirmation popup for exiting game
        if self.exit_msg:
            surface.blit(self.msgbox, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2))
            pg.draw.rect(surface, self.c_black, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2, self.msgbox.get_width(), self.msgbox.get_height()), self.box_borderthick)
            pg.draw.rect(surface, self.c_lightgray, (self.exit_msgtxt_yes_x-self.exit_msgtxt_yes.get_width()/2-self.btn_borderthick, self.exit_msgtxt_yesno_y-self.exit_msgtxt_yes.get_height()/2, self.exit_msgtxt_yes.get_width()+2*self.btn_borderthick, self.exit_msgtxt_yes.get_height()), self.btn_borderthick)
            pg.draw.rect(surface, self.c_lightgray, (self.exit_msgtxt_no_x-self.exit_msgtxt_yes.get_width()/2-self.btn_borderthick, self.exit_msgtxt_yesno_y-self.exit_msgtxt_yes.get_height()/2, self.exit_msgtxt_yes.get_width()+2*self.btn_borderthick, self.exit_msgtxt_yes.get_height()), self.btn_borderthick)
            surface.blit(self.exit_msgtxt, self.exit_msgtxt_rect)
            surface.blit(self.exit_msgtxt_yes, self.exit_msgtxt_yes_rect)
            surface.blit(self.exit_msgtxt_no, self.exit_msgtxt_no_rect)
