# -*- coding: UTF-8 -*-
from Game.BaseGameEntity import *

class Miner(BaseGameEntity):
	def __init__(self, nID):
		BaseGameEntity.__init__(self, nID)
		self.