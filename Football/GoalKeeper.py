# -*- coding: UTF-8 -*-

import copy
from Football.PlayerBase import *
from Data import *
from FSM.StateMachine import *
from V2D.Vector2D import *
from Game.EntityFunctionTemplates import *
from Football.GoalKeeperStates import *

class GoalKeeper(PlayerBase):
	def __init__(self, oHomeTeam, nHomeRegion, oStartState, vHeading,
		         vVelocity, fMass, fMaxForce, fMaxSpeed, fMaxTurnRate, fScale):
		PlayerBase.__init__(self, oHomeTeam, nHomeRegion, vHeading, vVelocity, fMass,
			       fMaxForce, fMaxSpeed, fMaxTurnRate, fScale, Data.GOAL_KEEPER)

		self.m_oStateMachine = StateMachine(self)
		self.m_oStateMachine.SetCurrentState(oStartState)
		self.m_oStateMachine.SetPreviousState(oStartState)
		self.m_oStateMachine.SetGlobalState(GlobalKeeperState())
		self.m_vLookAt = Vector2D()

		self.m_oStateMachine.CurrentState().Enter(self)

	def Update(self):
		self.m_oStateMachine.Update()
		vSteeringForce = self.m_oSteering.Calculate()

		vAcceleration = vSteeringForce.Divide(self.m_fMass)

		self.m_vVelocity = self.m_vVelocity.Plus(vAcceleration)
		self.m_vVelocity.Truncate(self.m_fMaxSpeed)

		self.m_vPosition = self.m_vPosition.Plus(self.m_vVelocity)

		if Params.BNONPENETRATIONCONSTRAINT:
			EnforceNonPenetrationContraint(self, AutoList.GetAllMembers())

		if not self.m_vVelocity.isZero():
			self.m_vHeading = Vec2DNormalize(self.m_vVelocity)
			self.m_vSide = self.m_vHeading.Perp()

		if not self.Pitch().GoalKeeperHasBall():
			self.m_vLookAt = Vec2DNormalize(self.Ball().Pos().Minus(self.Pos() ) )

	def BallWithinRangeForIntercept(self):
		return Vec2DDistanceSq(self.Team().HomeGoal().Center(), self.Ball().Pos()) <= (
			   Params.GOALKEEPERINTERCEPTRANGE)**2

	def TooFarFromGoalMouth(self):
		return Vec2DDistanceSq(self.Pos(), self.GetRearInterposeTarget()) > (
			   Params.GOALKEEPERINTERCEPTRANGE)**2

	def GetRearInterposeTarget(self):
		fXPosTarget = self.Team().HomeGoal().Center().GetX()
		fYPosTarget = self.Pitch().PlayingArea().Center().GetY() - (
			          Params.GOALWIDTH * 0.5) + self.Ball().Pos().GetY()*Params.GOALWIDTH / (
			          self.Pitch().PlayingArea().Height())

		return Vector2D(fXPosTarget, fYPosTarget)

	def HandleMessage(self, tMsg):
		return self.m_oStateMachine.HandleMessage(tMsg)

	def Render(self):
		return

	def GetFSM(self):
		return self.m_oStateMachine

	def LookAt(self):
		return self.m_vLookAt

	def SetLookAt(self, vVec):
		self.m_vLookAt = copy.deepcopy(vVec)