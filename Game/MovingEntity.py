# -*- coding: UTF-8 -*-

import math
import copy
from V2D.Vector2D import *
from Game.BaseGameEntity import BaseGameEntity
from misc.utils import *
from V2D.C2DMatrix import *

class MovingEntity(BaseGameEntity):
	def __init__(self, vPosition, fRadius, vVelocity, fMaxSpeed, vHeading,
		               fMass, vScale, fTurnRate, fMaxForce):
		BaseGameEntity.__init__(self, BaseGameEntity.nNextValidID)
		
		self.SetPos(vPosition)
		self.SetBRadius(fRadius)
		self.SetScaleByVec(vScale)

		self.m_vVelocity = copy.deepcopy(vVelocity)
		self.m_fMaxSpeed = fMaxSpeed
		self.m_vHeading = copy.deepcopy(vHeading)
		self.m_vSide = vHeading.Perp()
		self.m_fMass = fMass
		self.m_fMaxTurnRate = fTurnRate
		self.m_fMaxForce = fMaxForce

	def Velocity(self):
		return self.m_vVelocity

	def SetVelocity(self, vNewVel):
		self.m_vVelocity = copy.deepcopy(vNewVel)

	def Mass(self):
		return self.m_fMass

	def Side(self):
		return self.m_vSide

	def MaxSpeed(self):
		return self.m_fMaxSpeed

	def SetMaxSpeed(self, fMaxSpeed):
		self.m_fMaxSpeed = fMaxSpeed

	def MaxForce(self):
		return self.m_fMaxForce

	def SetMaxForce(self, fMaxForce):
		self.m_fMaxForce = fMaxForce

	def IsSpeedMaxedOut(self):
		return self.m_fMaxSpeed**2 >= self.m_vVelocity.LengthSq()

	def Speed(self):
		return self.m_vVelocity.Length()

	def SpeedSq(self):
		return self.m_vVelocity.LengthSq()

	def Heading(self):
		return self.m_vHeading

	def SetHeading(self, vNewHeading):
		if (vNewHeading.LengthSq() - 1.0) < 0.00001:
			print "vNewHeading is not valid!\n"
			return

		self.m_vHeading = copy.deepcopy(vNewHeading)
		self.m_vSide = self.m_vHeading.Perp()

	def RotateHeadingToFacePosition(self, vTarget):
		vToTarget = Vec2DNormalize(vTarget.Minus(self.Pos() ))
		fDot = self.m_vHeading.Dot(vToTarget)
		fDot = Clamp(fDot, -1, 1)
		fAngle = math.acos(fDot)

		if fAngle < 0.00001:
			return True

		if fAngle > self.m_fMaxTurnRate:
			fAngle = self.m_fMaxTurnRate

		RotationMatrix = C2DMatrix()
		RotationMatrix.Rotate(fAngle * self.m_vHeading.Sign(vToTarget))
		RotationMatrix.TransformVector2D(self.m_vHeading)
		RotationMatrix.TransformVector2D(self.m_vVelocity)
		self.m_vSide = self.m_vHeading.Perp()
		return False

	def MaxTurnRate(self):
		return self.m_fMaxTurnRate

	def SetMaxTurnRate(self, fVal):
		self.m_fMaxTurnRate = fVal