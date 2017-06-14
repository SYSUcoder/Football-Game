# -*- coding: UTF-8 -*-
import copy
import time
import random

from V2D.Vector2D import *
from misc.utils import *
from V2D.C2DMatrix import C2DMatrix
from Game.BaseGameEntity import BaseGameEntity
from Game.MovingEntity import MovingEntity
from V2D.Transformations import *
from V2D.Geometry import *
from Football.SoccerBall import *
from V2D.Wall2D import *
from Football.TeamStates import *

class AClass:
	def __init__(self, vA):
		self.m_vX = copy.deepcopy(vA)

if __name__ == '__main__':
	oA = Attacking()
	oB = Defending()
	oC = Attacking()
	print type(oA) == type(oC)
