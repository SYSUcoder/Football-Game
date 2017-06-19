# -*- coding: UTF-8 -*-

import math
from Game.Region import *
from V2D.Vector2D import *
from Data import *
from Time.Regulator import *

class SupportSpot:
	def __init__(self, vPos, fValue):
		self.m_vPos = vPos
		self.m_fScore = fValue

class SupportSpotCalculator:
	def __init__(self, nNumX, nNumY, oTeam):
		self.m_oBestSupportingSpot = None
		self.m_oTeam = oTeam
		self.m_lSpots = []

		oPlayingField = oTeam.Pitch().PlayingArea()
		fHeightOfSSRegion = oPlayingField.Height() * 0.8
		fWidthOfSSRegion = oPlayingField.Width() * 0.9
		fSliceX = fWidthOfSSRegion / nNumX
		fSliceY = fHeightOfSSRegion / nNumY

		fLeft = oPlayingField.Left() + (oPlayingField.Width() - fWidthOfSSRegion) / 2.0 + fSliceX / 2.0
		fRight = oPlayingField.Right() - (oPlayingField.Width() - fWidthOfSSRegion) / 2.0 - fSliceX / 2.0
		fTop = oPlayingField.Top() + (oPlayingField.Height() - fHeightOfSSRegion) / 2.0 + fSliceY / 2.0

		for x in xrange(nNumX / 2 - 1):
			for y in xrange(nNumY):
				if self.m_oTeam.Color() == Data.BLUE:
					self.m_lSpots.append(SupportSpot(Vector2D(fLeft + x*fSliceX, fTop + y*fSliceY), 0.0))
				else:
					self.m_lSpots.append(SupportSpot(Vector2D(fRight - x*fSliceX, fTop + y*fSliceY), 0.0))

		self.m_oRegulator = Regulator(Params.SUPPORTSPOTUPDATEFREQ)

	def DetermineBestSupportingPosition(self):
		if (not self.m_oRegulator.isReady()) and self.m_oBestSupportingSpot:
			return self.m_oBestSupportingSpot.m_vPos

		self.m_oBestSupportingSpot = None
		fBestScoreSoFar = 0.0

		for curSpot in self.m_lSpots:
			curSpot.m_fScore = 1.0
			if self.m_oTeam.isPassSafeFromAllOpponents(self.m_oTeam.ControllingPlayer().Pos(),
				                                       curSpot.m_vPos,
				                                       None,
				                                       Params.MAXPASSINGFORCE):
				curSpot.m_fScore += Params.SPOT_CANPASSSCORE

			if self.m_oTeam.CanShoot(curSpot.m_vPos, Params.MAXSHOOTINGFORCE):
				curSpot.m_fScore += Params.SPOT_CANSCOREFROMPOSITIONSCORE

			if self.m_oTeam.SupportingPlayer():
				fOptimalDistance = 200.0
				fDist = Vec2DDistance(self.m_oTeam.ControllingPlayer().Pos(),
					                  curSpot.m_vPos)
				fTemp = math.fabs(fOptimalDistance - fDist)

				if fTemp < fOptimalDistance:
					curSpot.m_fScore += Params.SPOT_DISTFROMCONTROLLINGPLAYERSCORE * (
						                fOptimalDistance - fTemp) / fOptimalDistance

			if curSpot.m_fScore > fBestScoreSoFar:
				fBestScoreSoFar = curSpot.m_fScore
				self.m_oBestSupportingSpot = curSpot

		return self.m_oBestSupportingSpot.m_vPos

	def GetBestSupportingSpot(self):
		if self.m_oBestSupportingSpot:
			return self.m_oBestSupportingSpot.m_vPos
		else:
			return self.DetermineBestSupportingPosition()

	def Render(self):
		return