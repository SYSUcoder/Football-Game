# -*- coding: UTF-8 -*-

import copy
import math
from V2D.Vector2D import *
from Game.MovingEntity import *
from misc.autolist import *
from Data import *
from Messaging.MessageDispatcher import *
from Football.SteeringBehaviors import *
from Football.SoccerBall import *
from Football.SoccerTeam import *
from Football.SoccerPitch import *

class PlayerBase(MovingEntity, AutoList):
	def __init__(self, oHomeTeam, nHomeRegion, vHeading, vVelocity,
		         fMass, fMaxForce, fMaxSpeed, fMaxTurnRate, fScale,
		         nRole):
		MovingEntity.__init__(self, oHomeTeam.Pitch().GetRegionFromIndex(nHomeRegion).Center(),
			                  fScale * 10.0,
			                  copy.deepcopy(vVelocity),
			                  fMaxSpeed,
			                  copy.deepcopy(vHeading),
			                  fMass,
			                  Vector2D(fScale, fScale),
			                  fMaxTurnRate,
			                  fMaxForce)
		AutoList.__init__(self)
		
		self.m_oTeam = oHomeTeam
		self.m_fDistSqToBall = 99999999.0
		self.m_nHomeRegion = nHomeRegion
		self.m_nDefaultRegion = nHomeRegion
		self.m_nPlayerRole = nRole
		self.m_lVecPlayerVB = []

		lPlayers = [Vector2D(-3,8), Vector2D(3,10), Vector2D(3,-10), Vector2D(-3,-8)]
		for vtx in xrange(len(lPlayers)):
			self.m_lVecPlayerVB.append(lPlayers[vtx])
			if abs(lPlayers[vtx].GetX()) > self.BRadius():
				self.SetBRadius(math.abs(lPlayers[vtx].GetX() ) )

			if abs(lPlayers[vtx].GetY()) > self.BRadius():
				self.SetBRadius(math.abs(lPlayers[vtx].GetY() ) )

		self.m_oSteering = SteeringBehaviors(self, self.m_oTeam.Pitch(), self.Ball())
		self.m_oSteering.SetTarget(oHomeTeam.Pitch().GetRegionFromIndex(nHomeRegion).Center())

	def TrackBall(self):
		self.RotateHeadingToFacePosition(self.Ball().Pos())

	def TrackTarget(self):
		self.SetHeading(Vec2DNormalize(self.Steering().Target().Minus(self.Pos()) ) )

	def PositionInFrontOfPlayer(self, vPosition):
		vToSubject = vPosition.Minus(self.Pos())

		if vToSubject.Dot(self.Heading()) > 0:
			return True
		else:
			return False

	def isThreatened(self):
		for oCurOpp in self.Team().Opponents().Members():
			if self.PositionInFrontOfPlayer(oCurOpp.Pos() and (
				                            Vec2DDistanceSq(self.Pos(), oCurOpp.Pos())
				                            < Params.PLAYERCOMFORTZONE**2) ):
				return True

		return False

	def FindSupport(self):
		if self.Team().SupportingPlayer() == None:
			oBestSupportPly = self.Team().DetermineBestSupportingAttacker()
			self.Team().SetSupportingPlayer(oBestSupportPly)
			MessageDispatcher().DispatchMsg(MessageData.SEND_MSG_IMMEDIATELY,
				                            self.ID(),
				                            self.Team().SupportingPlayer().ID(),
				                            MessageData.MSG_SUPPORTATTACKER,
				                            None)

		oBestSupportPly = self.Team().DetermineBestSupportingAttacker()

		if oBestSupportPly and oBestSupportPly != self.Team().SupportingPlayer():
			if self.Team().SupportingPlayer():
				MessageDispatcher().DispatchMsg(MessageData.SEND_MSG_IMMEDIATELY,
					                            self.ID(),
				                                self.Team().SupportingPlayer().ID(),
				                                MessageData.MSG_GOHOME,
				                                None)

			self.Team().SetSupportingPlayer(oBestSupportPly)

			MessageDispatcher().DispatchMsg(MessageData.SEND_MSG_IMMEDIATELY,
					                        self.ID(),
				                            self.Team().SupportingPlayer().ID(),
				                            MessageData.MSG_SUPPORTATTACKER,
				                            None)

	def DistToOppGoal(self):
		return math.fabs(self.Pos().GetX() - self.Team().OpponentsGoal().Center().GetX())

	def DistToHomeGoal(self):
		return math.fabs(self.Pos().GetX() - self.Team().HomeGoal().Center().GetX())

	def isControllingPlayer(self):
		# 返回引用，估计有bug
		return self.Team().ControllingPlayer() == self

	def BallWithinKeeperRange(self):
		return Vec2DDistanceSq(self.Pos(), self.Ball().Pos()) < Params.KEEPERINBALLRANGE**2

	def BallWithinReceivingRange(self):
		return Vec2DDistanceSq(self.Pos(), self.Ball().Pos()) < Params.BALLWITHINRECEIVINGRANGE**2

	def BallWithinKickingRange(self):
		return Vec2DDistanceSq(self.Ball().Pos(), self.Pos()) < Params.PLAYERKICKINGDISTANCE**2

	def InHomeRegion(self):
		if self.m_nPlayerRole == Data.GOAL_KEEPER:
			return self.Pitch().GetRegionFromIndex(self.m_nHomeRegion).Inside(self.Pos(), RegionData.NORMAL)
		else:
			return self.Pitch().GetRegionFromIndex(self.m_nHomeRegion).Inside(self.Pos(), RegionData.HALFSIZE)

	def AtTarget(self):
		return Vec2DDistanceSq(self.Pos(), self.Steering().Target()) < Params.PLAYERINTARGETRANGE**2

	def isClosestTeamMemberToBall(self):
		return self.Team().PlayerClosestToBall() == self

	def isClosestPlayerOnPitchToBall(self):
		return self.isClosestTeamMemberToBall() and (
			   self.DistSqToBall() < self.Team().Opponents().ClosestDistToBallSq())

	def InHotRegion(self):
		return math.fabs(self.Pos().GetY() - self.Team().OpponentsGoal().Center().GetY()) < (
			   self.Pitch().PlayingArea().Length() / 3.0)

	def isAheadOfAttacker(self):
		return math.fabs(self.Pos().GetX() - self.Team().OpponentsGoal().Center().GetX()) < (
			   math.fabs(self.Team().ControllingPlayer().Pos().GetX() - self.Team().OpponentsGoal().Center().GetX()))

	def Ball(self):
		return self.Team().Pitch().Ball()

	def Pitch(self):
		return self.Team().Pitch()

	def HomeRegion(self):
		return self.Pitch().GetRegionFromIndex(self.m_nHomeRegion)

	def Role(self):
		return self.m_nPlayerRole

	def DistSqToBall(self):
		return self.m_fDistSqToBall

	def SetDistSqToBall(self, vVal):
		self.m_fDistSqToBall = vVal

	def SetDefaultHomeRegion(self):
		self.m_nHomeRegion = self.m_nDefaultRegion

	def Steering(self):
		return self.m_oSteering

	def SetHomeRegion(self, nNewRegion):
		self.m_nHomeRegion = nNewRegion

	def Team(self):
		return self.m_oTeam


def SortByDistanceToOpponentsGoal(oP1, oP2):
	return oP1.DistToOppGoal() < oP2.DistToOppGoal()

def SortByReversedDistanceToOpponentsGoal(oP1, oP2):
	return oP1.DistToOppGoal() > oP2.DistToOppGoal()
