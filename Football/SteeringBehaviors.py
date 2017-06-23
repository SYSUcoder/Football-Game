# -*- coding: UTF-8 -*-

import copy
from V2D.Vector2D import *
from Data import *
from misc.autolist import *

class SteeringBehaviors:
	def __init__(self, oAgent, oWorld, oBall):
		self.m_oPlayer = oAgent
		self.m_nFlags = 0
		self.m_fMultSeparation = Params.SEPARATIONCOEFFICIENT
		self.m_bTagged = False
		self.m_fViewDistance = Params.VIEWDISTANCE
		self.m_oBall = oBall
		self.m_fInterposeDist = 0.0
		self.m_lAntenna = [Vector2D()] * 5
		self.m_vSteeringForce = Vector2D()

	def AccumulateForce(self, vSf, vForceToAdd):
		fMagnitudeSoFar = vSf.Length()
		fMagnitudeRemaining = self.m_oPlayer.MaxForce() - fMagnitudeSoFar

		if fMagnitudeRemaining <= 0.0:
			return Vector2D(0, 0)

		fMagnitudeToAdd = vForceToAdd.Length()

		if fMagnitudeToAdd > fMagnitudeRemaining:
			fMagnitudeToAdd = fMagnitudeRemaining

		vSf = vSf.Plus(Vec2DNormalize(vForceToAdd).Multiply(fMagnitudeToAdd) )
		return vSf

	def Calculate(self):
		self.m_vSteeringForce.Zero()
		self.m_vSteeringForce = self.SumForces()

		self.m_vSteeringForce.Truncate(self.m_oPlayer.MaxForce())
		
		return self.m_vSteeringForce

	def SumForces(self):
		vForce = Vector2D()

		self.FindNeighbours()

		if self.On(BehaviorType.SEPARATION):
			# print "Player", self.m_oPlayer.ID(), "is execute Separation()"
			vForce = vForce.Plus(self.Separation().Multiply(self.m_fMultSeparation) )
			self.m_vSteeringForce = self.AccumulateForce(self.m_vSteeringForce, vForce)
			if not self.m_vSteeringForce:
				return self.m_vSteeringForce

		if self.On(BehaviorType.SEEK):
			# print "Player", self.m_oPlayer.ID(), "is execute Seek()"
			vForce = vForce.Plus(self.Seek(self.m_vTarget))
			self.m_vSteeringForce = self.AccumulateForce(self.m_vSteeringForce, vForce)
			if not self.m_vSteeringForce:
				return self.m_vSteeringForce

		if self.On(BehaviorType.ARRIVE):
			# print "Player", self.m_oPlayer.ID(), "is execute Arrive()"
			vForce = vForce.Plus(self.Arrive(self.m_vTarget, Data.FAST))
			self.m_vSteeringForce = self.AccumulateForce(self.m_vSteeringForce, vForce)
			if not self.m_vSteeringForce:
				return self.m_vSteeringForce

		if self.On(BehaviorType.PURSUIT):
			# print "Player", self.m_oPlayer.ID(), "is execute Pursuit()"
			vForce = vForce.Plus(self.Pursuit(self.m_oBall))
			self.m_vSteeringForce = self.AccumulateForce(self.m_vSteeringForce, vForce)
			if not self.m_vSteeringForce:
				return self.m_vSteeringForce

		if self.On(BehaviorType.INTERPOSE):
			# print "Player", self.m_oPlayer.ID(), "is execute Interpose()"
			vForce = vForce.Plus(self.Interpose(self.m_oBall, self.m_vTarget, self.m_fInterposeDist))
			self.m_vSteeringForce = self.AccumulateForce(self.m_vSteeringForce, vForce)
			if not self.m_vSteeringForce:
				return self.m_vSteeringForce

		return self.m_vSteeringForce

	def ForwardComponent(self):
		return self.m_oPlayer.Heading().Dot(self.m_vSteeringForce)

	def SideComponent(self):
		return self.m_oPlayer.Side().Dot(self.m_vSteeringForce) * self.m_oPlayer.MaxTurnRate()

	def Seek(self, vTarget):
		vDesiredVelocity = Vec2DNormalize(vTarget.Minus(self.m_oPlayer.Pos())).Multiply(self.m_oPlayer.MaxSpeed())

		return vDesiredVelocity.Minus(self.m_oPlayer.Velocity())

	def Arrive(self, vTarget, nDeceleration):
		vToTarget = vTarget.Minus(self.m_oPlayer.Pos())

		fDist = vToTarget.Length()

		if fDist > 0:
			fDecelerationTweaker = 0.3

			fSpeed = fDist / (float(nDeceleration) * fDecelerationTweaker)
			fSpeed = min(fSpeed, self.m_oPlayer.MaxSpeed())

			vDesiredVelocity = vToTarget.Multiply(fSpeed / fDist)

			return vDesiredVelocity.Minus(self.m_oPlayer.Velocity())

		return Vector2D(0, 0)

	def Pursuit(self, oBall):
		vToBall = oBall.Pos().Minus(self.m_oPlayer.Pos())

		fLookAheadTime = 0.0

		if oBall.Speed() != 0.0:
			fLookAheadTime = vToBall.Length() / oBall.Speed()

		self.m_vTarget = oBall.FuturePosition(fLookAheadTime)

		return self.Arrive(self.m_vTarget, Data.FAST)

	def FindNeighbours(self):
		lAllPlayers = AutoList.GetAllMembers()

		for oCurPlyr in lAllPlayers:
			oCurPlyr.Steering().UnTag()

			vTo = oCurPlyr.Pos().Minus(self.m_oPlayer.Pos())

			if vTo.LengthSq() < self.m_fViewDistance**2:
				oCurPlyr.Steering().Tag()

	def Separation(self):
		vSteeringForce = Vector2D()

		lAllPlayers = AutoList.GetAllMembers()
		for oCurPlyr in lAllPlayers:
			if oCurPlyr != self.m_oPlayer and oCurPlyr.Steering().Tagged():
				vToAgent = self.m_oPlayer.Pos().Minus(oCurPlyr.Pos())

				vSteeringForce = vSteeringForce.Plus(Vec2DNormalize(vToAgent).Divide(vToAgent.Length()))

		return vSteeringForce

	def Interpose(self, oBall, vTarget, fDistFromTarget):
		return self.Arrive(vTarget.Plus(Vec2DNormalize(oBall.Pos().Minus(vTarget)).Multiply(fDistFromTarget)),
			               Data.NORMAL)

	def RenderAids(self):
		return

	def On(self, nBt):
		return (self.m_nFlags & nBt) == nBt

	def Force(self):
		return self.m_vSteeringForce

	def Target(self):
		return self.m_vTarget

	def SetTarget(self, vT):
		self.m_vTarget = copy.deepcopy(vT)

	def InterposeDistance(self):
		return self.m_fInterposeDist

	def SetInterposeDistance(self, fD):
		self.m_fInterposeDist = fD

	def Tagged(self):
		return self.m_bTagged

	def Tag(self):
		self.m_bTagged = True

	def UnTag(self):
		self.m_bTagged = False

	def SeekOn(self):
		self.m_nFlags = self.m_nFlags | BehaviorType.SEEK

	def ArriveOn(self):
		self.m_nFlags = self.m_nFlags | BehaviorType.ARRIVE

	def PursuitOn(self):
		self.m_nFlags = self.m_nFlags | BehaviorType.PURSUIT

	def SeparationOn(self):
		self.m_nFlags = self.m_nFlags | BehaviorType.SEPARATION

	def InterposeOn(self, fD):
		self.m_nFlags = self.m_nFlags | BehaviorType.INTERPOSE
		self.m_fInterposeDist = fD

	def SeekOff(self):
		if self.On(BehaviorType.SEEK):
			self.m_nFlags = self.m_nFlags ^ BehaviorType.SEEK

	def ArriveOff(self):
		if self.On(BehaviorType.ARRIVE):
			self.m_nFlags = self.m_nFlags ^ BehaviorType.ARRIVE

	def PursuitOff(self):
		if self.On(BehaviorType.PURSUIT):
			self.m_nFlags = self.m_nFlags ^ BehaviorType.PURSUIT

	def SeparationOff(self):
		if self.On(BehaviorType.SEPARATION):
			self.m_nFlags = self.m_nFlags ^ BehaviorType.SEPARATION

	def InterposeOff(self):
		if self.On(BehaviorType.INTERPOSE):
			self.m_nFlags = self.m_nFlags ^ BehaviorType.INTERPOSE

	def SeekIsOn(self):
		return self.On(BehaviorType.SEEK)

	def ArriveIsOn(self):
		return self.On(BehaviorType.ARRIVE)

	def PursuitIsOn(self):
		return self.On(BehaviorType.PURSUIT)

	def SeparationIsOn(self):
		return self.On(BehaviorType.SEPARATION)

	def InterposeIsOn(self):
		return self.On(BehaviorType.INTERPOSE)
