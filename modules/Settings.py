'''
Manages the Settings screen
'''

#Import needed modules
import os
import pygame as pg
from pygame.locals import *
from modules.Gamestate import Gamestate

class Settings(Gamestate):
    def __init__(self):

        super(Settings, self).__init__()

        self.title = self.font_title2.render('Settings', True, self.c_black)
        self.title_rect = self.title.get_rect(center=(self.screen_centerx, self.title_rect_centery))

        self.sfxtxt_rect_centery = self.title_rect_centery+2*self.btn_ydist
        self.sfxvol_bar_rect_centery = self.title_rect_centery+5*self.btn_ydist/2
        self.musictxt_rect_centery = self.title_rect_centery+4*self.btn_ydist
        self.musicvol_bar_rect_centery = self.title_rect_centery+9*self.btn_ydist/2
        self.resetsavetxt_rect_centery = self.title_rect_centery+6*self.btn_ydist

        self.sfxtxt = self.font_body.render('SFX', True, self.c_black)
        self.sfxtxt_rect = self.sfxtxt.get_rect(midleft=(self.settingsstatinfo_xalignleft, self.sfxtxt_rect_centery))

        self.musictxt = self.font_body.render('Music', True, self.c_black)
        self.musictxt_rect = self.musictxt.get_rect(midleft=(self.settingsstatinfo_xalignleft, self.musictxt_rect_centery))

        self.resetsavetxt = self.font_body.render('Reset Save', True, self.c_black)
        self.resetsavetxt_rect = self.resetsavetxt.get_rect(center=(self.screen_centerx, self.resetsavetxt_rect_centery))

        self.sliderthick = 16

        self.musicvol_bar = self.sfxvol_bar = pg.Surface((self.box_w-2*self.box_borderdist, self.sliderthick))
        self.vol_bar_rightx = self.screen_centerx + self.box_w/2 - self.box_borderdist
        self.sfxvol_bar_rect = self.sfxvol_bar.get_rect(midright=(self.vol_bar_rightx, self.sfxvol_bar_rect_centery))
        self.sfxvol_bar.fill(self.c_black)

        self.musicvol_bar_rect = self.musicvol_bar.get_rect(midright=(self.vol_bar_rightx, self.musicvol_bar_rect_centery))
        self.musicvol_bar.fill(self.c_black)

        self.vol_bar_centerx = self.vol_bar_rightx - self.sfxvol_bar_rect.w/2

        self.sfxvol_slider = pg.Surface((self.sliderthick, self.sliderthick))
        self.musicvol_slider = pg.Surface((self.sliderthick, self.sliderthick))
        self.sfxvol_slider.fill(self.c_blue)
        self.musicvol_slider.fill(self.c_blue)

        self.sfxvol_slider_centerx = None
        self.sfxvol_slider_rect = None

        self.musicvol_slider_centerx = None
        self.musicvol_slider_rect = None

        self.msgbox_bordershift = 40

        self.reset_save_msgtxt = self.font_body.render('Are You Sure?', True, self.c_lightgray)
        self.reset_save_msgtxt_rect = self.reset_save_msgtxt.get_rect(center=(self.screen_centerx, self.screen_centery))

        self.msgbox = pg.Surface((self.reset_save_msgtxt_rect.w+self.msgbox_bordershift, self.reset_save_msgtxt_rect.h+self.msgbox_bordershift))
        self.msgbox.fill(self.c_darkgray)

        self.reset_save_msgtxt_yes_x = self.screen_centerx-self.msgbox.get_width()/6
        self.reset_save_msgtxt_no_x = self.screen_centerx+self.msgbox.get_width()/6
        self.reset_save_msgtxt_yesno_y = self.screen_centery+3*self.msgbox_bordershift/4

        self.reset_save_msgtxt_yes = self.font_body2.render('Yes', True, self.c_lightgray)
        self.reset_save_msgtxt_yes_rect = self.reset_save_msgtxt_yes.get_rect(center=(self.reset_save_msgtxt_yes_x, self.reset_save_msgtxt_yesno_y))
        self.reset_save_msgtxt_no = self.font_body2.render('No', True, self.c_lightgray)
        self.reset_save_msgtxt_no_rect = self.reset_save_msgtxt_no.get_rect(center=(self.reset_save_msgtxt_no_x, self.reset_save_msgtxt_yesno_y))

        self.success_reset_save_msgtxta = self.font_body.render('Save Reset', True, self.c_lightgray)
        self.success_reset_save_msgtxta_rect = self.success_reset_save_msgtxta.get_rect(center=(self.screen_centerx, self.msgbox_3line_ya))
        self.success_reset_save_msgtxtb = self.font_body2.render('Click to Return', True, self.c_lightgray)
        self.success_reset_save_msgtxtb_rect = self.success_reset_save_msgtxtb.get_rect(center=(self.screen_centerx, self.msgbox_3line_yb))
        self.success_reset_save_msgtxtc = self.font_body2.render('to Settings', True, self.c_lightgray)
        self.success_reset_save_msgtxtc_rect = self.success_reset_save_msgtxtc.get_rect(center=(self.screen_centerx, self.msgbox_3line_yc))

    def startup(self, persistent):

        self.persist = persistent
        self.sfxvol = self.persist['sfxvol']
        self.musicvol = self.persist['musicvol']

        self.background_img = pg.image.load(os.path.join('resources/temp', 'background.png')).convert()

        self.sfxvoltxt = self.font_body2.render(str(int(self.sfxvol*100.0))+'%', True, self.c_black)
        self.sfxvoltxt_rect = self.sfxvoltxt.get_rect(midright=(self.settingsstatinfo_xalignright, self.sfxtxt_rect_centery))

        self.musicvoltxt = self.font_body2.render(str(int(self.musicvol*100.0))+'%', True, self.c_black)
        self.musicvoltxt_rect = self.musicvoltxt.get_rect(midright=(self.settingsstatinfo_xalignright, self.musictxt_rect_centery))

        self.set_sfxvol_slider_position()
        self.set_musicvol_slider_position()

        self.reset_save_msg = False
        self.success_reset_save_msg = False

        self.sfxslider_holddown = False
        self.musicslider_holddown = False

    def reset_save(self):
        '''
        Resets the player's save
        '''
        self.persist['grid'] = []
        self.persist['grid_tilecycle'] = []
        for row in range(self.grid_h):
            self.persist['grid'].append([])
            self.persist['grid_tilecycle'].append([])
            for col in range(self.grid_w):
                self.persist['grid'][row].append('Grass0')
                self.persist['grid_tilecycle'][row].append(0)
        self.persist['money'] = self.start_money
        self.persist['timer'] = 0
        self.persist['days_total'] = 0
        self.persist['days_seasonyear'] = 0
        self.persist['year'] = 0
        self.persist['plowingtiles_dict'] = {}
        self.persist['total_money_earned'] = 0.0
        self.persist['total_money_spent'] = 0.0
        self.persist['total_money_highest'] = self.start_money
        self.persist['total_money_lowest'] = self.start_money

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

    def set_sfxvol_slider_position(self):
        '''
        Determines the position of the slider on the SFX volume bar
        '''
        self.sfxvol_slider_centerx = self.vol_bar_centerx-self.sfxvol_bar_rect.w/2+int(self.sfxvol*float(self.sfxvol_bar_rect.w-self.sliderthick))+self.sliderthick/2
        self.sfxvol_slider_rect = self.sfxvol_slider.get_rect(center=(self.sfxvol_slider_centerx, self.sfxvol_bar_rect_centery))

    def set_musicvol_slider_position(self):
        '''
        Determines the position of the slider on the music volume bar
        '''
        self.musicvol_slider_centerx = self.vol_bar_centerx-self.musicvol_bar_rect.w/2+int(self.musicvol*float(self.musicvol_bar_rect.w-self.sliderthick))+self.sliderthick/2
        self.musicvol_slider_rect = self.musicvol_slider.get_rect(center=(self.musicvol_slider_centerx, self.musicvol_bar_rect_centery))

    def get_event(self, event):

        self.set_musicvol()

        if event.type == QUIT:
            self.quit = True

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            if self.reset_save_msg or self.success_reset_save_msg:
                self.reset_save_msg = False
                self.success_reset_save_msg = False
                self.play_sfx(self.sfx_clicked)
            else:
                self.next_state = 'Options'
                self.done = True
                self.play_sfx(self.sfx_clicked)

        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.success_reset_save_msg:
                if self.screen_centerx-self.msgbox.get_width()/2 < event.pos[0] < self.screen_centerx+self.msgbox.get_width()/2 and self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2 < event.pos[1] < self.screen_centery+self.msgbox.get_height()/2+self.msgbox_bordershift/2:
                    self.success_reset_save_msg = False
                    self.play_sfx(self.sfx_clicked)

            elif self.reset_save_msg:
                if self.reset_save_msgtxt_yesno_y-self.reset_save_msgtxt_yes.get_height()/2 < event.pos[1] < self.reset_save_msgtxt_yesno_y+self.reset_save_msgtxt_yes.get_height()/2:
                    #Press Yes
                    if self.reset_save_msgtxt_yes_x-self.reset_save_msgtxt_yes.get_width()/2-self.btn_borderthick < event.pos[0] < self.reset_save_msgtxt_yes_x+self.reset_save_msgtxt_yes.get_width()/2+self.btn_borderthick:
                        self.reset_save()
                        self.reset_save_msg = False
                        self.success_reset_save_msg = True
                        self.persist['saved'] = True
                        self.play_sfx(self.sfx_clicked)
                    #Press No
                    elif self.reset_save_msgtxt_no_x-self.reset_save_msgtxt_yes.get_width()/2-self.btn_borderthick < event.pos[0] < self.reset_save_msgtxt_no_x+self.reset_save_msgtxt_yes.get_width()/2+self.btn_borderthick:
                        self.reset_save_msg = False
                        self.play_sfx(self.sfx_clicked)

            else:
                self.close_btn_farm(event)
                self.back_btn_options(event)

                #Reset Save Confirmation Popup
                if self.screen_centerx-self.btn_w/2 < event.pos[0] < self.screen_centerx+self.btn_w/2 and self.resetsavetxt_rect_centery-self.btn_h/2 < event.pos[1] < self.resetsavetxt_rect_centery+self.btn_h/2:
                    self.reset_save_msg = True
                    self.play_sfx(self.sfx_clicked)

                #Press on SFX volume bar
                elif self.sfxvol_bar_rect_centery-self.sliderthick/2 < event.pos[1] < self.sfxvol_bar_rect_centery+self.sliderthick/2:
                    if self.vol_bar_rightx-self.sfxvol_bar_rect.w < event.pos[0] < self.vol_bar_rightx:
                        self.sfxvol = float((event.pos[0]-(self.vol_bar_rightx-self.sfxvol_bar_rect.w)))/float(self.sfxvol_bar_rect.w)
                        self.set_sfxvol_slider_position()
                        self.persist['sfxvol'] = self.sfxvol
                        self.sfxslider_holddown = True
                        self.play_sfx(self.sfx_clicked)

                #Press on SFX volume bar
                elif self.musicvol_bar_rect_centery-self.sliderthick/2 < event.pos[1] < self.musicvol_bar_rect_centery+self.sliderthick/2:
                    if self.vol_bar_rightx-self.musicvol_bar_rect.w < event.pos[0] < self.vol_bar_rightx:
                        self.musicvol = float((event.pos[0]-(self.vol_bar_rightx-self.musicvol_bar_rect.w)))/float(self.musicvol_bar_rect.w)
                        self.set_musicvol_slider_position()
                        self.persist['musicvol'] = self.musicvol
                        self.musicslider_holddown = True
                        self.play_sfx(self.sfx_clicked)

        #Let go on LMB after holding it down to slide along volume bar
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if self.sfxslider_holddown or self.musicslider_holddown:
                self.sfxslider_holddown = False
                self.musicslider_holddown = False

        elif event.type == MOUSEMOTION:
            if self.sfxslider_holddown:
                if self.vol_bar_rightx-self.sfxvol_bar_rect.w < event.pos[0] < self.vol_bar_rightx:
                    self.sfxvol = float((event.pos[0]-(self.vol_bar_rightx-self.sfxvol_bar_rect.w)))/float(self.sfxvol_bar_rect.w)
                    self.set_sfxvol_slider_position()
                    self.persist['sfxvol'] = self.sfxvol
                elif event.pos[0] < self.vol_bar_rightx-self.sfxvol_bar_rect.w:
                    self.sfxvol = 0.0
                    self.set_sfxvol_slider_position()
                    self.persist['sfxvol'] = self.sfxvol
                elif event.pos[0] > self.vol_bar_rightx:
                    self.sfxvol = 1.0
                    self.set_sfxvol_slider_position()
                    self.persist['sfxvol'] = self.sfxvol

            elif self.musicslider_holddown:
                if self.vol_bar_rightx-self.musicvol_bar_rect.w < event.pos[0] < self.vol_bar_rightx:
                    self.musicvol = float((event.pos[0]-(self.vol_bar_rightx-self.musicvol_bar_rect.w)))/float(self.musicvol_bar_rect.w)
                    self.set_musicvol_slider_position()
                    self.persist['musicvol'] = self.musicvol
                elif event.pos[0] < self.vol_bar_rightx-self.musicvol_bar_rect.w:
                    self.musicvol = 0.0
                    self.set_musicvol_slider_position()
                    self.persist['musicvol'] = self.musicvol
                elif event.pos[0] > self.vol_bar_rightx:
                    self.musicvol = 1.0
                    self.set_musicvol_slider_position()
                    self.persist['musicvol'] = self.musicvol

        elif event.type == USEREVENT+2:
            self.play_next_music()

    def update(self, dt):

        self.sfxvoltxt = self.font_body2.render(str(int(self.sfxvol*100.0))+'%', True, self.c_black)
        self.sfxvoltxt_rect = self.sfxvoltxt.get_rect(midright=(self.settingsstatinfo_xalignright, self.sfxtxt_rect_centery))

        self.musicvoltxt = self.font_body2.render(str(int(self.musicvol*100.0))+'%', True, self.c_black)
        self.musicvoltxt_rect = self.musicvoltxt.get_rect(midright=(self.settingsstatinfo_xalignright, self.musictxt_rect_centery))

    def draw(self, surface):

        #Draw background
        surface.blit(self.background_img, (0, 0))
        surface.blit(self.background_img_blackoverlay, (0, 0))

        #Draw containing box
        pg.draw.rect(surface, self.c_white, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h))
        pg.draw.rect(surface, self.c_black, (self.box_topleftx, self.box_toplefty, self.box_w, self.box_h), self.box_borderthick)

        #Draw button to Reset Save
        pg.draw.rect(surface, self.c_black, (self.btn_topleftx, self.resetsavetxt_rect_centery - self.btn_h/2, self.btn_w, self.btn_h), self.btn_borderthick)

        #Draw text, close and back buttons
        surface.blit(self.title, self.title_rect)
        surface.blit(self.close_btntxt, self.close_btntxt_rect)
        surface.blit(self.back_btntxt, self.back_btntxt_rect)
        surface.blit(self.sfxtxt, self.sfxtxt_rect)
        surface.blit(self.sfxvoltxt, self.sfxvoltxt_rect)
        surface.blit(self.musictxt, self.musictxt_rect)
        surface.blit(self.musicvoltxt, self.musicvoltxt_rect)
        surface.blit(self.resetsavetxt, self.resetsavetxt_rect)

        #Draw SFX and music volume bar
        surface.blit(self.sfxvol_bar, self.sfxvol_bar_rect)
        surface.blit(self.musicvol_bar, self.musicvol_bar_rect)

        #Draw SFX and music volume slider
        surface.blit(self.sfxvol_slider, self.sfxvol_slider_rect)
        surface.blit(self.musicvol_slider, self.musicvol_slider_rect)

        #Draw confirmation popup for resetting save
        if self.reset_save_msg:
            surface.blit(self.msgbox, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2))
            pg.draw.rect(surface, self.c_black, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2, self.msgbox.get_width(), self.msgbox.get_height()), self.box_borderthick)
            pg.draw.rect(surface, self.c_lightgray, (self.reset_save_msgtxt_yes_x-self.reset_save_msgtxt_yes.get_width()/2-self.btn_borderthick, self.reset_save_msgtxt_yesno_y-self.reset_save_msgtxt_yes.get_height()/2, self.reset_save_msgtxt_yes.get_width()+2*self.btn_borderthick, self.reset_save_msgtxt_yes.get_height()), self.btn_borderthick)
            pg.draw.rect(surface, self.c_lightgray, (self.reset_save_msgtxt_no_x-self.reset_save_msgtxt_yes.get_width()/2-self.btn_borderthick, self.screen_centery+3*self.msgbox_bordershift/4-self.reset_save_msgtxt_yes.get_height()/2, self.reset_save_msgtxt_yes.get_width()+2*self.btn_borderthick, self.reset_save_msgtxt_yes.get_height()), self.btn_borderthick)
            surface.blit(self.reset_save_msgtxt, self.reset_save_msgtxt_rect)
            surface.blit(self.reset_save_msgtxt_yes, self.reset_save_msgtxt_yes_rect)
            surface.blit(self.reset_save_msgtxt_no, self.reset_save_msgtxt_no_rect)

        #Draw popup for after save is reset
        if self.success_reset_save_msg:
            surface.blit(self.msgbox, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2))
            pg.draw.rect(surface, self.c_black, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2, self.msgbox.get_width(), self.msgbox.get_height()), self.box_borderthick)
            surface.blit(self.success_reset_save_msgtxta, self.success_reset_save_msgtxta_rect)
            surface.blit(self.success_reset_save_msgtxtb, self.success_reset_save_msgtxtb_rect)
            surface.blit(self.success_reset_save_msgtxtc, self.success_reset_save_msgtxtc_rect)
