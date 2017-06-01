# -*- coding: UTF-8 -*-

from V2D.Vector2D import *
from misc.utils import *
from V2D.C2DMatrix import C2DMatrix
from Game.BaseGameEntity import BaseGameEntity


if __name__ == '__main__':
	eEntity = BaseGameEntity(2)
	eEntity.SetPos(Vector2D(1, 2))
	print eEntity.ID()
	
