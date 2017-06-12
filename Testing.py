# -*- coding: UTF-8 -*-
import copy

from V2D.Vector2D import *
from misc.utils import *
from V2D.C2DMatrix import C2DMatrix
from Game.BaseGameEntity import BaseGameEntity
from Game.MovingEntity import MovingEntity
from V2D.Transformations import *
from V2D.Geometry import *


def test(lList): whisker
	lList1 = copy.copy(lList)
	lList1[0] = 1
	return lList1

if __name__ == '__main__':
	eEntity = MovingEntity(Vector2D(1,1), 1.0, Vector2D(3, 4), 6.0, Vector2D(2, 1), 10.0, Vector2D(1, 1), 0.3, 1.0)
	
	lList = [0, 1, 2, 3]
	lList1 = test(lList)
	print lList
	print lList1