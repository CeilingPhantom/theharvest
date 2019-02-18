'''
Manages the Farm screen
'''

#Import needed modules
import pygame as pg
from pygame.locals import *
from modules.Gamestate import Gamestate

class Farm(Gamestate):
    def __init__(self):

        super(Farm, self).__init__()

        #Initialise variables related to time
        self.current_month = None
        self.displaydatetxt = None
        self.displaydatetxt_rect = None

        self.background_dirt0_tiles_side = 160

        self.extbound = 5 #exterior bound, beyond the wdith and height of the screen
        self.sidebar_tile_yadjust = 25

        self.sidebar_topleft = -self.extbound
        self.sidebar_w = self.screen_width - self.viewablegrid_w*self.tile_side
        self.sidebar_h = self.screen_height + 2*self.extbound

        self.btmbar_topleftx = self.sidebar_w
        self.btmbar_toplefty = self.viewablegrid_h*self.tile_side

        self.btmbar_w = self.viewablegrid_w*self.tile_side + self.extbound
        self.btmbar_h = self.tile_side + self.extbound

        self.bordergfx_w = 90
        self.bordergfx_h = 20
        self.bordergfx_hor = pg.transform.scale(self.bordergfx_raw, (self.bordergfx_w, self.bordergfx_h))
        self.bordergfx_ver = pg.transform.rotate(self.bordergfx_hor, -90)

        self.sidebar_tiles_side = 100
        self.sidebar_tiles_dist = self.sidebar_tiles_side + self.sidebar_tile_yadjust

        self.displaydate_leftx = self.sidebar_w-self.bordergfx_h+self.tile_side/2

        self.displaytotalmoney_rightx = self.screen_width - 2*self.tile_side - self.bordergfx_h
        self.displaybtmbar_yalign = self.btmbar_toplefty + self.tile_side/2

        self.sidebar_highlight_borderthick = 5
        self.tile_highlight_borderthick = 4
        self.sidebar_tilestab_highlight_borderthick = 4

        self.tooltip = None
        self.tooltip_rect = None
        self.tooltip_x = None
        self.tooltip_y = None
        self.tooltipbox_w = None
        self.tooltipbox_h = None
        self.tooltiptile = None
        self.tooltipdisplayed = False

        self.tutorial_btntxt_rect_rightx = self.screen_width-11*self.tile_side/8
        self.tutorial_btntxt = self.font_title.render('?', True, self.c_white)
        self.tutorial_btntxt_rect = self.tutorial_btntxt.get_rect(center=(self.tutorial_btntxt_rect_rightx, self.displaybtmbar_yalign))

        self.options_btnimg_s = self.tile_side/2
        self.options_btnimg_rect_rightx = self.screen_width-5*self.tile_side/8
        self.options_btnimg = pg.transform.scale(self.options_btnimg_raw, (self.options_btnimg_s, self.options_btnimg_s))
        self.options_btnimg_rect = self.options_btnimg.get_rect(center=(self.options_btnimg_rect_rightx, self.displaybtmbar_yalign))

        seasongfx_summer_scale = 7
        seasongfx_scale = 4
        self.seasongfx_summer_w = self.seasongfx_summer_raw.get_width()*seasongfx_summer_scale
        self.seasongfx_summer_h = self.seasongfx_summer_raw.get_height()*seasongfx_summer_scale
        self.seasongfx_w = self.seasongfx_autumn_raw.get_width()*seasongfx_scale
        self.seasongfx_h = self.seasongfx_autumn_raw.get_height()*seasongfx_scale
        self.seasongfx_summer = pg.transform.scale(self.seasongfx_summer_raw, (self.seasongfx_summer_w, self.seasongfx_summer_h))
        self.seasongfx_autumn = pg.transform.scale(self.seasongfx_autumn_raw, (self.seasongfx_w, self.seasongfx_h))
        self.seasongfx_winter = pg.transform.scale(self.seasongfx_winter_raw, (self.seasongfx_w, self.seasongfx_h))
        self.seasongfx_spring = pg.transform.scale(self.seasongfx_spring_raw, (self.seasongfx_w, self.seasongfx_h))
        self.seasongfx_summer_topleft = (self.displaydate_leftx+3*self.tile_side, self.tile_side*self.viewablegrid_h+self.bordergfx_h)
        self.seasongfx_topy = self.screen_height - self.seasongfx_h
        self.seasongfx_count = self.screen_width/self.seasongfx_w + 1

    def startup(self, persistent):

        self.persist = persistent
        self.grid = self.persist['grid']
        self.grid_tilecycle = self.persist['grid_tilecycle']
        self.viewablegrid_topleft = self.persist['viewablegrid_topleft']
        self.money = self.persist['money']
        self.buytile = self.persist['buytile']
        self.timer = self.persist['timer']
        self.days_total = self.persist['days_total']
        self.days_seasonyear = self.persist['days_seasonyear']
        self.year = self.persist['year']
        self.plowingtiles_dict = self.persist['plowingtiles_dict']
        self.plowingtile_counter = self.persist['plowingtile_counter']
        self.plowingtimer = self.persist['plowingtimer']
        self.current_season = self.persist['current_season']
        self.select_sidebar_tilestab1 = self.persist['select_sidebar_tilestab1']
        self.greenhouse_tiles_season_all = self.persist['greenhouse_tiles_season_all']
        self.shed_tiles_reduced_plow = self.persist['shed_tiles_reduced_plow']
        self.silo_tiles_livestock_can = self.persist['silo_tiles_livestock_can']
        self.greenhouse_affectedtiles_lvl3 = self.persist['greenhouse_affectedtiles_lvl3']
        self.shed_affectedtiles_lvl3 = self.persist['shed_affectedtiles_lvl3']
        self.silo_affectedtiles_lvl3 = self.persist['silo_affectedtiles_lvl3']
        self.tile_imgs = self.persist['tile_imgs']
        self.sfxvol = self.persist['sfxvol']
        self.musicvol = self.persist['musicvol']

        self.viewablegrid_w_add = bool(self.viewablegrid_topleft['x']%self.tile_side)
        self.viewablegrid_h_add = bool(self.viewablegrid_topleft['y']%self.tile_side)

        #Reset autosave timer if player just saved
        if self.persist['saved']:
            self.persist['saved'] = False
            self.autosavetimer = 0
            self.persist['autosavetimer'] = self.autosavetimer
        else:
            self.autosavetimer = self.persist['autosavetimer']

        pg.time.set_timer(USEREVENT+1, self.cycle.timecycle)

        #Determine next plowingtile_counter from save
        if self.plowingtiles_dict:
            for plowingtile_key in self.plowingtiles_dict.keys():
                if int(plowingtile_key) > self.plowingtile_counter:
                    self.plowingtile_counter = int(plowingtile_key)
            self.plowingtile_counter += 1
            self.persist['plowingtile_counter'] = self.plowingtile_counter

        #Run
        self.calc_shed_tiles_reduced_plow()
        self.calc_greenhouse_tiles_season_all()
        self.calc_silo_tiles_livestock_can()
        self.calc_maintenance()
        self.calc_earnings()

        self.sidebar_bordergfx_hor_count = (self.sidebar_w+self.extbound)/self.bordergfx_w + 1
        self.sidebar_bordergfx_ver_count = self.sidebar_h/self.bordergfx_w + 1
        self.sidebar_bordergfx_right_topleftx = self.sidebar_w - self.bordergfx_h

        self.btmbar_bordergfx_hor_count = self.btmbar_w/self.bordergfx_w + 1
        self.btmbar_bordergfx_ver_count = self.btmbar_h/self.bordergfx_w + 1
        self.btmbar_bordergfx_right_leftx = self.screen_width - self.bordergfx_h

        self.btm_bordergfx_hor_count = (self.screen_width+2*self.extbound)/self.bordergfx_w + 1
        self.btm_bordergfx_topy = self.screen_height - self.bordergfx_h

        self.sidebar_tilestab_leftx1 = self.bordergfx_h
        self.sidebar_tilestab_leftx2 = self.sidebar_w/2 - self.bordergfx_h/2
        self.sidebar_tilestab_topy = self.bordergfx_h
        self.sidebar_tilestab_w = self.sidebar_w/2 - self.bordergfx_h
        self.sidebar_tilestab_h = 3*self.bordergfx_h/2
        self.sidebar_tilestab_yadjust = 3

        self.select_sidebar_tiles_topy = None
        self.sidebar_tiles_leftx = self.sidebar_w/2 - self.sidebar_tiles_side/2
        self.sidebar_tiles_topy = self.sidebar_tilestab_h + 2*self.sidebar_tile_yadjust + self.extbound

        self.sidebar_tile_highlight = None
        self.tile_highlight = None

        self.set_sidebar_tilestabtxt()
        self.set_display_total_money()
        self.calc_displaydate()
        self.kill_tiles()
        self.set_tile_imgs()

    def set_sidebar_tilestabtxt(self):
        '''
        Determines which tab of tiles to show on the sidebar
        '''
        self.sidebar_tilestab1txt = self.font_body3.render('1', True, self.c_white)
        self.sidebar_tilestab2txt = self.font_body3.render('2', True, self.c_white)

        if self.select_sidebar_tilestab1:
            self.sidebar_tilestab1txt_rect = self.sidebar_tilestab1txt.get_rect(topright=(self.sidebar_tilestab_leftx2-2*self.sidebar_highlight_borderthick, self.sidebar_tilestab_topy+self.sidebar_highlight_borderthick-self.sidebar_tilestab_yadjust))
            self.sidebar_tilestab2txt_rect = self.sidebar_tilestab2txt.get_rect(topright=(self.sidebar_bordergfx_right_topleftx-2*self.sidebar_highlight_borderthick, self.sidebar_tilestab_topy+self.sidebar_highlight_borderthick))

        else:
            self.sidebar_tilestab1txt_rect = self.sidebar_tilestab1txt.get_rect(topright=(self.sidebar_tilestab_leftx2-2*self.sidebar_highlight_borderthick, self.sidebar_tilestab_topy+self.sidebar_highlight_borderthick))
            self.sidebar_tilestab2txt_rect = self.sidebar_tilestab2txt.get_rect(topright=(self.sidebar_bordergfx_right_topleftx-2*self.sidebar_highlight_borderthick, self.sidebar_tilestab_topy+self.sidebar_highlight_borderthick-self.sidebar_tilestab_yadjust))

    def set_tile_imgs_afterbuy(self, row, col):
        '''
        Updates the visuals for a tile on the player's farm after a tile is bought
        '''
        self.tile_imgs[row-self.viewablegrid_topleft['y']/self.tile_side][col-self.viewablegrid_topleft['x']/self.tile_side] = pg.transform.scale(self.tiles[self.grid[row][col]].img0, (self.tile_side, self.tile_side))
        self.persist['tile_imgs'] = self.tile_imgs

    def set_tile_imgs(self):
        '''
        Updates the visuals for the player's farm
        '''
        self.tile_imgs = []
        for row in range(self.viewablegrid_h+int(self.viewablegrid_h_add)):
            self.tile_imgs.append([])
            for col in range(self.viewablegrid_w+int(self.viewablegrid_w_add)):
                viewrow = row+self.viewablegrid_topleft['y']/self.tile_side
                viewcol = col+self.viewablegrid_topleft['x']/self.tile_side
                tile_imgs_currentframe = self.grid_tilecycle[viewrow][viewcol]%self.cycle.tile_imgs_cycle
                if tile_imgs_currentframe/self.cycle.timecycle_sec_mult == 0:
                    drawtileimg = self.tiles[self.grid[viewrow][viewcol]].img0
                elif tile_imgs_currentframe/self.cycle.timecycle_sec_mult == 1:
                    drawtileimg = self.tiles[self.grid[viewrow][viewcol]].img1
                elif tile_imgs_currentframe/self.cycle.timecycle_sec_mult == 2:
                    drawtileimg = self.tiles[self.grid[viewrow][viewcol]].img2
                elif tile_imgs_currentframe/self.cycle.timecycle_sec_mult == 3:
                    drawtileimg = self.tiles[self.grid[viewrow][viewcol]].img3
                img = pg.transform.scale(drawtileimg, (self.tile_side, self.tile_side))
                self.tile_imgs[row].append(img)
        self.persist['tile_imgs'] = self.tile_imgs

    def set_display_total_money(self):
        '''
        Updates the display for how much money the player currently owns
        '''
        if self.money < 0:
            money_sign = '-$'
            money = abs(self.money)
            moneytxt_color = self.c_red
        else:
            money_sign = '$'
            money = self.money
            moneytxt_color = self.c_white
        self.moneytxt = self.font_body.render(money_sign+str(int(money)), True, moneytxt_color)
        self.moneytxt_rect = self.moneytxt.get_rect(midright=(self.displaytotalmoney_rightx, self.displaybtmbar_yalign))

    def calc_displaydate(self):
        '''
        Calculates and updates the display for the current season and date
        '''
        if self.year < 3:
            self.yeartype = self.cycle.year_norm
        elif self.year == 3:
            self.yeartype = self.cycle.year_leap
        days_months = 0
        for month in self.cycle.months:
            days_months += self.yeartype[month][1]
            if self.days_seasonyear < days_months:
                self.current_month = month
                current_day = str(self.yeartype[month][1] - (days_months - self.days_seasonyear)+1)
                self.displaydatetxt = self.font_body.render(self.yeartype[month][2]+', '+self.yeartype[month][0]+' '+current_day, True, self.c_white)
                self.displaydatetxt_rect = self.displaydatetxt.get_rect(midleft=(self.displaydate_leftx, self.displaybtmbar_yalign))
                break

    def convert_tile_to_dirt(self, row, col):
        '''
        Turns a tile into a dirt tile
        '''
        self.plowingtiles_dict[str(self.plowingtile_counter)] = ['Grass0', row, col, self.plowingtimer]
        self.grid[row][col] = 'Dirt0'
        self.plowingtile_counter += 1
        self.grid_tilecycle[row][col] = 0
        self.persist['grid'] = self.grid
        self.persist['plowingtiles_dict'] = self.plowingtiles_dict
        self.persist['plowingtile_counter'] = self.plowingtile_counter
        self.persist['grid_tilecycle'] = self.grid_tilecycle
        self.set_tile_imgs_afterbuy(row, col)

    def kill_tiles(self):
        '''
        Turns tiles on the farm that should not exist at the current time into dirt tiles

        The current seasons, and the existence of greenhouses and silos on the player's farm impact this
        '''
        self.current_season = self.yeartype[self.current_month][2]
        self.persist['current_season'] = self.current_season
        for row in range(self.grid_h):
            for col in range(self.grid_w):
                if self.tiles[self.grid[row][col]].tiletype == 'Crop' and not(self.tiles[self.grid[row][col]].season == self.current_season or self.tiles[self.grid[row][col]].season == 'All' or self.greenhouse_tiles_season_all[row][col]):
                    self.convert_tile_to_dirt(row, col)
                elif self.tiles[self.grid[row][col]].tiletype == 'Livestock' and not self.silo_tiles_livestock_can[row][col]:
                    self.convert_tile_to_dirt(row, col)
                for plowingtile in self.plowingtiles_dict.keys():
                    if self.plowingtiles_dict[plowingtile][1] == row and self.plowingtiles_dict[plowingtile][2] == col:
                        if self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Crop' and not(self.tiles[self.plowingtiles_dict[plowingtile][0]].season == self.current_season or self.tiles[self.plowingtiles_dict[plowingtile][0]].season == 'All' or self.greenhouse_tiles_season_all[row][col]):
                            del self.plowingtiles_dict[plowingtile]
                            self.convert_tile_to_dirt(row, col)
                            break
                        elif self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Livestock' and not self.silo_tiles_livestock_can[row][col]:
                            del self.plowingtiles_dict[plowingtile]
                            self.convert_tile_to_dirt(row, col)
                            break


    def find_structure(self, structure):
        '''
        Finds a certain tile and returns how many of that tile exist on the player's farm
        '''
        structure_count = 0
        for row in self.grid:
            for tile in row:
                if tile == structure:
                    structure_count += 1
        return structure_count

    def calc_structure_radius(self, structure):
        '''
        Calculates which tiles are affected by structure effects
        '''
        if bool(self.find_structure(structure)):
            structure_radius_list = []
            found_structures = []
            for row in range(self.grid_h):
                for col in range(self.grid_w):
                    if self.grid[row][col] == structure:
                        found_structures.append({'row': row, 'col': col})
            for nth_structure in range(self.find_structure(structure)):
                radius_minrow = found_structures[nth_structure]['row'] - self.structures[structure].radius
                radius_mincol = found_structures[nth_structure]['col'] - self.structures[structure].radius
                radius_maxrow = found_structures[nth_structure]['row'] + self.structures[structure].radius + 1
                radius_maxcol = found_structures[nth_structure]['col'] + self.structures[structure].radius + 1
                if self.shed_affectedtiles_lvl3[found_structures[nth_structure]['row']][found_structures[nth_structure]['col']] and self.tiles[self.grid[found_structures[nth_structure]['row']][found_structures[nth_structure]['row']]].displayname != 'Shed':
                    radius_minrow -= self.structures['Shed3'].lvl3_aoe_upg
                    radius_mincol -= self.structures['Shed3'].lvl3_aoe_upg
                    radius_maxrow += self.structures['Shed3'].lvl3_aoe_upg
                    radius_maxcol += self.structures['Shed3'].lvl3_aoe_upg
                if radius_minrow < 0:
                    radius_minrow = 0
                if radius_maxrow > self.grid_h:
                    radius_maxrow = self.grid_h
                if radius_mincol < 0:
                    radius_mincol = 0
                if radius_maxcol > self.grid_w:
                    radius_maxcol = self.grid_w
                structure_radius_list.append((radius_minrow, radius_maxrow, radius_mincol, radius_maxcol))
            return structure_radius_list

    def greenhouse_aoe(self, greenhouse):
        '''
        Determines which tiles are affected by a certain greenhouse tier's area of effect
        '''
        if bool(self.calc_structure_radius(greenhouse)):
            for nth_structure in range(self.find_structure(greenhouse)):
                (radius_minrow, radius_maxrow, radius_mincol, radius_maxcol) = self.calc_structure_radius(greenhouse)[nth_structure]
                for row in range(radius_minrow, radius_maxrow):
                    for col in range(radius_mincol, radius_maxcol):
                        self.greenhouse_tiles_season_all[row][col] = True
                        if greenhouse == 'Greenhouse3':
                            self.greenhouse_affectedtiles_lvl3[row][col] += 1

    def shed_aoe(self, shed):
        '''
        Determines which tiles are affected by a certain shed tier's area of effect
        '''
        if bool(self.calc_structure_radius(shed)):
            for nth_structure in range(self.find_structure(shed)):
                (radius_minrow, radius_maxrow, radius_mincol, radius_maxcol) = self.calc_structure_radius(shed)[nth_structure]
                for row in range(radius_minrow, radius_maxrow):
                    for col in range(radius_mincol, radius_maxcol):
                        self.shed_tiles_reduced_plow[row][col] = True

    def silo_aoe(self, silo):
        '''
        Determines which tiles are affected by a certain silo tier's area of effect
        '''
        if bool(self.calc_structure_radius(silo)):
            for nth_structure in range(self.find_structure(silo)):
                (radius_minrow, radius_maxrow, radius_mincol, radius_maxcol) = self.calc_structure_radius(silo)[nth_structure]
                for row in range(radius_minrow, radius_maxrow):
                    for col in range(radius_mincol, radius_maxcol):
                        self.silo_tiles_livestock_can[row][col] = True
                        if silo == 'Silo3':
                            self.silo_affectedtiles_lvl3[row][col] += 1

    def shed_tier3_aoe(self):
        '''
        Determines which tiles are affected by the shed's tier 3 area of effect
        '''
        if bool(self.calc_structure_radius('Shed3')):
            for nth_structure in range(self.find_structure('Shed3')):
                (radius_minrow, radius_maxrow, radius_mincol, radius_maxcol) = self.calc_structure_radius('Shed3')[nth_structure]
                for row in range(radius_minrow, radius_maxrow):
                    for col in range(radius_mincol, radius_maxcol):
                        if self.tiles[self.grid[row][col]].displayname != 'Shed':
                            self.shed_affectedtiles_lvl3[row][col] = True


    def calc_greenhouse_tiles_season_all(self):
        '''
        Determines which tiles are affected by the greenhouse's area of effect
        '''
        self.greenhouse_tiles_season_all = []
        self.greenhouse_affectedtiles_lvl3 = []
        for row in range(self.grid_h):
            self.greenhouse_tiles_season_all.append([])
            self.greenhouse_affectedtiles_lvl3.append([])
            for col in range(self.grid_w):
                self.greenhouse_tiles_season_all[row].append(False)
                self.greenhouse_affectedtiles_lvl3[row].append(0)
        self.greenhouse_aoe('Greenhouse1')
        self.greenhouse_aoe('Greenhouse2')
        self.greenhouse_aoe('Greenhouse3')
        self.persist['greenhouse_tiles_season_all'] = self.greenhouse_tiles_season_all
        self.persist['greenhouse_affectedtiles_lvl3'] = self.greenhouse_affectedtiles_lvl3

    def calc_shed_tiles_reduced_plow(self):
        '''
        Determines which tiles are affected by the shed's area of effect
        '''
        self.shed_tiles_reduced_plow = []
        self.shed_affectedtiles_lvl3 = []
        for row in range(self.grid_h):
            self.shed_tiles_reduced_plow.append([])
            self.shed_affectedtiles_lvl3.append([])
            for col in range(self.grid_w):
                self.shed_tiles_reduced_plow[row].append(False)
                self.shed_affectedtiles_lvl3[row].append(False)
        self.shed_tier3_aoe()
        self.shed_aoe('Shed1')
        self.shed_aoe('Shed2')
        self.shed_aoe('Shed3')
        self.persist['shed_tiles_reduced_plow'] = self.shed_tiles_reduced_plow
        self.persist['shed_affectedtiles_lvl3'] = self.shed_affectedtiles_lvl3

    def calc_silo_tiles_livestock_can(self):
        '''
        Determines which tiles are affected by the silo's area of effect
        '''
        self.silo_tiles_livestock_can = []
        self.silo_affectedtiles_lvl3 = []
        for row in range(self.grid_h):
            self.silo_tiles_livestock_can.append([])
            self.silo_affectedtiles_lvl3.append([])
            for col in range(self.grid_w):
                self.silo_tiles_livestock_can[row].append(False)
                self.silo_affectedtiles_lvl3[row].append(0)
        self.silo_aoe('Silo1')
        self.silo_aoe('Silo2')
        self.silo_aoe('Silo3')
        self.persist['silo_tiles_livestock_can'] = self.silo_tiles_livestock_can
        self.persist['silo_affectedtiles_lvl3'] = self.silo_affectedtiles_lvl3

    def reset_plowingtile_counter(self):
        '''
        Resets the counter for tiles in development
        '''
        if not self.plowingtiles_dict:
            self.plowingtile_counter = 0

    def evolve_tiles(self):
        '''
        Advances tiles in development
        '''
        for plowingtile in self.plowingtiles_dict.keys():
            #row in grid
            select_row = self.plowingtiles_dict[plowingtile][1]
            #column in grid
            select_col = self.plowingtiles_dict[plowingtile][2]
            evolvecycle = 0
            if self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Crop':
                evolvecycle = self.cycle.evolvecycle_crop
            elif self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Livestock':
                evolvecycle = self.cycle.evolvecycle_livestock
            elif self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Structure':
                evolvecycle = self.cycle.evolvecycle_structure
            elif self.plowingtiles_dict[plowingtile][0] == 'Grass0':
                evolvecycle = self.cycle.evolvecycle_grass
            if self.grid_tilecycle[select_row][select_col]%evolvecycle == 0:
                if self.plowingtiles_dict[plowingtile][0] == 'Grass0' or self.plowingtiles_dict[plowingtile][3] == 1 or self.shed_tiles_reduced_plow[select_row][select_col]:
                    self.grid[select_row][select_col] = self.plowingtiles_dict[plowingtile][0] #tile name
                    del self.plowingtiles_dict[plowingtile]
                    self.persist['grid'] = self.grid
                    self.persist['plowingtiles_dict'] = self.plowingtiles_dict
                else: #plowingtimer
                    self.plowingtiles_dict[plowingtile][3] += 1
                    if self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Crop':
                        self.grid[select_row][select_col] = 'Field0'
                        self.persist['grid'] = self.grid
                    elif self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Livestock' or self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Structure':
                        self.grid[select_row][select_col] = 'Construct0'
                        self.persist['grid'] = self.grid
                    self.persist['plowingtiles_dict'] = self.plowingtiles_dict
                #Reset timer for tile in development/that has been finished
                self.grid_tilecycle[select_row][select_col] = 0
                self.persist['grid_tilecycle'] = self.grid_tilecycle
                self.set_tile_imgs_afterbuy(select_row, select_col)
        self.calc_shed_tiles_reduced_plow()
        self.calc_greenhouse_tiles_season_all()
        self.calc_silo_tiles_livestock_can()
        self.reset_plowingtile_counter()
        self.kill_tiles()

    def set_highlight(self):
        '''
        Highlights the tile being bought from the sidebar and the grid tile which the player's mouse is hovering over on the player's farm
        '''
        pos = pg.mouse.get_pos()
        if self.buytile is not None:
            if self.select_sidebar_tilestab1:
                select_sidebar_tilestab = self.tilestobuya
            else:
                select_sidebar_tilestab = self.tilestobuyb
            for nth_tile, tile in enumerate(select_sidebar_tilestab):
                if tile == self.buytile:
                    self.select_sidebar_tiles_topy = self.sidebar_tiles_topy + nth_tile*self.sidebar_tiles_dist
            if self.sidebar_w <= pos[0] <= self.screen_width and 0 <= pos[1] <= self.btmbar_toplefty:
                select_col = (pos[0] - self.sidebar_w)/self.tile_side + self.viewablegrid_topleft['x']/self.tile_side
                select_row = pos[1]/self.tile_side + self.viewablegrid_topleft['y']/self.tile_side
                if not self.viewablegrid_w_add and select_col >= self.viewablegrid_topleft['x']/self.tile_side + self.viewablegrid_w:
                    select_col -= 1
                if not self.viewablegrid_h_add and select_row >= self.viewablegrid_topleft['y']/self.tile_side + self.viewablegrid_h:
                    select_row -= 1
                self.tile_highlight_x = self.sidebar_w + (select_col-self.viewablegrid_topleft['x']/self.tile_side)*self.tile_side - self.viewablegrid_topleft['x']
                self.tile_highlight_y = (select_row-self.viewablegrid_topleft['y']/self.tile_side)*self.tile_side
                if self.money > 0:
                    if self.grid[select_row][select_col] == 'Grass0':
                        if self.tiles[self.buytile].tiletype == 'Crop':
                            if self.tiles[self.buytile].season == 'All' or self.tiles[self.buytile].season == self.current_season:
                                self.sidebar_tile_highlight = True
                                self.tile_highlight = True
                            elif self.tile_exists('Greenhouse'):
                                self.sidebar_tile_highlight = True
                                if self.greenhouse_tiles_season_all[select_row][select_col]:
                                #if selected, and season passes sidebar remains true
                                    self.tile_highlight = True
                                else:
                                    self.tile_highlight = False
                            else:
                                self.sidebar_tile_highlight = False
                                self.tile_highlight = False
                        elif self.tiles[self.buytile].tiletype == 'Livestock':
                            if self.tile_exists('Silo'):
                                self.sidebar_tile_highlight = True
                                if self.silo_tiles_livestock_can[select_row][select_col]:
                                    self.tile_highlight = True
                                else:
                                    self.tile_highlight = False
                            else:
                                self.sidebar_tile_highlight = False
                                self.tile_highlight = False
                        elif self.tiles[self.buytile].tiletype == 'Structure':
                            self.sidebar_tile_highlight = True
                            self.tile_highlight = True
                        else:
                            self.sidebar_tile_highlight = True
                            self.tile_highlight = False
                    else:
                        self.sidebar_tile_highlight = True
                        self.tile_highlight = False
                else:
                    self.sidebar_tile_highlight = False
                    self.tile_highlight = False
            else:
                if self.money > 0:
                    if self.tiles[self.buytile].tiletype == 'Crop':
                        if self.tiles[self.buytile].season == 'All' or self.tiles[self.buytile].season == self.current_season or self.tile_exists('Greenhouse'):
                            self.sidebar_tile_highlight = True
                    elif self.tiles[self.buytile].tiletype == 'Livestock':
                        if self.tile_exists('Silo'):
                            self.sidebar_tile_highlight = True
                    elif self.tiles[self.buytile].tiletype == 'Structure':
                        self.sidebar_tile_highlight = True
                    else:
                        self.sidebar_tile_highlight = True
                else:
                    self.sidebar_tile_highlight = False
                self.tile_highlight = None
        else:
            self.sidebar_tile_highlight = None
            self.tile_highlight = None

    def set_tooltip(self):
        '''
        Determines if the tooltip showing the name of the tile which the player's mouse is hovering over in the sidebar should be shown.
        '''
        pos = pg.mouse.get_pos()
        if self.sidebar_tiles_leftx < pos[0] < self.sidebar_tiles_leftx+self.sidebar_tiles_side:
            if self.select_sidebar_tilestab1:
                select_sidebar_tilestab = self.tilestobuya
            else:
                select_sidebar_tilestab = self.tilestobuyb
            for nth_tile in range(len(select_sidebar_tilestab)):
                select_sidebar_tiles_topy = self.sidebar_tiles_topy+nth_tile*self.sidebar_tiles_dist
                if select_sidebar_tiles_topy < pos[1] < select_sidebar_tiles_topy+self.sidebar_tiles_side:
                    if not self.tooltipdisplayed and self.tooltiptile != select_sidebar_tilestab[nth_tile]:
                        self.tooltiptile = select_sidebar_tilestab[nth_tile]
                        self.tooltipdisplayed = True
                        tilename = self.tiles[self.tooltiptile].displayname
                        self.tooltip = self.font_body.render(tilename, True, self.c_blue)
                        self.tooltip_rect = self.tooltip.get_rect(topleft=(pos))
                        self.tooltip_x = pos[0]
                        self.tooltip_y = pos[1]
                        self.tooltipbox_w = self.tooltip_rect.w
                        self.tooltipbox_h = self.tooltip_rect.h
                    break
            else:
                self.tooltiptile = None
                self.tooltipdisplayed = False
        elif not self.sidebar_tiles_leftx < pos[0] < self.sidebar_tiles_leftx + self.sidebar_tiles_side:
            self.tooltiptile = None
            self.tooltipdisplayed = False

    def goto_tutorial(self, event):
        '''
        Determines when to go to the Tutorial screen
        '''
        if self.tutorial_btntxt_rect_rightx-self.tutorial_btntxt_rect.w/2 < event.pos[0] < self.tutorial_btntxt_rect_rightx+self.tutorial_btntxt_rect.w/2 and (self.displaybtmbar_yalign-self.tutorial_btntxt_rect.h/2 < event.pos[1] < self.displaybtmbar_yalign+self.tutorial_btntxt_rect.h/2 and self.btmbar_toplefty+self.bordergfx_h < event.pos[1] < self.screen_height-self.bordergfx_h):
            self.done = True
            self.next_state = 'Tutorial'
            self.play_sfx(self.sfx_clicked)
            self.save_background_img()

    def goto_options(self, event):
        '''
        Determines when to go to the Options screen
        '''
        if self.options_btnimg_rect_rightx-self.options_btnimg_rect.w/2 < event.pos[0] < self.options_btnimg_rect_rightx+self.options_btnimg_rect.w/2 and (self.displaybtmbar_yalign-self.options_btnimg_rect.h/2 < event.pos[1] < self.displaybtmbar_yalign+self.options_btnimg_rect.h/2 and self.btmbar_toplefty+self.bordergfx_h < event.pos[1] < self.screen_height-self.bordergfx_h):
            self.done = True
            self.next_state = 'Options'
            self.play_sfx(self.sfx_clicked)
            self.save_background_img()

    def goto_money(self, event):
        '''
        Determines when to go to the Money screen
        '''
        if self.displaytotalmoney_rightx-self.moneytxt_rect.w < event.pos[0] < self.displaytotalmoney_rightx and (self.displaybtmbar_yalign-self.moneytxt_rect.h/2 < event.pos[1] < self.displaybtmbar_yalign+self.moneytxt_rect.h/2 and self.btmbar_toplefty+self.bordergfx_h < event.pos[1] < self.screen_height-self.bordergfx_h):
            self.done = True
            self.next_state = 'Money'
            self.play_sfx(self.sfx_clicked)
            self.save_background_img()

    def grid_tilecycle_advance(self):
        '''
        Advances each tile's timer and cycle
        '''
        for row in range(self.grid_h):
            for col in range(self.grid_w):
                self.grid_tilecycle[row][col] += 1
        self.grid_tilecycle = self.persist['grid_tilecycle']

    def calc_earnings(self):
        '''
        Calculate earnings as of current second
        '''
        thisday_earnings = 0.0
        for row in range(self.grid_h):
            for col in range(self.grid_w):
                earncycle = 0
                if self.tiles[self.grid[row][col]].tiletype == 'Crop':
                    earncycle = self.cycle.earncycle_crop
                elif self.tiles[self.grid[row][col]].tiletype == 'Livestock':
                    earncycle = self.cycle.earncycle_livestock
                if earncycle:
                    if self.grid_tilecycle[row][col]%earncycle == 0:
                        earnings = float(self.tiles[self.grid[row][col]].earnings)
                        if self.greenhouse_affectedtiles_lvl3[row][col] and self.tiles[self.grid[row][col]].tiletype == 'Crop':
                            earnings = float(earnings)*(1.0+self.structures['Greenhouse3'].lvl3_aoe_upg)**float(self.greenhouse_affectedtiles_lvl3[row][col])
                        elif self.silo_affectedtiles_lvl3[row][col] and self.tiles[self.grid[row][col]].tiletype == 'Livestock':
                            earnings = float(earnings)*(1.0+self.structures['Silo3'].lvl3_aoe_upg)**float(self.silo_affectedtiles_lvl3[row][col])
                        thisday_earnings += earnings
        self.persist['thisday_earnings'] = thisday_earnings
        return thisday_earnings

    def calc_maintenance(self):
        '''
        Calculate maintenance as of current second
        '''
        thisday_maintenance = 0.0
        for row in range(self.grid_h):
            for col in range(self.grid_w):
                maincycle = 0
                if self.tiles[self.grid[row][col]].tiletype == 'Crop':
                    maincycle = self.cycle.maincycle_crop
                elif self.tiles[self.grid[row][col]].tiletype == 'Livestock':
                    maincycle = self.cycle.maincycle_livestock
                elif self.tiles[self.grid[row][col]].tiletype == 'Structure':
                    maincycle = self.cycle.maincycle_structure
                if maincycle:
                    if self.grid_tilecycle[row][col]%maincycle == 0:
                        maintenance = self.tiles[self.grid[row][col]].maintenance
                        if self.greenhouse_affectedtiles_lvl3[row][col] and self.tiles[self.grid[row][col]].tiletype == 'Crop':
                            maintenance = float(maintenance)*(1.0-self.structures['Greenhouse3'].lvl3_aoe_upg)**float(self.greenhouse_affectedtiles_lvl3[row][col])
                        elif self.silo_affectedtiles_lvl3[row][col] and self.tiles[self.grid[row][col]].tiletype == 'Livestock':
                            maintenance = float(maintenance)*(1.0-self.structures['Silo3'].lvl3_aoe_upg)**float(self.silo_affectedtiles_lvl3[row][col])
                        thisday_maintenance += maintenance

        for plowingtile in self.plowingtiles_dict.keys():
            plow_maincycle = 0
            if self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Crop':
                plow_maincycle = self.cycle.maincycle_crop
            elif self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Livestock':
                plow_maincycle = self.cycle.maincycle_livestock
            elif self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Structure':
                plow_maincycle = self.cycle.maincycle_structure
            if plow_maincycle:
                if self.grid_tilecycle[self.plowingtiles_dict[plowingtile][1]][self.plowingtiles_dict[plowingtile][2]]%plow_maincycle == 0:
                    maintenance = self.tiles[self.plowingtiles_dict[plowingtile][0]].maintenance
                    if self.greenhouse_affectedtiles_lvl3[self.plowingtiles_dict[plowingtile][1]][self.plowingtiles_dict[plowingtile][2]] and self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Crop':
                        maintenance = float(maintenance)*(1.0-self.structures['Greenhouse3'].lvl3_aoe_upg)**float(self.greenhouse_affectedtiles_lvl3[self.plowingtiles_dict[plowingtile][1]][self.plowingtiles_dict[plowingtile][2]])
                    elif self.silo_affectedtiles_lvl3[self.plowingtiles_dict[plowingtile][1]][self.plowingtiles_dict[plowingtile][2]] and self.tiles[self.plowingtiles_dict[plowingtile][0]].tiletype == 'Livestock':
                        maintenance = float(maintenance)*(1.0-self.structures['Silo3'].lvl3_aoe_upg)**float(self.silo_affectedtiles_lvl3[self.plowingtiles_dict[plowingtile][1]][self.plowingtiles_dict[plowingtile][2]])
                    thisday_maintenance += maintenance
        self.persist['thisday_maintenance'] = thisday_maintenance
        return thisday_maintenance

    def earnings(self):
        thisday_earnings = self.calc_earnings()
        #print thisday_earnings
        self.money += thisday_earnings
        self.persist['total_money_earned'] += thisday_earnings
        self.persist['money'] = self.money
        self.set_total_money_highest_lowest()

    def maintenance(self):
        thisday_maintenance = self.calc_maintenance()
        #print thisday_maintenance
        self.money -= thisday_maintenance
        self.persist['total_money_spent'] += thisday_maintenance
        self.persist['money'] = self.money
        self.set_total_money_highest_lowest()

    def get_event(self, event):

        if event.type == QUIT:
            self.quit = True

        #Shifting up and down the viewable grid
        keyspressed = pg.key.get_pressed()
        if keyspressed[pg.K_w]:
            if self.viewablegrid_topleft['y'] > 0:
                self.viewablegrid_topleft['y'] -= 1
                self.persist['viewablegrid_topleft'] = self.viewablegrid_topleft
                self.viewablegrid_h_add = bool(self.viewablegrid_topleft['y']%self.tile_side)
                self.set_tile_imgs()

        if keyspressed[pg.K_a]:
            if self.viewablegrid_topleft['x'] > 0:
                self.viewablegrid_topleft['x'] -= 1
                self.persist['viewablegrid_topleft'] = self.viewablegrid_topleft
                self.viewablegrid_w_add = bool(self.viewablegrid_topleft['x']%self.tile_side)
                self.set_tile_imgs()

        if keyspressed[pg.K_s]:
            if self.viewablegrid_topleft['y'] < (self.grid_h-self.viewablegrid_h)*self.tile_side:
                self.viewablegrid_topleft['y'] += 1
                self.persist['viewablegrid_topleft'] = self.viewablegrid_topleft
                self.viewablegrid_h_add = bool(self.viewablegrid_topleft['y']%self.tile_side)
                self.set_tile_imgs()

        if keyspressed[pg.K_d]:
            if self.viewablegrid_topleft['x'] < (self.grid_w-self.viewablegrid_w)*self.tile_side:
                self.viewablegrid_topleft['x'] += 1
                self.persist['viewablegrid_topleft'] = self.viewablegrid_topleft
                self.viewablegrid_w_add = bool(self.viewablegrid_topleft['x']%self.tile_side)
                self.set_tile_imgs()

        #Functionality that works around time
        elif event.type == USEREVENT+1:
            self.timer += 1
            #print self.timer
            self.autosavetimer += 1
            self.persist['timer'] = self.timer
            self.persist['autosavetimer'] = self.autosavetimer
            self.grid_tilecycle_advance()
            #print self.grid_tilecycle
            self.earnings()
            self.maintenance()

            #Add days
            if self.timer%self.cycle.day == 0:
                self.days_total += 1
                self.days_seasonyear += 1
                self.persist['days_total'] = self.days_total
                self.persist['days_seasonyear'] = self.days_seasonyear

            self.evolve_tiles() #must be AFTER earnings done

            #Autosave
            if self.autosavetimer == self.cycle.autosave_cycle:
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
                self.autosavetimer = 0
                self.persist['autosavetimer'] = self.autosavetimer

            #Update tile img displayed on farm
            self.set_tile_imgs()

            #Years
            if self.year < 3 and self.days_seasonyear == self.cycle.year_normcycle: #end of a normal year
                self.days_seasonyear = 0
                self.year += 1
                self.persist['days_seasonyear'] = self.days_seasonyear
                self.persist['year'] = self.year
            elif self.year == 3 and self.days_seasonyear == self.cycle.year_leapcycle: #end of a leap year
                self.days_seasonyear = 0
                self.year = 0
                self.persist['days_seasonyear'] = self.days_seasonyear
                self.persist['year'] = self.year

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            if self.buytile is None:
                self.next_state = 'Options'
                self.done = True
                self.play_sfx(self.sfx_clicked)
                self.save_background_img()
            else:
                self.buytile = None
                self.persist['buytile'] = self.buytile

        #cheats

        #Plus money
        elif event.type == KEYDOWN and event.key == K_f:
            self.money += 1000
            self.persist['money'] = self.money

        #Advance timer
        elif event.type == KEYDOWN and event.key == K_g:
            self.timer += 1
            #print self.timer
            self.persist['timer'] = self.timer
            self.grid_tilecycle_advance()
            #print self.grid_tilecycle
            self.earnings()
            self.maintenance()

            #Add days
            if self.timer%self.cycle.day == 0:
                self.days_total += 1
                self.days_seasonyear += 1
                self.persist['days_total'] = self.days_total
                self.persist['days_seasonyear'] = self.days_seasonyear

            self.evolve_tiles() #must be AFTER earnings done

            #Update tile img displayed on farm
            self.set_tile_imgs()

            #Years
            if self.year < 3 and self.days_seasonyear == self.cycle.year_normcycle: #end of a normal year
                self.days_seasonyear = 0
                self.year += 1
                self.persist['days_seasonyear'] = self.days_seasonyear
                self.persist['year'] = self.year
            elif self.year == 3 and self.days_seasonyear == self.cycle.year_leapcycle: #end of a leap year
                self.days_seasonyear = 0
                self.year = 0
                self.persist['days_seasonyear'] = self.days_seasonyear
                self.persist['year'] = self.year
        
        #end of cheats

        elif event.type == MOUSEBUTTONDOWN:
            # right click, cancel action
            if event.button == 3:
                if self.buytile is not None:
                    self.buytile = None
                    self.persist['buytile'] = self.buytile
                    self.play_sfx(self.sfx_clicked)

            # middle click, drag grid around
            #if event.button == 2:

            # left click, do action
            elif event.button == 1:
                if self.sidebar_w <= event.pos[0] <= self.screen_width and 0 <= event.pos[1] <= self.btmbar_toplefty:
                    select_col = (event.pos[0] - self.sidebar_w)/self.tile_side + self.viewablegrid_topleft['x']/self.tile_side
                    select_row = event.pos[1]/self.tile_side + self.viewablegrid_topleft['y']/self.tile_side
                    if not self.viewablegrid_w_add and select_col >= self.viewablegrid_topleft['x']/self.tile_side + self.viewablegrid_w:
                        select_col -= 1
                    if not self.viewablegrid_h_add and select_row >= self.viewablegrid_topleft['y']/self.tile_side + self.viewablegrid_h:
                        select_row -= 1

                    #Go to Tile screen
                    if self.buytile is None:
                        self.persist['select_col'] = select_col
                        self.persist['select_row'] = select_row
                        self.next_state = 'Tile'
                        self.done = True
                        self.play_sfx(self.sfx_clicked)
                        self.save_background_img()

                    #Place selected tile
                    else:
                        if self.grid[select_row][select_col] == 'Grass0':
                            if self.money > 0:
                                if self.tiles[self.buytile].tiletype == 'Crop':
                                    if self.tiles[self.buytile].season == 'All' or self.tiles[self.buytile].season == self.current_season or self.greenhouse_tiles_season_all[select_row][select_col]:
                                        self.plowingtiles_dict[str(self.plowingtile_counter)] = [self.buytile, select_row, select_col, self.plowingtimer]
                                        self.grid[select_row][select_col] = 'Dirt0'
                                        self.money -= self.tiles[self.buytile].buyupgprice
                                        self.plowingtile_counter += 1
                                        self.grid_tilecycle[select_row][select_col] = 0
                                        self.persist['grid'] = self.grid
                                        self.persist['total_money_spent'] += self.tiles[self.buytile].buyupgprice
                                        self.persist['money'] = self.money
                                        self.persist['plowingtiles_dict'] = self.plowingtiles_dict
                                        self.persist['plowingtile_counter'] = self.plowingtile_counter
                                        self.persist['grid_tilecycle'] = self.grid_tilecycle
                                        self.calc_shed_tiles_reduced_plow()
                                        self.set_total_money_highest_lowest()
                                        self.play_sfx(self.sfx_money)
                                        self.set_tile_imgs_afterbuy(select_row, select_col)
                                    else:
                                        self.play_sfx(self.sfx_denied)

                                elif self.tiles[self.buytile].tiletype == 'Livestock':
                                    if self.silo_tiles_livestock_can[select_row][select_col]:
                                        self.plowingtiles_dict[str(self.plowingtile_counter)] = [self.buytile, select_row, select_col, self.plowingtimer]
                                        self.grid[select_row][select_col] = 'Dirt0'
                                        self.money -= self.tiles[self.buytile].buyupgprice
                                        self.plowingtile_counter += 1
                                        self.grid_tilecycle[select_row][select_col] = 0
                                        self.persist['grid'] = self.grid
                                        self.persist['total_money_spent'] += self.tiles[self.buytile].buyupgprice
                                        self.persist['money'] = self.money
                                        self.persist['plowingtiles_dict'] = self.plowingtiles_dict
                                        self.persist['plowingtile_counter'] = self.plowingtile_counter
                                        self.persist['grid_tilecycle'] = self.grid_tilecycle
                                        self.calc_shed_tiles_reduced_plow()
                                        self.set_total_money_highest_lowest()
                                        self.play_sfx(self.sfx_money)
                                        self.set_tile_imgs_afterbuy(select_row, select_col)
                                    else:
                                        self.play_sfx(self.sfx_denied)

                                elif self.tiles[self.buytile].tiletype == 'Structure':
                                    self.plowingtiles_dict[str(self.plowingtile_counter)] = [self.buytile, select_row, select_col, self.plowingtimer]
                                    self.grid[select_row][select_col] = 'Dirt0'
                                    self.money -= self.tiles[self.buytile].buyupgprice
                                    self.plowingtile_counter += 1
                                    self.grid_tilecycle[select_row][select_col] = 0
                                    self.persist['grid'] = self.grid
                                    self.persist['total_money_spent'] += self.tiles[self.buytile].buyupgprice
                                    self.persist['money'] = self.money
                                    self.persist['plowingtiles_dict'] = self.plowingtiles_dict
                                    self.persist['plowingtile_counter'] = self.plowingtile_counter
                                    self.persist['grid_tilecycle'] = self.grid_tilecycle
                                    self.calc_shed_tiles_reduced_plow()
                                    self.set_total_money_highest_lowest()
                                    if self.tiles[self.buytile].displayname == 'Greenhouse':
                                        self.calc_greenhouse_tiles_season_all()
                                    elif self.tiles[self.buytile].displayname == 'Shed':
                                        self.calc_shed_tiles_reduced_plow()
                                    elif self.tiles[self.buytile].displayname == 'Silo':
                                        self.calc_silo_tiles_livestock_can()
                                    self.play_sfx(self.sfx_money)
                                    self.set_tile_imgs_afterbuy(select_row, select_col)

                            else:
                                self.play_sfx(self.sfx_denied)
                        else:
                            self.play_sfx(self.sfx_denied)

                #Determines which tab of tiles to buy to show on the sidebar
                elif self.sidebar_tilestab_topy < event.pos[1] < self.sidebar_tilestab_topy + self.sidebar_tilestab_h:
                    if self.sidebar_tilestab_leftx1 < event.pos[0] < self.sidebar_tilestab_leftx2:
                        if self.buytile is None and not self.select_sidebar_tilestab1:
                            self.select_sidebar_tilestab1 = True
                            self.sidebar_tilestab1txt_rect = self.sidebar_tilestab1txt.get_rect(topright=(self.sidebar_tilestab_leftx2-2*self.sidebar_highlight_borderthick, self.sidebar_tilestab_topy+self.sidebar_highlight_borderthick-self.sidebar_tilestab_yadjust))
                            self.sidebar_tilestab2txt_rect = self.sidebar_tilestab2txt.get_rect(topright=(self.sidebar_bordergfx_right_topleftx-2*self.sidebar_highlight_borderthick, self.sidebar_tilestab_topy+self.sidebar_highlight_borderthick))
                            self.play_sfx(self.sfx_clicked)
                    elif self.sidebar_tilestab_leftx2+self.bordergfx_h < event.pos[0] < self.sidebar_bordergfx_right_topleftx:
                        if self.buytile is None and self.select_sidebar_tilestab1:
                            self.select_sidebar_tilestab1 = False
                            self.sidebar_tilestab1txt_rect = self.sidebar_tilestab1txt.get_rect(topright=(self.sidebar_tilestab_leftx2-2*self.sidebar_highlight_borderthick, self.sidebar_tilestab_topy+self.sidebar_highlight_borderthick))
                            self.sidebar_tilestab2txt_rect = self.sidebar_tilestab2txt.get_rect(topright=(self.sidebar_bordergfx_right_topleftx-2*self.sidebar_highlight_borderthick, self.sidebar_tilestab_topy+self.sidebar_highlight_borderthick-self.sidebar_tilestab_yadjust))
                            self.play_sfx(self.sfx_clicked)
                    self.persist['select_sidebar_tilestab1'] = self.select_sidebar_tilestab1

                elif self.sidebar_tiles_leftx < event.pos[0] < self.sidebar_tiles_leftx + self.sidebar_tiles_side:
                    if self.buytile is None:

                        #Determines which tile the player has selected to buy from the sidebar
                        #and when to go to the Tile screen for the corresponding tile selected
                        if self.select_sidebar_tilestab1:
                            select_sidebar_tilestab = self.tilestobuya
                        else:
                            select_sidebar_tilestab = self.tilestobuyb
                        for nth_tile, tile in enumerate(select_sidebar_tilestab):
                            lefty = self.sidebar_tiles_topy + nth_tile*self.sidebar_tiles_dist
                            if lefty < event.pos[1] < lefty + self.sidebar_tiles_side:
                                self.persist['buytile'] = tile
                                self.next_state = 'Tile'
                                self.done = True
                                self.play_sfx(self.sfx_clicked)
                                self.save_background_img()

                elif self.buytile is None:
                    self.goto_tutorial(event)
                    self.goto_options(event)
                    self.goto_money(event)

        elif event.type == MOUSEMOTION:
            self.set_highlight()
            self.set_tooltip()

        elif event.type == USEREVENT+2:
            self.play_next_music()

    def update(self, dt):
        self.calc_displaydate()
        self.set_display_total_money()
        self.calc_greenhouse_tiles_season_all()
        self.calc_shed_tiles_reduced_plow()
        self.calc_silo_tiles_livestock_can()
        self.kill_tiles()
        self.set_highlight()
        self.set_tooltip()

    def draw(self, surface):
        #Draw background
        for row in range(1+(self.screen_height/self.background_dirt0_tiles_side)):
            for col in range(1+(self.screen_width/self.background_dirt0_tiles_side)):
                img = pg.transform.scale(self.tiles['Dirt0'].img0, (self.background_dirt0_tiles_side, self.background_dirt0_tiles_side))
                surface.blit(img, (col*self.background_dirt0_tiles_side, row*self.background_dirt0_tiles_side))

        #Draw sidebar tabs of tiles to buy
        if self.select_sidebar_tilestab1:
            for nth_bordergfx in range(1+(self.sidebar_tilestab_w/self.bordergfx_w)):
                surface.blit(self.bordergfx_hor, (self.sidebar_tilestab_leftx2+nth_bordergfx*self.bordergfx_w, self.sidebar_tilestab_topy + self.sidebar_tilestab_h))
        else:
            for nth_bordergfx in range(1+(self.sidebar_tilestab_w/self.bordergfx_w)):
                surface.blit(self.bordergfx_hor, (self.sidebar_tilestab_leftx2-(1+nth_bordergfx)*self.bordergfx_w+self.bordergfx_h, self.sidebar_tilestab_topy + self.sidebar_tilestab_h))
        for nth_bordergfx in range(1+(self.sidebar_tilestab_h/self.bordergfx_w)):
            surface.blit(self.bordergfx_ver, (self.sidebar_tilestab_leftx2, self.sidebar_tilestab_topy + self.sidebar_tilestab_h-(1+nth_bordergfx)*self.bordergfx_w))

        #Draw the player's farm
        for row in range(self.viewablegrid_h+int(self.viewablegrid_h_add)):
            for col in range(self.viewablegrid_w+int(self.viewablegrid_w_add)):
                surface.blit(self.tile_imgs[row][col], (self.sidebar_w+col*self.tile_side-self.viewablegrid_topleft['x']%self.tile_side, row*self.tile_side-self.viewablegrid_topleft['y']%self.tile_side))

        #Draw sidebar tabs of tiles to buy
        if self.select_sidebar_tilestab1:
            select_sidebar_tilestab = self.tilestobuya
        else:
            select_sidebar_tilestab = self.tilestobuyb
        for nth_tile, tile in enumerate(select_sidebar_tilestab):
            img = pg.transform.scale(self.tiles[tile].img0, (self.sidebar_tiles_side, self.sidebar_tiles_side))
            surface.blit(img, (self.sidebar_tiles_leftx, self.sidebar_tiles_topy+nth_tile*self.sidebar_tiles_dist))
            #surface.blit(self.bordergfx_hor, self.sidebar_tiles_topy+nth_tile*self.sidebar_tiles_dist+self.sidebar_tiles_side+)

        #Draw border between tiles in sidebar
        for nth_tile_fence in range(len(select_sidebar_tilestab)-1):
            surface.blit(self.bordergfx_hor, (self.sidebar_w/2-self.bordergfx_w/2, self.sidebar_tiles_topy+(1+nth_tile_fence)*self.sidebar_tiles_dist-self.sidebar_tile_yadjust/2-self.bordergfx_h/2))


        #Draw sidebar horizontal border
        for nth_bordergfx in range(self.sidebar_bordergfx_hor_count):
            surface.blit(self.bordergfx_hor, (self.sidebar_w - (1+nth_bordergfx)*self.bordergfx_w, 0))

        #Draw sidebar vertical borders
        for nth_bordergfx in range(self.sidebar_bordergfx_ver_count):
            surface.blit(self.bordergfx_ver, (self.sidebar_bordergfx_right_topleftx, nth_bordergfx*self.bordergfx_w))
            surface.blit(self.bordergfx_ver, (0, nth_bordergfx*self.bordergfx_w))

        #Draw bottom bar vertical borders
        for nth_bordergfx in range(self.btmbar_bordergfx_ver_count):
            surface.blit(self.bordergfx_ver, (self.displaytotalmoney_rightx+self.bordergfx_h, self.btmbar_toplefty + nth_bordergfx*self.bordergfx_w))
            surface.blit(self.bordergfx_ver, (self.btmbar_bordergfx_right_leftx, self.btmbar_toplefty+nth_bordergfx*self.bordergfx_w))

        #Draw bottom bar top horizontal border
        for nth_bordergfx in range(self.btmbar_bordergfx_hor_count):
            surface.blit(self.bordergfx_hor, (self.btmbar_topleftx+nth_bordergfx*self.bordergfx_w, self.btmbar_toplefty))

        #Draw bottom border
        for nth_bordergfx in range(self.btm_bordergfx_hor_count):
            surface.blit(self.bordergfx_hor, (nth_bordergfx*self.bordergfx_w, self.btm_bordergfx_topy))

        #Draw seasonal art
        if self.current_season == 'Summer':
            surface.blit(self.seasongfx_summer, self.seasongfx_summer_topleft)
        else:
            if self.current_season == 'Autumn':
                seasongfx = self.seasongfx_autumn
            elif self.current_season == 'Winter':
                seasongfx = self.seasongfx_winter
            elif self.current_season == 'Spring':
                seasongfx = self.seasongfx_spring
            for nth_seasongfx in range(self.seasongfx_count):
                surface.blit(seasongfx, (nth_seasongfx*self.seasongfx_w, self.seasongfx_topy))

        #Draw text and options img
        surface.blit(self.sidebar_tilestab1txt, self.sidebar_tilestab1txt_rect)
        surface.blit(self.sidebar_tilestab2txt, self.sidebar_tilestab2txt_rect)
        surface.blit(self.moneytxt, self.moneytxt_rect)
        surface.blit(self.displaydatetxt, self.displaydatetxt_rect)
        surface.blit(self.tutorial_btntxt, self.tutorial_btntxt_rect)
        surface.blit(self.options_btnimg, self.options_btnimg_rect)

        #Draw grid tile highlight
        if self.tile_highlight is not None:
            if self.tile_highlight:
                tile_highlight_c = self.c_blue
            elif not self.tile_highlight:
                tile_highlight_c = self.c_red
            pg.draw.rect(surface, tile_highlight_c, (self.tile_highlight_x, self.tile_highlight_y, self.tile_side, self.tile_side), self.tile_highlight_borderthick)

        #Draw tile to buy highlight
        if self.sidebar_tile_highlight is not None:
            if self.sidebar_tile_highlight:
                sidebar_tile_highlight_c = self.c_blue
            elif not self.sidebar_tile_highlight:
                sidebar_tile_highlight_c = self.c_red
            pg.draw.rect(surface, sidebar_tile_highlight_c, (self.sidebar_tiles_leftx, self.select_sidebar_tiles_topy, self.sidebar_tiles_side, self.sidebar_tiles_side), self.sidebar_highlight_borderthick)

        #Draw tooltip
        if self.tooltipdisplayed:
            pg.draw.rect(surface, self.c_white, (self.tooltip_x, self.tooltip_y, self.tooltipbox_w, self.tooltipbox_h))
            surface.blit(self.tooltip, self.tooltip_rect)
