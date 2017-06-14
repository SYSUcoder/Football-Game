# -*- coding: UTF-8 -*-

import copy
from Game.Region import *
from FSM.StateMachine import *
from Data import *
from Football.TeamStates import *
from Football.SupportSpotCalculator import *
from V2D.Vector2D import *

class SoccerTeam:
	def __init__(self, oHomeGoal, oOpponentsGoal, oPitch, nTeamColor):
		self.m_oOpponentsGoal = copy.deepcopy(oOpponentsGoal)
		self.m_oHomeGoal = copy.deepcopy(oHomeGoal)
		self.m_oOpponents = None
		self.m_oPitch = copy.deepcopy(oPitch)
		self.m_nColor = nTeamColor
		self.m_fDistSqToBallOfClosestPlayer = 0.0
		self.m_oSupportingPlayer = None # PlayerBase暂未实现
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