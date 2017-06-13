# -*- coding: UTF-8 -*-
import copy

from V2D.Vector2D import *
from misc.utils import *
from V2D.C2DMatrix import C2DMatrix
from Game.BaseGameEntity import BaseGameEntity
from Game.MovingEntity import MovingEntity
from V2D.Transformations import *
from V2D.Geometry import *
from Football.SoccerBall import *
from V2D.Wall2D import *



if __name__ == '__main__':
	m_lRegions = [None] * (Data.NUMREGIONSHORIZONTAL * Data.NUMREGIONSVERTICAL)
	print len(m_lRegions)