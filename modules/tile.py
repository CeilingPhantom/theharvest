'''
Manages the Tile screen
'''

#Import needed modules
import os
import pygame as pg
from pygame.locals import *
from modules.gamestate import Gamestate

class Tile(Gamestate):
    def __init__(self):

        super(Tile, self).__init__()

        self.box_w = 600
        self.box_topleftx = self.screen_centerx - self.box_w/2
        self.btn_w = 120

        #redefine because different box dimensions compared to other screens using the close and back buttons
        self.close_btntxt_rect = self.close_btntxt.get_rect(midright=(self.box_topleftx+self.box_w-self.box_borderdist/2, self.box_toplefty+3*self.box_borderdist/4))
        self.back_btntxt_rect = self.back_btntxt.get_rect(midleft=(self.box_topleftx+self.box_borderdist/2, self.box_toplefty+3*self.box_borderdist/4))

        self.xaligndist = 30
        self.xadjust = 20
        self.ydist = 80
        self.yadjust = 10
        self.xalign1 = self.box_topleftx + self.xaligndist + self.xadjust
        self.xalign2 = self.screen_centerx - self.xadjust
        self.xalign3 = self.xalign1 + self.box_w/2 - self.xadjust #670
        self.xalign4 = self.xalign2 + self.box_w/2 - self.xadjust

        self.tc_mdtopx = self.screen_centerx - self.box_w/4 + self.xadjust # tc = tier current
        self.tier_mdtopy = self.screen_centery + 3*self.yadjust
        self.earntxt_y = self.tier_mdtopy + self.ydist - self.yadjust
        self.maintxt_y = self.earntxt_y + self.ydist - 2*self.yadjust
        self.sellremovebuy_centerx = (self.xalign1 + self.tc_mdtopx)/2
        self.sellremoveupgbuy_centery = self.box_toplefty + self.box_h - self.btn_h
        self.sellbuybtn_topleftx = self.sellremovebuy_centerx - self.btn_w/2
        self.btn_topy = self.sellremoveupgbuy_centery - self.btn_h/2

        self.img_s = 285
        self.img_x = self.box_topleftx + 2*self.xadjust #340 + 30 + 270 = 640
        self.img_y = self.box_toplefty + 2*self.xadjust #60 + 280

        self.titleflavor_x = self.xalign3 + self.xadjust
        self.flavor_y = self.title_rect_centery + self.ydist/3

        self.buyupg_msgtxta = self.font_body.render('Insufficient Money', True, self.c_lightgray)
        self.buyupg_msgtxta_rect = self.buyupg_msgtxta.get_rect(center=(self.screen_centerx, self.msgbox_3line_ya))
        self.buyupg_msgtxtb = self.font_body2.render('At Least $1 Needed', True, self.c_lightgray)
        self.buyupg_msgtxtb_rect = self.buyupg_msgtxtb.get_rect(center=(self.screen_centerx, self.msgbox_3line_yb))
        self.buyupg_msgtxtc = self.font_body2.render('Click to Return', True, self.c_lightgray)
        self.buyupg_msgtxtc_rect = self.buyupg_msgtxtc.get_rect(center=(self.screen_centerx, self.msgbox_3line_yc))

        self.msgbox = pg.Surface((self.buyupg_msgtxta_rect.w+self.msgbox_bordershift, self.buyupg_msgtxta_rect.h+self.msgbox_bordershift))
        self.msgbox.fill(self.c_darkgray)

        self.greenhouse_required_msgtxta = self.font_body.render('Greenhouse Required', True, self.c_lightgray)
        self.greenhouse_required_msgtxta_rect = self.greenhouse_required_msgtxta.get_rect(center=(self.screen_centerx, self.msgbox_3line_ya))
        self.greenhouse_required_msgtxtb = self.font_body2.render('Crop Not in Season', True, self.c_lightgray)
        self.greenhouse_required_msgtxtb_rect = self.greenhouse_required_msgtxtb.get_rect(center=(self.screen_centerx, self.msgbox_3line_yb))
        self.greenhouse_required_msgtxtc = self.font_body2.render('Click to Return', True, self.c_lightgray)
        self.greenhouse_required_msgtxtc_rect = self.greenhouse_required_msgtxtc.get_rect(center=(self.screen_centerx, self.msgbox_3line_yc))

        self.silo_required_msgtxta = self.font_body.render('Silo Required', True, self.c_lightgray)
        self.silo_required_msgtxta_rect = self.silo_required_msgtxta.get_rect(center=(self.screen_centerx, self.msgbox_3line_ya))
        self.silo_required_msgtxtb = self.font_body2.render('Livestock Need Silo for Food', True, self.c_lightgray)
        self.silo_required_msgtxtb_rect = self.silo_required_msgtxtb.get_rect(center=(self.screen_centerx, self.msgbox_3line_yb))
        self.silo_required_msgtxtc = self.font_body2.render('Click to Return', True, self.c_lightgray)
        self.silo_required_msgtxtc_rect = self.silo_required_msgtxtc.get_rect(center=(self.screen_centerx, self.msgbox_3line_yc))

        self.sellremoveupg_msgtxt_yes_x = self.screen_centerx-self.msgbox.get_width()/6
        self.sellremoveupg_msgtxt_no_x = self.screen_centerx+self.msgbox.get_width()/6
        self.sellremoveupg_msg_yesno_y = self.screen_centery+3*self.msgbox_bordershift/4

        self.sellremoveupg_msgtxt = self.font_body.render('Are You Sure?', True, self.c_lightgray)
        self.sellremoveupg_msgtxt_rect = self.sellremoveupg_msgtxt.get_rect(center=(self.screen_centerx, self.screen_centery))
        self.sellremoveupg_msgtxt_yes = self.font_body2.render('Yes', True, self.c_lightgray)
        self.sellremoveupg_msgtxt_yes_rect = self.sellremoveupg_msgtxt_yes.get_rect(center=(self.sellremoveupg_msgtxt_yes_x, self.sellremoveupg_msg_yesno_y))
        self.sellremoveupg_msgtxt_no = self.font_body2.render('No', True, self.c_lightgray)
        self.sellremoveupg_msgtxt_no_rect = self.sellremoveupg_msgtxt_no.get_rect(center=(self.sellremoveupg_msgtxt_no_x, self.sellremoveupg_msg_yesno_y))

    def startup(self, persistent):

        self.persist = persistent
        self.grid = self.persist['grid']
        self.grid_tilecycle = self.persist['grid_tilecycle']
        self.money = self.persist['money']
        self.select_col = self.persist['select_col']
        self.select_row = self.persist['select_row']
        self.buytile = self.persist['buytile']
        self.plowingtiles_dict = self.persist['plowingtiles_dict']
        self.plowingtile_counter = self.persist['plowingtile_counter']
        self.plowingtimer = self.persist['plowingtimer']
        self.current_season = self.persist['current_season']
        self.sfxvol = self.persist['sfxvol']
        self.musicvol = self.persist['musicvol']

        self.background_img = pg.image.load(os.path.join('resources/temp', 'background.png')).convert()

        self.can_upgrade = False
        self.sellremoveupg_msg = False
        self.insufficent_money = False
        self.greenhouse_required = False
        self.silo_required = False

        self.subtitle = None
        self.subtitle_rect = None

        if self.buytile is None:
            if not(self.grid[self.select_row][self.select_col] == 'Dirt0' or self.grid[self.select_row][self.select_col] == 'Field0' or self.grid[self.select_row][self.select_col] == 'Construct0'):
                self.tile = self.grid[self.select_row][self.select_col]
                #Set title
                self.title = self.tiles[self.tile].displayname
                #Set img
                self.img = self.tiles[self.tile].img0.convert()
                #Set flavor text
                self.flavortxta = self.tiles[self.tile].flavora
                self.flavortxtb = self.tiles[self.tile].flavorb
                #Set season text
                self.seasontxt = self.tiles[self.tile].season
            else:
                for self.plowingtile in self.plowingtiles_dict.keys():
                    if self.plowingtiles_dict[self.plowingtile][1] == self.select_row and self.plowingtiles_dict[self.plowingtile][2] == self.select_col:
                        break
                self.tile = self.plowingtiles_dict[self.plowingtile][0]
                #Set title
                self.title = self.tiles[self.tile].displayname
                #Set subtitle
                if self.tiles[self.plowingtiles_dict[self.plowingtile][0]].tiletype == 'Crop' and self.grid[self.select_row][self.select_col] == 'Dirt0':
                    self.subtitle = self.tiles['Field0'].displayname
                elif (self.tiles[self.plowingtiles_dict[self.plowingtile][0]].tiletype == 'Livestock' or self.tiles[self.plowingtiles_dict[self.plowingtile][0]].tiletype == 'Structure') and self.grid[self.select_row][self.select_col] == 'Dirt0':
                    self.subtitle = self.tiles['Construct0'].displayname
                else:
                    self.subtitle = self.title
                if len(self.tiles[self.grid[self.select_row][self.select_col]].displayname+' --> '+self.subtitle) > 26:
                    self.subtitle = self.font_ibody3.render(self.tiles[self.grid[self.select_row][self.select_col]].displayname+' --> '+self.subtitle, True, self.c_black)
                else:
                    self.subtitle = self.font_ibody2.render(self.tiles[self.grid[self.select_row][self.select_col]].displayname+' --> '+self.subtitle, True, self.c_black)
                self.subtitle_rect = self.subtitle.get_rect(midleft=(self.titleflavor_x, self.title_rect_centery-2*self.ydist/5))
                #Set img
                self.img = self.tiles[self.grid[self.select_row][self.select_col]].img0.convert()
                #Set flavor text
                self.flavortxta = self.tiles[self.grid[self.select_row][self.select_col]].flavora
                self.flavortxtb = self.tiles[self.grid[self.select_row][self.select_col]].flavorb
                #Set season text
                self.seasontxt = self.tiles[self.tile].season
                #Set remove price
                self.removep = self.tiles[self.grid[self.select_row][self.select_col]].sellprice
        else:
            self.tile = self.buytile
            #Set title
            self.title = self.tiles[self.tile].displayname
            #Set img
            self.img = self.tiles[self.tile].img0.convert()
            #Set flavor text
            self.flavortxta = self.tiles[self.tile].flavora
            self.flavortxtb = self.tiles[self.tile].flavorb
            #Set season text
            self.seasontxt = self.tiles[self.tile].season

        #Set name to be used for determining the name of the tile 1 tier above
        self.name = self.tiles[self.tile].name[0:-1]
        #Set sell price
        self.sellp = self.tiles[self.tile].sellprice
        #Set upgrade price
        self.buyp = self.tiles[self.tile].buyupgprice
        #Set current tier earnings
        self.tc_earn = self.tiles[self.tile].earnings
        #Set current tier maintenance
        self.tc_main = self.tiles[self.tile].maintenance

        #Sets the structure area of effect info, if it is a structure
        self.upgtxt_list = []
        for structure in self.structures:
            if self.tile == structure:
                tiercrnt = int(self.tile[-1])
                lowest_tier = 1
                name = list(self.tile[0:-1])
                name.append(str(lowest_tier))
                tier_structure_name = ''.join(name)
                tier1 = []
                t1upgtxt_list = []
                t1upgtxt_rect_list = []

                t1upgtxt_list.append(self.font_body2.render('Tier 1: '+self.structure_tierupgtxt[tier_structure_name][0], True, self.c_black))
                t1upgtxt_list.append(self.font_body2.render(self.structure_tierupgtxt[tier_structure_name][1], True, self.c_black))
                t1upgtxt_list.append(self.font_body2.render(self.structure_tierupgtxt[tier_structure_name][2], True, self.c_black))

                t1upgtxt_rect_list.append(t1upgtxt_list[0].get_rect(topleft=(self.titleflavor_x, self.flavor_y+5*self.ydist/4)))
                t1upgtxt_rect_list.append(t1upgtxt_list[1].get_rect(topleft=(self.titleflavor_x, self.flavor_y+3*self.ydist/2)))
                t1upgtxt_rect_list.append(t1upgtxt_list[2].get_rect(topleft=(self.titleflavor_x, self.flavor_y+7*self.ydist/4)))

                tier1.append(t1upgtxt_list)
                tier1.append(t1upgtxt_rect_list)
                self.upgtxt_list.append(tier1)
                lowest_tier += 1

                if self.buytile is None and tiercrnt+1 >= lowest_tier:
                    name = list(self.tile[0:-1])
                    name.append(str(lowest_tier))
                    tier_structure_name = ''.join(name)

                    tier2 = []
                    t2upgtxt_list = []
                    t2upgtxt_rect_list = []

                    t2upgtxt_list.append(self.font_body2.render('Tier 2: '+self.structure_tierupgtxt[tier_structure_name], True, self.c_black))
                    t2upgtxt_rect_list.append(t2upgtxt_list[0].get_rect(topleft=(self.titleflavor_x, self.flavor_y+2*self.ydist)))

                    tier2.append(t2upgtxt_list)
                    tier2.append(t2upgtxt_rect_list)
                    self.upgtxt_list.append(tier2)
                    lowest_tier += 1

                    if lowest_tier <= tiercrnt+1 <= 3+1:
                        name = list(self.tile[0:-1])
                        name.append(str(lowest_tier))
                        tier_structure_name = ''.join(name)

                        tier3 = []
                        t3upgtxt_list = []
                        t3upgtxt_rect_list = []

                        t3upgtxt_list.append(self.font_body2.render('Tier 3: '+self.structure_tierupgtxt[tier_structure_name][0], True, self.c_black))
                        t3upgtxt_list.append(self.font_body2.render(self.structure_tierupgtxt[tier_structure_name][1], True, self.c_black))
                        t3upgtxt_list.append(self.font_body2.render(self.structure_tierupgtxt[tier_structure_name][2], True, self.c_black))

                        t3upgtxt_rect_list.append(t3upgtxt_list[0].get_rect(topleft=(self.titleflavor_x, self.flavor_y+9*self.ydist/4)))
                        t3upgtxt_rect_list.append(t3upgtxt_list[1].get_rect(topleft=(self.titleflavor_x, self.flavor_y+5*self.ydist/2)))
                        t3upgtxt_rect_list.append(t3upgtxt_list[2].get_rect(topleft=(self.titleflavor_x, self.flavor_y+11*self.ydist/4)))

                        tier3.append(t3upgtxt_list)
                        tier3.append(t3upgtxt_rect_list)
                        self.upgtxt_list.append(tier3)
                        break
                    else:
                        break
                else:
                    break

        self.tile = self.tiles[self.tile]

        #Tile Info and Upgrade title
        if len(self.title) > 9:
            self.title = self.font_title2.render(self.title, True, self.c_black)
        else:
            self.title = self.font_title.render(self.title, True, self.c_black)
        self.title_rect = self.title.get_rect(midleft=(self.titleflavor_x, self.title_rect_centery))

        #Img
        self.img = pg.transform.scale(self.img, (self.img_s, self.img_s))

        #Flavor Text
        self.flavortxta = self.font_ibody.render(self.flavortxta, True, self.c_black)
        self.flavortxtb = self.font_ibody.render(self.flavortxtb, True, self.c_black)
        self.flavortxta_rect = self.flavortxta.get_rect(topleft=(self.titleflavor_x, self.flavor_y))
        self.flavortxtb_rect = self.flavortxtb.get_rect(topleft=(self.titleflavor_x, self.flavor_y+self.ydist/4))

        #Season Text
        self.seasontxt = self.font_body.render('Season: '+self.seasontxt, True, self.c_black)
        self.seasontxt_rect = self.seasontxt.get_rect(topleft=(self.titleflavor_x, self.flavor_y+3*self.ydist/4))

        if self.tile != self.tiles['Grass0']:
            self.tiercrnt = int(self.tile.name[-1])

            #Tier Current Heading
            self.tctxt = self.font_header.render('Tier '+str(self.tiercrnt), True, self.c_black)
            self.tctxt_rect = self.tctxt.get_rect(midtop=(self.tc_mdtopx, self.tier_mdtopy))

            #TC Earnings
            self.earntxta = self.font_body.render('Earnings', True, self.c_black)
            self.tc_earntxta_rect = self.earntxta.get_rect(topleft=(self.xalign1, self.earntxt_y))

            self.tc_earntxtb = self.font_body2.render('+$'+str(self.tc_earn)+'/10 days', True, self.c_black)
            self.tc_earntxtb_rect = self.tc_earntxtb.get_rect(topright=(self.xalign2, self.earntxt_y))

            #TC Maintenance
            self.maintxta = self.font_body.render('Maintenance', True, self.c_black)
            self.tc_maintxta_rect = self.maintxta.get_rect(topleft=(self.xalign1, self.maintxt_y))

            self.tc_maintxtb = self.font_body2.render('-$'+str(self.tc_main)+'/day', True, self.c_black)
            self.tc_maintxtb_rect = self.tc_maintxtb.get_rect(topright=(self.xalign2, self.maintxt_y))

            #Sell
            if self.buytile is None:
                if not(self.grid[self.select_row][self.select_col] == 'Dirt0' or self.grid[self.select_row][self.select_col] == 'Field0' or self.grid[self.select_row][self.select_col] == 'Construct0'):
                    self.selltxt = self.font_body.render('Sell', True, self.c_black)
                    self.selltxt_rect = self.selltxt.get_rect(center=(self.sellremovebuy_centerx, self.sellremoveupgbuy_centery))

                    self.sellptxt = self.font_body2.render('+$'+str(self.sellp), True, self.c_black)
                    self.sellptxt_rect = self.sellptxt.get_rect(midright=(self.xalign2, self.sellremoveupgbuy_centery))

                #Remove
                else:
                    self.removetxt = self.font_body.render('Remove', True, self.c_black)
                    self.removetxt_rect = self.removetxt.get_rect(center=(self.sellremovebuy_centerx, self.sellremoveupgbuy_centery))

                    self.removeptxt = self.font_body2.render('-$'+str(self.removep), True, self.c_black)
                    self.removeptxt_rect = self.removeptxt.get_rect(midright=(self.xalign2, self.sellremoveupgbuy_centery))

            #Buy
            else:
                self.buytxt = self.font_body.render('Buy', True, self.c_black)
                self.buytxt_rect = self.buytxt.get_rect(center=(self.sellremovebuy_centerx, self.sellremoveupgbuy_centery))

                self.buyptxt = self.font_body2.render('-$'+str(self.buyp), True, self.c_black)
                self.buyptxt_rect = self.buyptxt.get_rect(midright=(self.xalign2, self.sellremoveupgbuy_centery))

            if self.tiercrnt < 3:
                self.tiernxt = str(self.tiercrnt + 1)
                upg_tile_name = list(self.name)
                upg_tile_name.append(self.tiernxt)
                self.upg_tile_name = ''.join(upg_tile_name)
                self.upg_tile = self.tiles[self.upg_tile_name]
                self.upgp = self.upg_tile.buyupgprice
                self.tn_earn = self.upg_tile.earnings
                self.tn_main = self.upg_tile.maintenance

                self.tn_mdtopx = self.screen_centerx + self.box_w/4
                self.upg_centerx = (self.tn_mdtopx + self.xalign3)/2
                self.upgbtn_topleftx = self.upg_centerx - self.btn_w/2

                #Tier Next Heading
                self.tntxt = self.font_header.render('Tier '+self.tiernxt, True, self.c_black)
                self.tntxt_rect = self.tntxt.get_rect(midtop=(self.tn_mdtopx, self.tier_mdtopy))

                #TN Earnings
                self.tn_earntxta_rect = self.earntxta.get_rect(topleft=(self.xalign3, self.earntxt_y))

                self.tn_earntxtb = self.font_body2.render('+$'+str(self.tn_earn)+'/10 days', True, self.c_black)
                self.tn_earntxtb_rect = self.tn_earntxtb.get_rect(topright=(self.xalign4, self.earntxt_y))

                #TN Maintenance
                self.tn_maintxta_rect = self.maintxta.get_rect(topleft=(self.xalign3, self.maintxt_y))

                self.tn_maintxtb = self.font_body2.render('-$'+str(self.tn_main)+'/day', True, self.c_black)
                self.tn_maintxtb_rect = self.tn_maintxtb.get_rect(topright=(self.xalign4, self.maintxt_y))

                #Upgrade
                if self.buytile is None:
                    if not(self.grid[self.select_row][self.select_col] == 'Dirt0' or self.grid[self.select_row][self.select_col] == 'Field0' or self.grid[self.select_row][self.select_col] == 'Construct0'):
                        self.upgtxt = self.font_body.render('Upgrade', True, self.c_black)
                        self.upgtxt_rect = self.upgtxt.get_rect(center=(self.upg_centerx, self.sellremoveupgbuy_centery))

                        self.upgptxt = self.font_body2.render('-$'+str(self.upgp), True, self.c_black)
                        self.upgptxt_rect = self.upgptxt.get_rect(midright=(self.xalign4, self.sellremoveupgbuy_centery))

    def sell_tile(self):
        '''
        Sells the selected tile
        '''
        self.plowingtiles_dict[str(self.plowingtile_counter)] = ['Grass0', self.select_row, self.select_col, self.plowingtimer]
        self.grid[self.select_row][self.select_col] = 'Dirt0'
        self.money += self.sellp
        self.plowingtile_counter += 1
        self.grid_tilecycle[row][col] = 0
        self.persist['grid'] = self.grid
        self.persist['money'] = self.money
        self.persist['total_money_earned'] += self.sellp
        self.persist['plowingtiles_dict'] = self.plowingtiles_dict
        self.persist['plowingtile_counter'] = self.plowingtile_counter
        self.persist['grid_tilecycle'] = self.grid_tilecycle
        self.set_total_money_highest_lowest()
        self.next_state = 'Farm'
        self.done = True
        self.play_sfx(self.sfx_money)

    def upgrade_tile(self):
        '''
        Upgrades the selected tile
        '''
        self.grid[self.select_row][self.select_col] = self.upg_tile_name
        self.money -= self.upgp
        self.persist['grid'] = self.grid
        self.persist['total_money_spent'] += self.upgp
        self.persist['money'] = self.money
        self.set_total_money_highest_lowest()
        self.next_state = 'Farm'
        self.done = True
        self.play_sfx(self.sfx_money)

    def remove_tile(self):
        '''
        Removes the selected tile
        '''
        del self.plowingtiles_dict[self.plowingtile]
        self.plowingtiles_dict[str(self.plowingtile_counter)] = ['Grass0', self.select_row, self.select_col, self.plowingtimer]
        self.grid[self.select_row][self.select_col] = 'Dirt0'
        self.money -= self.removep
        self.plowingtile_counter += 1
        self.grid_tilecycle[self.select_row][self.select_col] = 0
        self.persist['grid'] = self.grid
        self.persist['total_money_spent'] += self.removep
        self.persist['money'] = self.money
        self.persist['plowingtiles_dict'] = self.plowingtiles_dict
        self.persist['plowingtile_counter'] = self.plowingtile_counter
        self.persist['grid_tilecycle'] = self.grid_tilecycle
        self.set_total_money_highest_lowest()
        self.next_state = 'Farm'
        self.done = True
        self.play_sfx(self.sfx_money)

    def buy_tile_or_not(self):
        '''
        Determines if the player can buy the selected tile
        '''
        if self.tile.tiletype == 'Crop':
            if self.tile.season == self.current_season or self.tile.season == 'All':
                self.next_state = 'Farm'
                self.done = True
                self.play_sfx(self.sfx_clicked)
            else:
                if self.tile_exists('Greenhouse'):
                    self.next_state = 'Farm'
                    self.done = True
                    self.play_sfx(self.sfx_clicked)
                else:
                    self.greenhouse_required = True
                    self.play_sfx(self.sfx_denied)
        elif self.tile.tiletype == 'Livestock':
            if self.tile_exists('Silo'):
                self.next_state = 'Farm'
                self.done = True
                self.play_sfx(self.sfx_clicked)
            else:
                self.silo_required = True
                self.play_sfx(self.sfx_denied)
        else:
            self.next_state = 'Farm'
            self.done = True
            self.play_sfx(self.sfx_clicked)

    def get_event(self, event):
        if event.type == QUIT:
            self.quit = True

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            if self.can_upgrade or self.sellremoveupg_msg or self.insufficent_money or self.greenhouse_required or self.silo_required:
                self.can_upgrade = False
                self.sellremoveupg_msg = False
                self.insufficent_money = False
                self.greenhouse_required = False
                self.silo_required = False
                self.play_sfx(self.sfx_clicked)
            else:
                self.persist['buytile'] = None
                self.next_state = 'Farm'
                self.done = True
                self.play_sfx(self.sfx_clicked)

        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.insufficent_money or self.greenhouse_required or self.silo_required or self.sellremoveupg_msg:
                if self.screen_centerx-self.msgbox.get_width()/2 < event.pos[0] < self.screen_centerx+self.msgbox.get_width()/2 and self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2 < event.pos[1] < self.screen_centery+self.msgbox.get_height()/2+self.msgbox_bordershift/2 and (self.insufficent_money or self.greenhouse_required or self.silo_required):
                    self.insufficent_money = False
                    self.greenhouse_required = False
                    self.silo_required = False
                    self.play_sfx(self.sfx_clicked)

                elif self.sellremoveupg_msg_yesno_y-self.sellremoveupg_msgtxt_yes.get_height()/2 < event.pos[1] < self.sellremoveupg_msg_yesno_y+self.sellremoveupg_msgtxt_yes.get_height()/2 and self.sellremoveupg_msg:
                    #Press Yes
                    if self.sellremoveupg_msgtxt_yes_x-self.sellremoveupg_msgtxt_yes.get_width()/2-self.btn_borderthick < event.pos[0] < self.sellremoveupg_msgtxt_yes_x+self.sellremoveupg_msgtxt_yes.get_width()/2+self.btn_borderthick:
                        if self.buytile is None:
                            if self.can_upgrade:
                                self.upgrade_tile()
                                self.can_upgrade = False
                                self.sellremoveupg_msg = False
                                self.play_sfx(self.sfx_money)
                            else:
                                if not(self.grid[self.select_row][self.select_col] == 'Dirt0' or self.grid[self.select_row][self.select_col] == 'Field0' or self.grid[self.select_row][self.select_col] == 'Construct0'):
                                    self.sell_tile()
                                    self.sellremoveupg_msg = False
                                    self.play_sfx(self.sfx_money)
                                else:
                                    self.remove_tile()
                                    self.sellremoveupg_msg = False
                                    self.play_sfx(self.sfx_money)

                    #Press No
                    elif self.sellremoveupg_msgtxt_no_x-self.sellremoveupg_msgtxt_yes.get_width()/2-self.btn_borderthick < event.pos[0] < self.sellremoveupg_msgtxt_no_x+self.sellremoveupg_msgtxt_yes.get_width()/2+self.btn_borderthick:
                        self.can_upgrade = False
                        self.sellremoveupg_msg = False
                        self.play_sfx(self.sfx_clicked)

            else:
                self.close_btn_farm(event)
                self.back_btn_farm(event)

                if self.btn_topy < event.pos[1] < self.btn_topy + self.btn_h:
                    if self.tile != self.tiles['Grass0']:
                        if self.sellbuybtn_topleftx < event.pos[0] < self.sellbuybtn_topleftx + self.btn_w:
                            if self.buytile is None:
                                self.sellremoveupg_msg = True
                                self.play_sfx(self.sfx_clicked)
                            else:
                                if self.money > 0:
                                    self.buy_tile_or_not()
                                else:
                                    self.insufficent_money = True
                                    self.play_sfx(self.sfx_denied)

                        elif self.upgbtn_topleftx < event.pos[0] < self.upgbtn_topleftx + self.btn_w and self.tiercrnt < 3 and self.buytile is None and not(self.grid[self.select_row][self.select_col] == 'Dirt0' or self.grid[self.select_row][self.select_col] == 'Field0' or self.grid[self.select_row][self.select_col] == 'Construct0'):
                            if self.money > 0:
                                self.can_upgrade = True
                                self.sellremoveupg_msg = True
                                self.play_sfx(self.sfx_clicked)

                            else:
                                self.insufficent_money = True
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

        #Draw text, close and back buttons
        surface.blit(self.title, self.title_rect)
        surface.blit(self.close_btntxt, self.close_btntxt_rect)
        surface.blit(self.back_btntxt, self.back_btntxt_rect)
        surface.blit(self.img, (self.img_x, self.img_y))

        #Draw text for tiles in development
        if self.subtitle is not None:
            surface.blit(self.subtitle, self.subtitle_rect)

        #Draw flavor text
        surface.blit(self.flavortxta, self.flavortxta_rect)
        surface.blit(self.flavortxtb, self.flavortxtb_rect)

        #Draw season text
        surface.blit(self.seasontxt, self.seasontxt_rect)

        #Draw structure area of effect info text
        if bool(self.upgtxt_list):
            for tier in self.upgtxt_list:
                txt = tier[0]
                txt_rect = tier[1]
                for nth_txt in range(len(txt)):
                    surface.blit(txt[nth_txt], txt_rect[nth_txt])

        #Draw info about current tier and next tier (if not tier 3)
        if self.tile != self.tiles['Grass0']:

            pg.draw.rect(surface, self.c_black, (self.sellbuybtn_topleftx, self.btn_topy, self.btn_w, self.btn_h), self.btn_borderthick)

            surface.blit(self.tctxt, self.tctxt_rect)
            surface.blit(self.earntxta, self.tc_earntxta_rect)
            surface.blit(self.tc_earntxtb, self.tc_earntxtb_rect)
            surface.blit(self.maintxta, self.tc_maintxta_rect)
            surface.blit(self.tc_maintxtb, self.tc_maintxtb_rect)

            if self.buytile is None:
                if not(self.grid[self.select_row][self.select_col] == 'Dirt0' or self.grid[self.select_row][self.select_col] == 'Field0' or self.grid[self.select_row][self.select_col] == 'Construct0'):
                    surface.blit(self.selltxt, self.selltxt_rect)
                    surface.blit(self.sellptxt, self.sellptxt_rect)
                else:
                    surface.blit(self.removetxt, self.removetxt_rect)
                    surface.blit(self.removeptxt, self.removeptxt_rect)
            else:
                surface.blit(self.buytxt, self.buytxt_rect)
                surface.blit(self.buyptxt, self.buyptxt_rect)

            if self.tiercrnt < 3:
                surface.blit(self.tntxt, self.tntxt_rect)

                surface.blit(self.earntxta, self.tn_earntxta_rect)
                surface.blit(self.tn_earntxtb, self.tn_earntxtb_rect)

                surface.blit(self.maintxta, self.tn_maintxta_rect)
                surface.blit(self.tn_maintxtb, self.tn_maintxtb_rect)

                if self.buytile is None:
                    if not(self.grid[self.select_row][self.select_col] == 'Dirt0' or self.grid[self.select_row][self.select_col] == 'Field0' or self.grid[self.select_row][self.select_col] == 'Construct0'):
                        pg.draw.rect(surface, self.c_black, (self.upgbtn_topleftx, self.btn_topy, self.btn_w, self.btn_h), self.btn_borderthick)

                        surface.blit(self.upgtxt, self.upgtxt_rect)
                        surface.blit(self.upgptxt, self.upgptxt_rect)

        #Draw popup for insufficient money
        if self.insufficent_money:
            surface.blit(self.msgbox, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2))
            pg.draw.rect(surface, self.c_black, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2, self.msgbox.get_width(), self.msgbox.get_height()), self.box_borderthick)
            surface.blit(self.buyupg_msgtxta, self.buyupg_msgtxta_rect)
            surface.blit(self.buyupg_msgtxtb, self.buyupg_msgtxtb_rect)
            surface.blit(self.buyupg_msgtxtc, self.buyupg_msgtxtc_rect)

        #Draw popup for greenhouse required
        if self.greenhouse_required:
            surface.blit(self.msgbox, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2))
            pg.draw.rect(surface, self.c_black, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2, self.msgbox.get_width(), self.msgbox.get_height()), self.box_borderthick)
            surface.blit(self.greenhouse_required_msgtxta, self.greenhouse_required_msgtxta_rect)
            surface.blit(self.greenhouse_required_msgtxtb, self.greenhouse_required_msgtxtb_rect)
            surface.blit(self.greenhouse_required_msgtxtc, self.greenhouse_required_msgtxtc_rect)

        #Draw popup for silo required
        if self.silo_required:
            surface.blit(self.msgbox, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2))
            pg.draw.rect(surface, self.c_black, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2, self.msgbox.get_width(), self.msgbox.get_height()), self.box_borderthick)
            surface.blit(self.silo_required_msgtxta, self.silo_required_msgtxta_rect)
            surface.blit(self.silo_required_msgtxtb, self.silo_required_msgtxtb_rect)
            surface.blit(self.silo_required_msgtxtc, self.silo_required_msgtxtc_rect)

        #Draw popup for selling, removing or upgrading a tile
        if self.sellremoveupg_msg:
            surface.blit(self.msgbox, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2))
            pg.draw.rect(surface, self.c_black, (self.screen_centerx-self.msgbox.get_width()/2, self.screen_centery-self.msgbox.get_height()/2+self.msgbox_bordershift/2, self.msgbox.get_width(), self.msgbox.get_height()), self.box_borderthick)
            pg.draw.rect(surface, self.c_lightgray, (self.sellremoveupg_msgtxt_yes_x-self.sellremoveupg_msgtxt_yes.get_width()/2-self.btn_borderthick, self.sellremoveupg_msg_yesno_y-self.sellremoveupg_msgtxt_yes.get_height()/2, self.sellremoveupg_msgtxt_yes.get_width()+2*self.btn_borderthick, self.sellremoveupg_msgtxt_yes.get_height()), self.btn_borderthick)
            pg.draw.rect(surface, self.c_lightgray, (self.sellremoveupg_msgtxt_no_x-self.sellremoveupg_msgtxt_yes.get_width()/2-self.btn_borderthick, self.sellremoveupg_msg_yesno_y-self.sellremoveupg_msgtxt_yes.get_height()/2, self.sellremoveupg_msgtxt_yes.get_width()+2*self.btn_borderthick, self.sellremoveupg_msgtxt_yes.get_height()), self.btn_borderthick)
            surface.blit(self.sellremoveupg_msgtxt, self.sellremoveupg_msgtxt_rect)
            surface.blit(self.sellremoveupg_msgtxt_yes, self.sellremoveupg_msgtxt_yes_rect)
            surface.blit(self.sellremoveupg_msgtxt_no, self.sellremoveupg_msgtxt_no_rect)
