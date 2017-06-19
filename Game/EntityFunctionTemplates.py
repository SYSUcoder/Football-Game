# -*- coding: UTF-8 -*-

from Game.BaseGameEntity import *
from V2D.Geometry import *
from V2D.Vector2D import *

def Overlapped(oObj, lContainer, fMinDistBetweenObstacles):
	for oItem in lContainer:
		if TwoCirclesOverlapped(oObj.Pos(), oObj.BRadius() + fMinDistBetweenObstacles,
			                    oItem.Pos(), oItem.BRadius()):
			return True

	return False

def TagNeighbors(oEntity, lOthers, fRadius):
	for oItem in lOthers:
		oItem.UnTag()

		vTo = oItem.Pos().Minus(oEntity.Pos())
		fRange = fRadius + oItem.BRadius()
		# 引用比较 !=
		if oItem != oEntity and vTo.LengthSq() < fRange*fRange:
			oItem.Tag()

def EnforceNonPenetrationContraint(oEntity, lOthers):
	for oItem in lOthers:
		if oItem == oEntity:
			continue

		vToEntity = oEntity.Pos().Minus(oItem.Pos())
		fDistFromEachOther = vToEntity.Length()

		fAmountOfOverLap = oItem.BRadius() + oEntity.BRadius() - fDistFromEachOther

		if fAmountOfOverLap >= 0:
			oEntity.SetPos(oEntity.Pos().Plus(vToEntity.Divide(fDistFromEachOther).Multiply(fAmountOfOverLap) ) )

