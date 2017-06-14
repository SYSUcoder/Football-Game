# -*- coding: UTF-8 -*-

import copy
import math
from V2D.Vector2D import *
from Game.MovingEntity import *

class PlayerBase(MovingEntity):
	def __init__(self, oHomeTeam, nHomeRegion, vHeading, vVelocity,
		         fMass, fMaxForce, fMaxSpeed, fMaxTurnRate, fScale,
		         oRole):
		MovingEntity.__init__(self, oHomeTeam.Pitch().GetRegionFromIndex(nHomeRegion).Center(),
			                  fScale * 10.0,
			                  copy.deepcopy(vVelocity),
			                  fMaxSpeed,
			                  copy.deepcopy(vHeading),
			                  fMass,
			                  Vector2D(fScale, fScale),
			                  fMaxTurnRate,
			                  fMaxForce)
		self.m_oTeam = copy.deepcopy(oHomeTeam)
		self.m_fDistSqToBall = 99999999.0
		self.m_nHomeRegion = nHomeRegion
		self.m_nDefaultRegion = nHomeRegion
		self.m_om_PlayerRole = oRole
		self.m_lVecPlayerVB = []

		lPlayers = [Vector2D(-3,8), Vector2D(3,10), Vector2D(3,-10), Vector2D(-3,-8)]
		for vtx in xrange(len(lPlayers)):
			self.m_lVecPlayerVB.append(lPlayers[vtx])
			if math.abs(lPlayers[vtx].GetX()) > self.BRadius():
				self.SetBRadius(math.abs(lPlayers[vtx].GetX() ) )

			if math.abs(lPlayers[vtx].GetY()) > self.BRadius():
				self.SetBRadius(math.abs(lPlayers[vtx].GetY() ) )

		self.m_oSteering = SteeringBehaviors(self, self.m_oTeam.Pitch(), self.Ball()) # 暂未实现
		self.m_oSteering.SetTarget(oHomeTeam.Pitch().GetRegionFromIndex(nHomeRegion).Center())

	def TrackBall(self):
		self.RotateHeadingToFacePosition(self.Ball().Pos())

	def TrackTarget(self):
		self.SetHeading(Vec2DNormalize(self.Steering().Target().Minus(self.Pos()) ) )

	




	def Team(self):
		return self.m_oTeam

	def Ball(self):
		return self.Team().Pitch().Ball()


def SortByDistanceToOpponentsGoal(oP1, oP2):
	return oP1.DistToOppGoal() < oP2.DistToOppGoal()

def SortByReversedDistanceToOpponentsGoal(oP1, oP2):
	return oP1.DistToOppGoal() > oP2.DistToOppGoal()