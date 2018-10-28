'''
Backend processing and management of large portions
of data and values to be used in game states
'''

import os
import base64
import pygame as pg

pg.init()

class Cycle(object):
    '''
    Sets the values for the time and season functionality
    '''
    def __init__(self):
        '''
        6 seconds = 1 day
        60 seconds = 10 days

        1 maintenance cycle = 3 seconds = 1 day
        1 earn cycle = 1/2 minute = 10 days
        '''
        self.timecycle = 1000 #milliseconds

        self.day                   = 6 #seconds

        self.maincycle             = self.day/2 #1/2 day
        self.maincycle_crop        = self.day/2
        self.maincycle_livestock   = self.day
        self.maincycle_structure   = self.day*5

        self.earncycle             = self.day*10 #days
        self.earncycle_crop        = self.day*5
        self.earncycle_livestock   = self.day*20

        self.evolvecycle_dirt      = self.day*2
        self.evolvecycle_crop      = self.day*5
        self.evolvecycle_livestock = self.day*3
        self.evolvecycle_structure = self.day*10
        self.evolvecycle           = self.day*7 #days

        self.year_normcycle = 365
        self.year_leapcycle = 366

        #Each month is respective to their number
        self.months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

                          #Month #Name         #No. of days #Season
        self.year_norm = {1:     ['January',   31,          'Summer'],
                          2:     ['February',  28,          'Summer'],
                          3:     ['March',     31,          'Autumn'],
                          4:     ['April',     30,          'Autumn'],
                          5:     ['May',       31,          'Autumn'],
                          6:     ['June',      30,          'Winter'],
                          7:     ['July',      31,          'Winter'],
                          8:     ['August',    31,          'Winter'],
                          9:     ['September', 30,          'Spring'],
                          10:    ['October',   31,          'Spring'],
                          11:    ['November',  30,          'Spring'],
                          12:    ['December',  31,          'Summer']
                         }

        self.year_leap = {1:     ['January',   31,          'Summer'],
                          2:     ['February',  29,          'Summer'],
                          3:     ['March',     31,          'Autumn'],
                          4:     ['April',     30,          'Autumn'],
                          5:     ['May',       31,          'Autumn'],
                          6:     ['June',      30,          'Winter'],
                          7:     ['July',      31,          'Winter'],
                          8:     ['August',    31,          'Winter'],
                          9:     ['September', 30,          'Spring'],
                          10:    ['October',   31,          'Spring'],
                          11:    ['November',  30,          'Spring'],
                          12:    ['December',  31,          'Summer']
                         }

cycle = Cycle()

#Dictionary of every tile's flavor text
flavors = {'Grass0':      ['Go green',
                           ''                      ],
           'Dirt0':       ['What a dirty earth',
                           ''                      ],
           'Field0':      ['A plowed field',
                           'ready for plantng'     ],
           'Construct0':  ['Something\'s being',
                           'built here'            ],
           'Wheat1':      ['Stout wheat',
                           ''                      ],
           'Wheat2':      ['Poor man\'s wheat',
                           ''                      ],
           'Wheat3':      ['Vanguardist wheat',
                           ''                      ],
           'Blueberry1':  ['Blue fruit growing',
                           'from a bush'           ],
           'Blueberry2':  ['Big, blue berries',
                           ''                      ],
           'Blueberry3':  ['Bluey the bush',
                           ''                      ],
           'Carrot1':     ['Vegetables with',
                           'orange roots'          ],
           'Carrot2':     ['Captain Crunch\'s',
                           'Carrots'               ],
           'Carrot3':     ['Feed your inner',
                           'rabiribi desires'      ],
           'Potato1':     ['Brownish blob',
                           'with green leaves'     ],
           'Potato2':     ['What in potarnation',
                           ''                      ],
           'Potato3':     ['Now more powerful by',
                           'an extra half volt'    ],
           'Strawberry1': ['Red fruit growing',
                           'in abundance'          ],
           'Strawberry2': ['Strawberry nice',
                           ''                      ],
           'Strawberry3': ['Plump, juicy, sweet',
                           'and red is best'       ],
           'Chicken1':    ['Cluck cluck cluck',
                           ''                      ],
           'Chicken2':    ['Such fowl, sorcerous',
                           'beasts shan\'t prevail'],
           'Chicken3':    ['Chicks, cocks...all',
                           'the same to me'        ],
           'Pig1':        ['Oink oink oink',
                           ''                      ],
           'Pig2':        ['A creature of',
                           'high intellect'        ],
           'Pig3':        ['Swines make for great',
                           'temporary companions'  ],
           'Greenhouse1': ['Beat up seasons with',
                           'a cold, fiery heart'   ],
           'Greenhouse2': ['A house that\'s meant',
                           'for growing greens'    ],
           'Greenhouse3': ['Why exactly does it',
                           'work outside itself?'  ],
           'Shed1':       ['A shack with tools',
                           'fit for a farmer'      ],
           'Shed2':       ['With newfound wisdom',
                           'comes powerful farming'],
           'Shed3':       ['Was it worth it?',
                           'ecskdee'               ],
           'Silo1':       ['Feed livestock without',
                           'ever going near them'  ],
           'Silo2':       ['Store even more edible,',
                           'tasteless animal food' ],
           'Silo3':       ['Not to be mistaken',
                           'for oil silos'         ],
          }

side = 80

class Tile(object):
    '''
    Sets the member variables of each type of tile
    '''
    def __init__(self, name, displayname, tiletype, season, img0, img1, img2, img3, buyupgprice, sellprice, earnings, maintenance):
        self.name = name
        self.displayname = displayname
        self.tiletype = tiletype
        self.season = season
        self.flavora = flavors[self.name][0]
        self.flavorb = flavors[self.name][1]
        self.img0 = pg.image.load(os.path.join('resources/imgs/tiles', img0)).convert() #middle farme
        self.img1 = pg.image.load(os.path.join('resources/imgs/tiles', img1)).convert() #left frame
        self.img2 = pg.image.load(os.path.join('resources/imgs/tiles', img2)).convert() #middle frame
        self.img3 = pg.image.load(os.path.join('resources/imgs/tiles', img3)).convert() #right frame
        self.buyupgprice = buyupgprice
        self.sellprice = sellprice
        self.earnings = earnings
        self.maintenance = maintenance
        self.side = side


#The types of Tiles
Grass0      = Tile("Grass0",      "Grass",             "None",      "All",    "grass0_0.png",       "grass0_1.png",
                   "grass0_0.png", "grass0_2.png", 0, 0, 0, 0)

Dirt0       = Tile("Dirt0",       "Dirt",              "None",      "All",    "dirt0.png",          "dirt0.png",
                   "dirt0.png", "dirt0.png", 0, 0, 0, 0)

Field0      = Tile("Field0",      "Plowed Field",      "None",      "All",    "field0.png",         "field0.png",
                   "field0.png", "field0.png", 0, 50, 0, 0)

Construct0  = Tile("Construct0",  "Construction Site", "None",      "All",    "construct0.png",     "construct0.png",
                   "construct0.png", "construct0.png", 0, 200, 0, 0)

Wheat1      = Tile("Wheat1",      "Wheat",             "Crop",      "All",    "wheat1_0.png",       "wheat1_1.png",
                   "wheat1_0.png", "wheat1_2.png", 200, 100, 20, 1)

Wheat2      = Tile("Wheat2",      "Wheat",             "Crop",      "All",    "wheat2_0.png",       "wheat2_1.png",
                   "wheat2_0.png", "wheat2_2.png", 100, 125, 40, 2)

Wheat3      = Tile("Wheat3",      "Wheat",             "Crop",      "All",    "wheat3_0.png",       "wheat3_1.png",
                   "wheat3_0.png", "wheat3_2.png", 100, 150, 60, 3)

Blueberry1  = Tile("Blueberry1",  "Blueberry",         "Crop",      "Summer", "blueberry1_0.png",   "blueberry1_1.png",
                   "blueberry1_0.png", "blueberry1_2.png", 300, 100, 25, 1)

Blueberry2  = Tile("Blueberry2",  "Blueberry",         "Crop",      "Summer", "blueberry2_0.png",   "blueberry2_1.png",
                   "blueberry2_0.png", "blueberry2_2.png", 120, 125, 50, 2)

Blueberry3  = Tile("Blueberry3",  "Blueberry",         "Crop",      "Summer", "blueberry2_0.png",   "blueberry2_1.png",
                   "blueberry2_0.png", "blueberry2_2.png", 120, 150, 75, 3)

Carrot1     = Tile("Carrot1",     "Carrot",            "Crop",      "Autumn", "carrot1_0.png",      "carrot1_1.png",
                   "carrot1_0.png", "carrot1_2.png", 300, 100, 25, 1)

Carrot2     = Tile("Carrot2",     "Carrot",            "Crop",      "Autumn", "carrot2_0.png",      "carrot2_1.png",
                   "carrot2_0.png", "carrot2_2.png", 120, 125, 50, 2)

Carrot3     = Tile("Carrot3",     "Carrot",            "Crop",      "Autumn", "carrot3_0.png",      "carrot3_1.png",
                   "carrot3_0.png", "carrot3_2.png", 120, 150, 75, 3)

Potato1     = Tile("Potato1",     "Potato",            "Crop",      "Winter", "potato1_0.png",      "potato1_1.png",
                   "potato1_0.png", "potato1_2.png", 300, 100, 25, 1)

Potato2     = Tile("Potato2",     "Potato",            "Crop",      "Winter", "potato2_0.png",      "potato2_1.png",
                   "potato2_0.png", "potato2_2.png", 120, 125, 50, 2)

Potato3     = Tile("Potato3",     "Potato",            "Crop",      "Winter", "potato3_0.png",      "potato3_1.png",
                   "potato3_0.png", "potato3_2.png", 120, 150, 75, 3)

Strawberry1 = Tile("Strawberry1", "Strawberry",        "Crop",      "Spring", "strawberry1_0.png",  "strawberry1_1.png",
                   "strawberry1_0.png", "strawberry1_2.png", 300, 100, 25, 1)

Strawberry2 = Tile("Strawberry2", "Strawberry",        "Crop",      "Spring", "strawberry2_0.png",  "strawberry2_1.png",
                   "strawberry2_0.png", "strawberry2_2.png", 120, 125, 50, 2)

Strawberry3 = Tile("Strawberry3", "Strawberry",        "Crop",      "Spring", "strawberry3_0.png",  "strawberry3_1.png",
                   "strawberry3_0.png", "strawberry3_2.png", 120, 150, 75, 3)

Chicken1    = Tile("Chicken1",    "Chicken Coop",      "Livestock", "All",    "chickencoop1_0.png", "chickencoop1_1.png",
                   "chickencoop1_2.png", "chickencoop1_3.png", 2000, 500, 300, 15)

Chicken2    = Tile("Chicken2",    "Chicken Coop",      "Livestock", "All",    "chickencoop2_0.png", "chickencoop2_1.png",
                   "chickencoop2_2.png", "chickencoop2_3.png", 1000, 600, 400, 20)

Chicken3    = Tile("Chicken3",    "Chicken Coop",      "Livestock", "All",    "chickencoop3_0.png", "chickencoop3_1.png",
                   "chickencoop3_2.png", "chickencoop3_3.png", 1000, 700, 500, 25)

Pig1        = Tile("Pig1",        "Pig Pen",           "Livestock", "All",    "pigpen1_0.png",      "pigpen1_1.png",
                   "pigpen1_2.png", "pigpen1_3.png", 4000, 1000, 500, 30)

Pig2        = Tile("Pig2",        "Pig Pen",           "Livestock", "All",    "pigpen2_0.png",      "pigpen2_1.png",
                   "pigpen2_2.png", "pigpen2_3.png", 2000, 1250, 650, 38)

Pig3        = Tile("Pig3",        "Pig Pen",           "Livestock", "All",    "pigpen3_0.png",      "pigpen3_1.png",
                   "pigpen3_2.png", "pigpen3_3.png", 2000, 1500, 800, 45)

Greenhouse1 = Tile("Greenhouse1", "Greenhouse",        "Structure", "All",    "greenhouse1_X.png",  "greenhouse1_X.png",
                   "greenhouse1_X.png", "greenhouse1_X.png", 2000, 500, 0, 30)

Greenhouse2 = Tile("Greenhouse2", "Greenhouse",        "Structure", "All",    "greenhouse2_X.png",  "greenhouse2_X.png",
                   "greenhouse2_X.png", "greenhouse2_X.png", 1000, 650, 0, 60)

Greenhouse3 = Tile("Greenhouse3", "Greenhouse",        "Structure", "All",    "greenhouse3_0.png",  "greenhouse3_1.png",
                   "greenhouse3_2.png", "greenhouse3_3.png", 1000, 800, 0, 120)

Shed1       = Tile("Shed1",       "Shed",              "Structure", "All",    "shed1_X.png",        "shed1_X.png",
                   "shed1_X.png", "shed1_X.png", 200, 50, 0, 20)

Shed2       = Tile("Shed2",       "Shed",              "Structure", "All",    "shed2_X.png",        "shed2_X.png",
                   "shed2_X.png", "shed2_X.png", 1000, 250, 0, 100)

Shed3       = Tile("Shed3",       "Shed",              "Structure", "All",    "shed3_0.png",        "shed3_1.png",
                   "shed3_2.png", "shed3_3.png", 10000, 1000, 0, 400)

Silo1       = Tile("Silo1",       "Silo",              "Structure", "All",    "silo1_X.png",        "silo1_X.png",
                   "silo1_X.png", "silo1_X.png", 5000, 1000, 0, 100)

Silo2       = Tile("Silo2",       "Silo",              "Structure", "All",    "silo2_X.png",        "silo2_X.png",
                   "silo2_X.png", "silo2_X.png", 2500, 1500, 0, 150)

Silo3       = Tile("Silo3",       "Silo",              "Structure", "All",    "silo3_X.png",        "silo3_X.png",
                   "silo3_X.png", "silo3_X.png", 2500, 2000, 0, 250)


#Dictionary of every Tile
tiles = {'Grass0':      Grass0,
         'Dirt0':       Dirt0,
         'Field0':      Field0,
         'Construct0':  Construct0,
         'Wheat1':      Wheat1,
         'Wheat2':      Wheat2,
         'Wheat3':      Wheat3,
         'Blueberry1':  Blueberry1,
         'Blueberry2':  Blueberry2,
         'Blueberry3':  Blueberry3,
         'Carrot1':     Carrot1,
         'Carrot2':     Carrot2,
         'Carrot3':     Carrot3,
         'Potato1':     Potato1,
         'Potato2':     Potato2,
         'Potato3':     Potato3,
         'Strawberry1':    Strawberry1,
         'Strawberry2':    Strawberry2,
         'Strawberry3':    Strawberry3,
         'Chicken1':    Chicken1,
         'Chicken2':    Chicken2,
         'Chicken3':    Chicken3,
         'Pig1':        Pig1,
         'Pig2':        Pig2,
         'Pig3':        Pig3,
         'Greenhouse1': Greenhouse1,
         'Greenhouse2': Greenhouse2,
         'Greenhouse3': Greenhouse3,
         'Shed1':       Shed1,
         'Shed2':       Shed2,
         'Shed3':       Shed3,
         'Silo1':       Silo1,
         'Silo2':       Silo2,
         'Silo3':       Silo3
        }

#Tiles to show on tab 1 of the sidebar
tilestobuya = ['Wheat1',
               'Blueberry1',
               'Carrot1',
               'Potato1',
               'Strawberry1'
              ]

#Tiles to show on tab 2 of the sidebar
tilestobuyb = ['Chicken1',
               'Pig1',
               'Greenhouse1',
               'Shed1',
               'Silo1'
              ]


class Structure(object):
    '''
    Sets values for each structure's area of effect
    '''
    def __init__(self, name, radius, lvl3_aoe_upg):
        self.name = name
        self.radius = radius
        self.lvl3_aoe_upg = lvl3_aoe_upg

Structure_Greenhouse1 = Structure('Greenhouse1', 1, 0)
Structure_Greenhouse2 = Structure('Greenhouse2', 2, 0)
Structure_Greenhouse3 = Structure('Greenhouse3', 2, 0.1)
Structure_Shed1       = Structure('Shed1',       1, 0)
Structure_Shed2       = Structure('Shed2',       2, 0)
Structure_Shed3       = Structure('Shed3',       2, 1)
Structure_Silo1       = Structure('Silo1',       1, 0)
Structure_Silo2       = Structure('Silo2',       2, 0)
Structure_Silo3       = Structure('Silo3',       2, 0.1)

#Dictionary of all the structures
structures = {'Greenhouse1': Structure_Greenhouse1,
              'Greenhouse2': Structure_Greenhouse2,
              'Greenhouse3': Structure_Greenhouse3,
              'Shed1':       Structure_Shed1,
              'Shed2':       Structure_Shed2,
              'Shed3':       Structure_Shed3,
              'Silo1':       Structure_Silo1,
              'Silo2':       Structure_Silo2,
              'Silo3':       Structure_Silo3,
             }

#Dictionary of the information about each structure's area of effect
structure_tierupgtxt = {'Greenhouse1': ['In a 1 tile radius,',
                                        'all crops can be grown,',
                                        'no matter the season'],
                        'Greenhouse2': '2 tile radius',
                        'Greenhouse3': ['Crops affected by',
                                        'this earn 5% more and have',
                                        'maintenance cost cut by 5%'],
                        'Shed1':       ['In a 1 tile radius,',
                                        'plowing and construction',
                                        'is faster by 1 stage'],
                        'Shed2':       '2 tile radius',
                        'Shed3':       ['Tile radius effect of',
                                        'non-shed structures affected',
                                        'by this are increased by 1'],
                        'Silo1':       ['In a 1 tile radius,',
                                        'allows livestock to live',
                                        'on the farm'],
                        'Silo2':       '2 tile radius',
                        'Silo3':       ['Livestock affected by',
                                        'this earn 5% more and have',
                                        'maintenance cost cut by 5%']
                       }

'''
Specific detail about structure aoe

greenhouse
    lvl3 --> for crops increase earnings and reduce maintenance by 10%; stacks

shed     -->  removes potential 1 cycle (10 days) from plowing process
              rather than having max 2 cycles (20 days)

    lvl3 --> increase tile radius of nearby structure effects by 1
            affects all nearby structures except other sheds and itself; doesn't stack

silo
    lvl3 --> for crops increase earnings and reduce maintenance by 10%; stacks
'''


#Other images used by the game
bordergfx = pg.image.load(os.path.join('resources/imgs', 'bordergfx.png')).convert()
options_btnimg = pg.image.load(os.path.join('resources/imgs', 'options.png')).convert_alpha()
seasongfx_summer = pg.image.load(os.path.join('resources/imgs', 'summer.png')).convert_alpha()
seasongfx_autumn = pg.image.load(os.path.join('resources/imgs', 'autumn.png')).convert_alpha()
seasongfx_winter = pg.image.load(os.path.join('resources/imgs', 'winter.png')).convert_alpha()
seasongfx_spring = pg.image.load(os.path.join('resources/imgs', 'spring.png')).convert_alpha()

class SFX(object):
    '''
    SFX used by The Harvest
    '''
    def __init__(self, sfxfile):
        self.loadsfx = pg.mixer.Sound(os.path.join('resources/sfx', sfxfile))

class Music(object):
    '''
    Music used by The Harvest
    '''
    def __init__(self, musicfile):
        self.getmusic = os.path.join('resources/music', musicfile)

#SFX
sfx_money = SFX('sfx_money.ogg').loadsfx          #whenever tile bought, sold, removed (w/ money), upgraded
sfx_denied = SFX('sfx_denied.ogg').loadsfx        #whenever action cannot be done
sfx_clicked = SFX('sfx_clicked.ogg').loadsfx      #whever button/pressable things are pressed

#Music
music0 = Music('music0.ogg').getmusic
music1 = Music('music1.ogg').getmusic
music2 = Music('music2.ogg').getmusic
music3 = Music('music3.ogg').getmusic

#Music put into a list
music_list = [music0,
              music1,
              music2,
              music3
             ]

class Load(object):
    '''
    Loads The Harvest's save data, or creates new save data if none is found
    '''
    def __init__(self, savefile, grid_height, grid_width, starting_money):
        self.savefile = os.path.join(savefile)
        self.new_game = not os.path.isfile(self.savefile)

        self.grid = []
        self.grid_tilecycle = []
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.money = starting_money
        self.timer = 0
        self.days_total = 0
        self.days_seasonyear = 0
        self.year = 0
        self.plowingtiles_dict = {}
        self.sfxvol = 1.0
        self.musicvol = 1.0
        self.total_money_earned = 0.0
        self.total_money_spent = 0.0
        self.total_money_highest = starting_money
        self.total_money_lowest = starting_money

    def new_save(self):
        '''
        Creates new save data
        '''
        for row in range(self.grid_height):
            self.grid.append([])
            self.grid_tilecycle.append([])
            for col in range(self.grid_width):
                self.grid[row].append('Grass0')
                self.grid_tilecycle[row].append(0)

    def read_save(self):
        '''
        Reads the encoded savefile
        '''
        with open(self.savefile, 'rb') as encoded_savefile:
            self.encoded_grid = encoded_savefile.readline()
            self.encoded_grid_tilecycle = encoded_savefile.readline()
            self.encoded_money = encoded_savefile.readline()
            self.encoded_timer = encoded_savefile.readline()
            self.encoded_days_total = encoded_savefile.readline()
            self.encoded_days_seasonyear = encoded_savefile.readline()
            self.encoded_year = encoded_savefile.readline()
            self.encoded_plowingtiles_dict_keys = encoded_savefile.readline()
            self.encoded_plowingtiles_dict_values = encoded_savefile.readline()
            self.encoded_sfxvol = encoded_savefile.readline()
            self.encoded_musicvol = encoded_savefile.readline()
            self.encoded_total_money_earned = encoded_savefile.readline()
            self.encoded_total_money_spent = encoded_savefile.readline()
            self.encoded_total_money_highest = encoded_savefile.readline()
            self.encoded_total_money_lowest = encoded_savefile.readline()

    def decode_grid(self, encoded, grid):
        '''
        Decodes the encoded data for the layout of the player's farm
        and other grids that replicate it
        '''
        grid_string = base64.b64decode(encoded)
        grid_list = grid_string.split()
        done = False
        nth_tile = 0
        while not done:
            for row in range(self.grid_height):
                grid.append([])
                for col in range(self.grid_width):
                    try:
                        grid_list[nth_tile] = int(grid_list[nth_tile])
                    except:
                        pass
                    grid[row].append(grid_list[nth_tile])
                    nth_tile += 1
            done = True

    def decode_money(self):
        '''
        Decodes the encoded data for the player's total money
        '''
        self.money = float(base64.b64decode(self.encoded_money))

    def decode_timer(self):
        '''
        Decodes the encoded data for the player's total money
        '''
        self.timer = int(base64.b64decode(self.encoded_timer))

    def decode_days_total(self):
        '''
        Decodes the encoded data for the player's total money
        '''
        self.days_total = int(base64.b64decode(self.encoded_days_total))

    def decode_days_seasonyear(self):
        '''
        Decodes the encoded data for the player's total money
        '''
        self.days_seasonyear = int(base64.b64decode(self.encoded_days_seasonyear))

    def decode_year(self):
        '''
        Decodes the encoded data for the player's total money
        '''
        self.year = int(base64.b64decode(self.encoded_year))


    def decode_plowingtiles_dict(self):
        '''
        Decodes the encoded data for the tiles being plowed
        '''
        plowingtile_keystring = base64.b64decode(self.encoded_plowingtiles_dict_keys)
        plowingtile_valuestring = base64.b64decode(self.encoded_plowingtiles_dict_values)
        if bool(plowingtile_keystring) and bool(plowingtile_valuestring):
            plowingtile_keylist = plowingtile_keystring.split()
            plowingtile_valuelist = plowingtile_valuestring.split()
            len_onekeysvalues = len(plowingtile_valuelist)/len(plowingtile_keylist)
            valueslist = []
            for keyindex in range(1, len(plowingtile_keylist)+1):
                values = []
                for valueindex in range(len_onekeysvalues):
                    if (valueindex+((keyindex-1)*len_onekeysvalues))/len_onekeysvalues == keyindex-1:
                        value = plowingtile_valuelist[valueindex+((keyindex-1)*len_onekeysvalues)]
                        if float(valueindex+((keyindex-1)*len_onekeysvalues))/len_onekeysvalues != float(keyindex-1):
                            value = int(value)
                        values.append(value)
                valueslist.append(values)
            for keyindex, key in enumerate(plowingtile_keylist):
                self.plowingtiles_dict[key] = valueslist[keyindex]

    def decode_sfxvol(self):
        '''
        Decodes the encoded data for sfx volume
        '''
        self.sfxvol = float(base64.b64decode(self.encoded_sfxvol))

    def decode_musicvol(self):
        '''
        Decodes the encoded data for music volume
        '''
        self.musicvol = float(base64.b64decode(self.encoded_musicvol))

    def decode_total_money_earned(self):
        '''
        Decodes the encoded data for the player's total money earned
        '''
        self.total_money_earned = float(base64.b64decode(self.encoded_total_money_earned))

    def decode_total_money_spent(self):
        '''
        Decodes the encoded data for the player's total money spent
        '''
        self.total_money_spent = float(base64.b64decode(self.encoded_total_money_spent))

    def decode_total_money_highest(self):
        '''
        Decodes the encoded data for the player's historically highest total money
        '''
        self.total_money_highest = float(base64.b64decode(self.encoded_total_money_highest))

    def decode_total_money_lowest(self):
        '''
        Decodes the encoded data for the player's historically lowest total money
        '''
        self.total_money_lowest = float(base64.b64decode(self.encoded_total_money_lowest))

    def decode_save(self):
        '''
        Decodes the savefile
        '''
        self.read_save()
        self.decode_grid(self.encoded_grid, self.grid)
        self.decode_grid(self.encoded_grid_tilecycle, self.grid_tilecycle)
        self.decode_money()
        self.decode_timer()
        self.decode_days_total()
        self.decode_days_seasonyear()
        self.decode_year()
        self.decode_plowingtiles_dict()
        self.decode_sfxvol()
        self.decode_musicvol()
        self.decode_total_money_earned()
        self.decode_total_money_spent()
        self.decode_total_money_highest()
        self.decode_total_money_lowest()

    def loadsave(self):
        '''
        Decides if a new save should be created or
        the previous save should be loaded.
        '''
        if self.new_game:
            self.new_save()
        else:
            self.decode_save()

#Paramters for loading a save,
#and also variables to be used in game states
grid_h = 8
grid_w = 14
start_money = 1000.0

load = Load('savefile', grid_h, grid_w, start_money)

load.loadsave()

#Set variables to decoded values
grid = load.grid
grid_tilecycle = load.grid_tilecycle
money= load.money
timer = load.timer
days_total = load.days_total
days_seasonyear = load.days_seasonyear
year = load.year
plowingtiles_dict = load.plowingtiles_dict
sfxvol = load.sfxvol
musicvol = load.musicvol
total_money_earned = load.total_money_earned
total_money_spent = load.total_money_spent
total_money_highest = load.total_money_highest
total_money_lowest = load.total_money_lowest
