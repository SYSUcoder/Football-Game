# -*- coding: UTF-8 -*-

from Football.PlayerBase import *
from Football.SoccerTeam import *
from FSM.StateMachine import *
from Time.Regulator import *
from Data import *
from misc.utils import *
from V2D.Transformations import *
from misc.autolist import *
from Football.FieldPlayerStates import *
from Game.EntityFunctionTemplates import *
from V2D.Vector2D import *

class FieldPlayer(PlayerBase):
	def __init__(self, oHomeTeam, nHomeRegion, oStartState, vHeading, vVelocity,
		         fMass, fMaxForce, fMaxSpeed, fMaxTurnRate, fScale, nRole):
		PlayerBase.__init__(self, oHomeTeam, nHomeRegion, vHeading, vVelocity, fMass,
			       fMaxForce, fMaxSpeed, fMaxTurnRate, fScale, nRole)

		self.m_oStateMachine = StateMachine(self)
		if oStartState:
			self.m_oStateMachine.SetCurrentState(oStartState)
			self.m_oStateMachine.SetPreviousState(oStartState)
			self.m_oStateMachine.SetGlobalState(GlobalPlayerState())

			self.m_oStateMachine.CurrentState().Enter(self)

		self.m_oSteering.SeparationOn()

		self.m_oKickLimiter = Regulator(Params.PLAYERKICKFREQUENCY)

	def Update(self):
		self.m_oStateMachine.Update()
		self.m_oSteering.Calculate()

		if self.m_oSteering.Force().isZero():
			fBrakingRate = 0.8
			self.m_vVelocity = self.m_vVelocity.Multiply(fBrakingRate)

		fTurningForce = self.m_oSteering.SideComponent()
		fTurningForce =  Clamp(fTurningForce, -Params.PLAYERMAXTURNRATE, Params.PLAYERMAXTURNRATE)
		self.m_vHeading = Vec2DRotateAroundOrigin(self.m_vHeading, fTurningForce)
		self.m_vVelocity = self.m_vHeading.Multiply(self.m_vVelocity.Length())
		self.m_vSide = self.m_vHeading.Perp()

		vAccel = self.m_vHeading.Multiply(self.m_oSteering.ForwardComponent() / self.m_fMass)
		self.m_vVelocity = self.m_vVelocity.Plus(vAccel)

		self.m_vVelocity.Truncate(self.m_fMaxSpeed)

		self.m_vPosition = self.m_vPosition.Plus(self.m_vVelocity)

		if Params.BNONPENETRATIONCONSTRAINT:
			EnforceNonPenetrationContraint(self, AutoList.GetAllMembers())

		# debug
		# self.m_vPosition = Vector2D(1, 1)
		print "Player", self.ID(), "Location:", self.Pos().TranslateToTuple()

	def HandleMessage(self, tMsg):
		return self.m_oStateMachine.HandleMessage(tMsg)

	def Render(self):
		return

	def GetFSM(self):
		return self.m_oStateMachine

	def isReadyForNextKick(self):
		return self.m_oKickLimiter.isReady()

