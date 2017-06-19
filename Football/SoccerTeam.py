# -*- coding: UTF-8 -*-

import copy
import math
import random
from Game.Region import *
from FSM.StateMachine import *
from Data import *
from Football.TeamStates import *
from Football.SupportSpotCalculator import *
from V2D.Vector2D import *
from V2D.Geometry import *
from V2D.Transformations import *
from misc.utils import *
from Game.EntityManager import *
from Football.GoalKeeper import *
from Football.FieldPlayer import *
from Football.PlayerBase import *

class SoccerTeam:
	def __init__(self, oHomeGoal, oOpponentsGoal, oPitch, nTeamColor):
		self.m_oOpponentsGoal = oOpponentsGoal
		self.m_oHomeGoal = oHomeGoal
		self.m_oOpponents = None
		self.m_oPitch = oPitch
		self.m_nColor = nTeamColor
		self.m_fDistSqToBallOfClosestPlayer = 0.0
		self.m_oSupportingPlayer = None
		self.m_oReceivingPlayer = None
		self.m_oControllingPlayer = None
		self.m_oPlayerClosestToBall = None
		self.m_lPlayers = []

		self.m_oStateMachine = StateMachine(self)
		self.m_oStateMachine.SetCurrentState(Defending())
		self.m_oStateMachine.SetPreviousState(Defending())
		self.m_oStateMachine.SetGlobalState(None)

		self.CreatePlayers()
		for oPlayer in self.m_lPlayers:
			oPlayer.Steering().SeparationOn()

		self.m_oSupportSpotCalc = SupportSpotCalculator(Params.NUMSWEETSPOTSX,
														Params.NUMSWEETSPOTSY,
														self)

	def Update(self):
		self.CalculateClosestPlayerToBall()
		self.m_oStateMachine.Update()
		for oPlayer in self.m_lPlayers:
			oPlayer.Update()

	def CalculateClosestPlayerToBall(self):
		fClosestSoFar = 99999999.0
		for oPlayer in self.m_lPlayers:
			fDist = Vec2DDistanceSq(oPlayer.Pos(), self.Pitch().Ball().Pos())
			oPlayer.SetDistSqToBall(fDist)
			if fDist < fClosestSoFar:
				fClosestSoFar = fDist
				self.m_oPlayerClosestToBall = oPlayer

		self.m_fDistSqToBallOfClosestPlayer = fClosestSoFar

	def DetermineBestSupportingAttacker(self):
		fClosestSoFar = 99999999.0
		oBestPlayer = None
		for oPlayer in self.m_lPlayers:
			# 用!=判断必须保证id相等，也就是同一引用
			if oPlayer.Role() == Data.ATTACKER and oPlayer != self.m_oControllingPlayer:
				fDist = Vec2DDistanceSq(oPlayer.Pos(), self.m_oSupportSpotCalc.GetBestSupportingSpot())

				if fDist < fClosestSoFar:
					fClosestSoFar = fDist
					oBestPlayer = oPlayer

		return oBestPlayer

	def FindPass(self, oPasser, oReceiver, vPassTarget, fPower, fMinPassingDistance):
		fClosestToGoalSoFar = 99999999.0
		vTarget = Vector2D()

		for curPlyr in self.Members():
			if curPlyr != oPasser and Vec2DDistanceSq(oPasser.Pos(), curPlyr.Pos()) > fMinPassingDistance**2:
				if self.GetBestPassToReceiver(oPasser, curPlyr, vTarget, fPower):
					fDist2Goal = math.fabs(vTarget.GetX() - self.OpponentsGoal().Center().GetX())
					if fDist2Goal < fClosestToGoalSoFar:
						fClosestToGoalSoFar = fDist2Goal
						oReceiver = curPlyr
						vPassTarget = vTarget # 传引用

		if oReceiver:
			return True
		else:
			return False

	def GetBestPassToReceiver(self, oPasser, oReceiver, vPassTarget, fPower):
		fTime = self.Pitch().Ball().TimeToCoverDistance(Pitch().Ball().Pos(),
			                                            oReceiver.Pos(),
			                                            fPower)
		if fTime < 0:
			return False
		fInterceptRange = fTime * oReceiver.MaxSpeed()
		fScalingFactor = 0.3
		fInterceptRange *= fScalingFactor

		vIp1 = Vector2D()
		vIp2 = Vector2D()
		GetTangentPoints(oReceiver.Pos(), fInterceptRange, Pitch().Ball().Pos(), vIp1, vIp2)
		
		nNumPassesToTry = 3
		lPasses = [vIp1, oReceiver.Pos(), vIp2]

		fClosestSoFar = 99999999.0
		bResult = False
		for nPass in xrange(nNumPassesToTry):
			fDist = math.fabs(lPasses[nPass].GetX() - self.OpponentsGoal().Center().GetX())

			if fDist < fClosestSoFar and self.Pitch().PlayingArea().Inside(lPasses[nPass]) and (
			   isPassSafeFromAllOpponents(self.Pitch().Ball().Pos(), lPasses[nPass], oReceiver, fPower)):
				fClosestSoFar = fDist
				vPassTarget = lPasses[nPass]
				bResult = True

		return bResult

	def isPassSafeFromOpponent(self, vFrom, vTarget, oReceiver, oOpp, fPassingForce):
		vToTarget = vTarget.Minus(vFrom)
		vToTargetNormalized = Vec2DNormalize(vToTarget)

		vLocalPosOpp = PointToLocalSpace(oOpp.Pos(), vToTargetNormalized,
			                             vToTargetNormalized.Perp(), vFrom)
		if vLocalPosOpp.GetX() < 0:
			return True

		if Vec2DDistanceSq(vFrom, vTarget) < Vec2DDistanceSq(oOpp.Pos(), vFrom):
			if oReceiver:
				if Vec2DDistanceSq(vTarget, oOpp.Pos()) > Vec2DDistanceSq(vTarget, oReceiver.Pos()):
					return True
				else:
					return False
			else:
				return True

		fTimeForBall = self.Pitch().Ball().TimeToCoverDistance(Vector2D(0, 0),
			                                                   Vector2D(vLocalPosOpp.GetX(), 0),
			                                                   fPassingForce)
		fReach = oOpp.MaxSpeed() * fTimeForBall + self.Pitch().Ball().BRadius() + oOpp.BRadius()
		if math.fabs(vLocalPosOpp.GetY() < fReach):
			return False
		return True

	def isPassSafeFromAllOpponents(self, vFrom, vTarget, oReceiver, fPassingForce):
		for opp in self.Opponents().Members():
			if not self.isPassSafeFromOpponent(vFrom, vTarget, oReceiver, opp, fPassingForce):
				return False

		return True

	def CanShoot(self, vBallPos, fPower, vShotTarget):
		nNumAttempts = Params.NUMATTEMPTSTOFINDVALIDSTRIKE
		for i in xrange(nNumAttempts):
			vShotTarget = self.OpponentsGoal().Center()
			nMinYVal = self.OpponentsGoal().LeftPost().GetY() + self.Pitch().Ball().BRadius()
			nMaxYVal = self.OpponentsGoal().RightPost().GetY() - self.Pitch().Ball().BRadius()

			vShotTarget.SetY(float(RandInt(nMinYVal, nMaxYVal)))

			fTime = self.Pitch().Ball().TimeToCoverDistance(vBallPos, vShotTarget, fPower)

			if fTime >= 0:
				if self.isPassSafeFromAllOpponents(vBallPos, vShotTarget, None, fPower):
					return True

		return False

	def ReturnAllFieldPlayersToHome(self):
		for oPlayer in self.m_lPlayers:
			if oPlayer.Role() !=  Data.GOAL_KEEPER:
				MessageDispatcher().DispatchMsg(MessageData.SEND_MSG_IMMEDIATELY,
					                            1,
					                            oPlayer.ID(),
					                            MessageData.MSG_GOHOME,
					                            None)

	def Render(self):
		return

	def CreatePlayers(self):
		if self.Color() == Data.BLUE:
			self.m_lPlayers.append(GoalKeeper(self, 1, TendGoal(), Vector2D(0, 1),
				                              Vector2D(0.0, 0.0), Params.PLAYERMASS,
				                              Params.PLAYERMAXFORCE, Params.PLAYERMAXSPEEDWITHOUTBALL,
				                              Params.PLAYERMAXTURNRATE, Params.PLAYERSCALE))

			self.m_lPlayers.append(FieldPlayer(self, 6, Wait(), Vector2D(0,1),
				                               Vector2D(0.0, 0.0), Params.PLAYERMASS,
				                               Params.PLAYERMAXFORCE, Params.PLAYERMAXSPEEDWITHOUTBALL,
				                               Params.PLAYERMAXTURNRATE, Params.PLAYERSCALE,
				                               Data.ATTACKER))

			self.m_lPlayers.append(FieldPlayer(self, 8, Wait(), Vector2D(0,1),
				                               Vector2D(0.0, 0.0), Params.PLAYERMASS,
				                               Params.PLAYERMAXFORCE, Params.PLAYERMAXSPEEDWITHOUTBALL,
				                               Params.PLAYERMAXTURNRATE, Params.PLAYERSCALE,
				                               Data.ATTACKER))

			self.m_lPlayers.append(FieldPlayer(self, 3, Wait(), Vector2D(0,1),
				                               Vector2D(0.0, 0.0), Params.PLAYERMASS,
				                               Params.PLAYERMAXFORCE, Params.PLAYERMAXSPEEDWITHOUTBALL,
				                               Params.PLAYERMAXTURNRATE, Params.PLAYERSCALE,
				                               Data.DEFENDER))

			self.m_lPlayers.append(FieldPlayer(self, 5, Wait(), Vector2D(0,1),
				                               Vector2D(0.0, 0.0), Params.PLAYERMASS,
				                               Params.PLAYERMAXFORCE, Params.PLAYERMAXSPEEDWITHOUTBALL,
				                               Params.PLAYERMAXTURNRATE, Params.PLAYERSCALE,
				                               Data.DEFENDER))

		else:
			self.m_lPlayers.append(GoalKeeper(self, 16, TendGoal(), Vector2D(0, -1),
				                              Vector2D(0.0, 0.0), Params.PLAYERMASS,
				                              Params.PLAYERMAXFORCE, Params.PLAYERMAXSPEEDWITHOUTBALL,
				                              Params.PLAYERMAXTURNRATE, Params.PLAYERSCALE))

			self.m_lPlayers.append(FieldPlayer(self, 9, Wait(), Vector2D(0,-1),
				                               Vector2D(0.0, 0.0), Params.PLAYERMASS,
				                               Params.PLAYERMAXFORCE, Params.PLAYERMAXSPEEDWITHOUTBALL,
				                               Params.PLAYERMAXTURNRATE, Params.PLAYERSCALE,
				                               Data.ATTACKER))

			self.m_lPlayers.append(FieldPlayer(self, 11, Wait(), Vector2D(0,-1),
				                               Vector2D(0.0, 0.0), Params.PLAYERMASS,
				                               Params.PLAYERMAXFORCE, Params.PLAYERMAXSPEEDWITHOUTBALL,
				                               Params.PLAYERMAXTURNRATE, Params.PLAYERSCALE,
				                               Data.ATTACKER))

			self.m_lPlayers.append(FieldPlayer(self, 12, Wait(), Vector2D(0,-1),
				                               Vector2D(0.0, 0.0), Params.PLAYERMASS,
				                               Params.PLAYERMAXFORCE, Params.PLAYERMAXSPEEDWITHOUTBALL,
				                               Params.PLAYERMAXTURNRATE, Params.PLAYERSCALE,
				                               Data.DEFENDER))

			self.m_lPlayers.append(FieldPlayer(self, 14, Wait(), Vector2D(0,-1),
				                               Vector2D(0.0, 0.0), Params.PLAYERMASS,
				                               Params.PLAYERMAXFORCE, Params.PLAYERMAXSPEEDWITHOUTBALL,
				                               Params.PLAYERMAXTURNRATE, Params.PLAYERSCALE,
				                               Data.DEFENDER))

		for oPlayer in self.m_lPlayers:
			EntityManager().RegisterEntity(oPlayer)

	def GetPlayerFromID(self, nID):
		for oPlayer in self.m_lPlayers:
			if oPlayer.ID() == nID:
				return oPlayer
		return None

	def SetPlayerHomeRegion(self, nPlyr, nRegion):
		if not (nPlyr >= 0 and nPlyr < len(self.m_lPlayers)):
			print "player index wrong!\n"
			return
		self.m_lPlayers[nPlyr].SetHomeRegion(nRegion)

	def UpdateTargetsOfWaitingPlayers(self):
		for oPlayer in self.m_lPlayers:
			if oPlayer.Role() != Data.GOAL_KEEPER:
				if (oPlayer.GetFSM().isInState(Wait()) ) or (
					oPlayer.GetFSM().isInState(ReturnToHomeRegion()) ):
					oPlayer.Steering().SetTarget(oPlayer.HomeRegion().Center())

	def AllPlayersAtHome(self):
		for oPlayer in self.m_lPlayers:
			if oPlayer.InHomeRegion() == False:
				return False

		return True

	def RequestPass(self, oRequester):
		random.seed()
		if random.random() > 0.1:
			return

		if self.isPassSafeFromAllOpponents(self.ControllingPlayer().Pos(),
			                               oRequester.Pos(),
			                               oRequester,
			                               Params.MAXPASSINGFORCE):
			MessageDispatcher().DispatchMsg(MessageData.SEND_MSG_IMMEDIATELY,
				                            oRequester.ID(),
				                            self.ControllingPlayer().ID(),
				                            MessageData.MSG_PASSTOME,
				                            oRequester)

	def isOpponentWithinRadius(self, vPos, fRad):
		for oMember in self.Opponents().Members():
			if Vec2DDistanceSq(vPos, oMember.Pos()) < fRad**2:
				return True

		return False

	def Members(self):
		return self.m_lPlayers

	def GetFSM(self):
		return self.m_oStateMachine

	def HomeGoal(self):
		return self.m_oHomeGoal

	def OpponentsGoal(self):
		return self.m_oOpponentsGoal

	def Pitch(self):
		return self.m_oPitch

	def Opponents(self):
		return self.m_oOpponents

	def SetOpponents(self, oOpps):
		# 源码为存指针，所以存引用
		self.m_oOpponents = oOpps

	def Color(self):
		return self.m_nColor

	def SetPlayerClosestToBall(self, oPlayer):
		# PlayerBase*
		self.m_oPlayerClosestToBall = oPlayer

	def PlayerClosestToBall(self):
		return self.m_oPlayerClosestToBall

	def ClosestDistToBallSq(self):
		return self.m_fDistSqToBallOfClosestPlayer

	def GetSupportSpot(self):
		return self.m_oSupportSpotCalc.GetBestSupportingSpot()

	def SupportingPlayer(self):
		return self.m_oSupportingPlayer

	def SetSupportingPlayer(self, oPlayer):
		self.m_oSupportingPlayer = oPlayer

	def Receiver(self):
		return self.m_oReceivingPlayer

	def SetReceiver(self, oPlayer):
		self.m_oReceivingPlayer = oPlayer

	def ControllingPlayer(self):
		return self.m_oControllingPlayer

	def SetControllingPlayer(self, oPlayer):
		self.m_oControllingPlayer = oPlayer
		self.Opponents().LostControl()

	def InControl(self):
		if self.m_oControllingPlayer:
			return True
		else:
			return False

	def LostControl(self):
		self.m_oControllingPlayer = None

	def DetermineBestSupportingPosition(self):
		self.m_oSupportSpotCalc.DetermineBestSupportingPosition()

	def Name(self):
		if self.m_nColor == Data.BLUE:
			return "Blue"
		else:
			return "Red"
