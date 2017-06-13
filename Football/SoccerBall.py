# -*- coding: UTF-8 -*-

import math
from V2D.Vector2D import *
from Game.MovingEntity import MovingEntity
from V2D.Wall2D import *
from V2D.Geometry import *
from Data import *
from Messaging.Telegram import *
from misc.utils import *
from V2D.Transformations import *

class SoccerBall(MovingEntity):
	def __init__(self, vPos, fBallSize, fMass, lPitchBoundary):
		MovingEntity.__init__(self, vPos, fBallSize, Vector2D(0, 0), -1.0, 
			                  Vector2D(0, 1), fMass, Vector2D(1.0, 1.0), 0, 0)
		self.m_lPitchBoundary = lPitchBoundary

	def Update(self):
		self.m_vOldPos = self.Pos()
		self.TestCollisionWithWalls(self.m_lPitchBoundary)

		if self.Velocity().LengthSq() > Params.FRICTION**2:
			self.SetVelocity(self.Velocity().Plus(Vec2DNormalize(self.Velocity()).Multiply(Params.FRICTION) ))
			self.SetPos(self.Pos().Plus(self.Velocity()) )
			self.SetHeading(Vec2DNormalize(self.Velocity()) )

	def Render(self):
		return

	def HandleMessage(self, tMsg):
		return False

	def Kick(self, vDirection, fForce):
		vDirection.Normalize()
		vAcceleration = (vDirection.Multiply(fForce)).Divide(self.Mass())
		self.SetVelocity(vAcceleration)

	def TimeToCoverDistance(self, vFrom, vTo, fForce):
		fSpeed = fForce / self.Mass()
		fDistanceToCover = Vec2DDistance(vFrom, vTo)
		fTerm = fSpeed**2 + 2.0*fDistanceToCover*Data.FRICTION

		if fTerm <= 0.0:
			return -1.0

		fV = math.sqrt(fTerm)
		return (fV - fSpeed) / Data.FRICTION

	def FuturePosition(self, fTime):
		vUt = self.Velocity().Multiply(fTime)
		fHalfAtSquared = 0.5 * Data.FRICTION * fTime * fTime
		vScalarToVector = fHalfAtSquared * Vec2DNormalize(self.Velocity())
		return (self.Pos().Plus(vUt) ).Plus(vScalarToVector)

	def Trap(self):
		self.Velocity().Zero()

	def OldPos(self):
		return self.m_vOldPos

	def PlaceAtPosition(self, vNewPos):
		self.SetPos(vNewPos)
		self.m_vOldPos = self.Pos()
		self.Velocity().Zero()

	def TestCollisionWithWalls(self, lWalls):
		nIdxClosest = -1
		vVelNormal = Vec2DNormalize(self.Velocity())
		fDistToIntersection = 99999999

		for w in xrange(len(lWalls)):
			vThisCollisionPoint = self.Pos().Minus( (lWalls[w].Normal().Multiply(BRadius()) ) )

			if WhereIsPoint(vThisCollisionPoint, lWalls[w].From(), lWalls[w].Normal()) == Data.PLANE_BACKSIDE:
				fDistToWall = DistanceToRayPlaneIntersection(vThisCollisionPoint, lWalls[w].Normal(),
					                                         lWalls[w].From(), lWalls[w].Normal())
				vIntersectionPoint = vThisCollisionPoint.Plus(lWalls[w].Normal().Multiply(fDistToWall))
			else:
				fDistToWall = DistanceToRayPlaneIntersection(vThisCollisionPoint, vVelNormal,
															 lWalls[w].From(), lWalls[w].Normal())
				vIntersectionPoint = vThisCollisionPoint.Plus(vVelNormal.Multiply(fDistToWall))

			bOnLineSegment = False
			if LineIntersection2D(lWalls[w].From(), lWalls[w].To(),
			                  vThisCollisionPoint.Minus(lWalls[w].Normal().Multiply(20.0)),
			                  vThisCollisionPoint.Plus(lWalls[w].Normal().Multiply(20.0))):
				bOnLineSegment = True
			fDistSq = Vec2DDistanceSq(vThisCollisionPoint, vIntersectionPoint)
		
			if fDistSq <= self.Velocity().LengthSq() and fDistSq < fDistToIntersection and bOnLineSegment:
				fDistToIntersection = fDistSq
				nIdxClosest = w
				vCollisionPoint = vIntersectionPoint

		if nIdxClosest >= 0 and vVelNormal.Dot(lWalls[nIdxClosest].Normal()) < 0:
			self.Velocity().Reflect(lWalls[nIdxClosest].Normal()) # 撞墙改变速度方向



def AddNoiseToKick(vBallPos, vBallTarget):
	fDisplacement = (Data.PI - Data.PI*Params.PLAYERKICKINGACCURACY) * RandomClamped()
	vToTarget = vBallTarget.Minus(vBallPos)
	Vec2DRotateAroundOrigin(vToTarget, fDisplacement)
	return vToTarget.Plus(vBallPos)
