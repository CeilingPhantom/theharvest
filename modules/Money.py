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

	def startup(self, persistent):

		self.persist = persistent

		self.earnings = self.persist['']
		#self.earningstxt = self.font_body2.render('Earnings: '+str(self.))

		self.background_img = pg.image.load(os.path.join('resources/temp', 'background.png')).convert()

	def get_event(self, event):
		pass

	def draw(self, surface):
		pass