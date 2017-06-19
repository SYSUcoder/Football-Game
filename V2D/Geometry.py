# -*- coding: UTF-8 -*-

import math
from misc.utils import *
from V2D.Vector2D import *
from V2D.C2DMatrix import C2DMatrix
from V2D.Transformations import *
from Data import Data

def DistanceToRayPlaneIntersection(vRayOrigin, vRayHeading, vPlanePoint, vPlaneNormal):
	fD = vPlaneNormal.Dot(vPlanePoint)
	fNumer = vPlaneNormal.Dot(vRayOrigin) + fD
	fDenom = vPlaneNormal.Dot(vRayHeading)

	if (fDenom < 0.000001) and (fDenom > -0.000001):
		return -1.0

	return -(fNumer / fDenom)

def WhereIsPoint(vPoint, vPointOnPlane, vPlaneNormal):
	vDir = vPointOnPlane.Minus(vPoint)
	fD = vDir.Dot(vPlaneNormal)

	if fD < -0.000001:
		return Data.PLANE_FRONT
	elif fD > 0.000001:
		return Data.PLANE_BACKSIDE
	else:
		return Data.ON_PLANE

def GetRayCircleIntersect(vRayOrigin, vRayHeading, vCircleOrigin, fRadius):
	vToCircle = vCircleOrigin.Minus(vRayOrigin)
	fLength = vToCircle.Length()
	fV = vToCircle.Dot(vRayHeading)
	fD = fRadius**2 - (fLength**2 - fV**2)

	if fD < 0.0:
		return -1.0
	return fV - math.sqrt(fD)

def DoRayCircleIntersect(vRayOrigin, vRayHeading, vCircleOrigin, fRadius):
	vToCircle = vCircleOrigin.Minus(vRayOrigin)
	fLength = vToCircle.Length()
	fV = vToCircle.Dot(vRayHeading)
	fD = fRadius**2 - (fLength**2 - fV**2)

	return fD < 0.0

def GetTangentPoints(vC, fR, vP, vT1, vT2):
	# vT1&vT2为传引用
	vPmC = vP.Minus(vC)
	fSqrLen = vPmC.LengthSq()
	fRSqr = fR**2
	if fSqrLen <= fRSqr:
		return False

	fInvSqrLen = 1 / fSqrLen
	fRoot = math.sqrt(math.fabs(fSqrLen - fRSqr))

	vT1.SetX(vC.GetX() + fR*(fR*vPmC.GetX() - vPmC.GetY()*fRoot)*fInvSqrLen)
	vT1.SetY(vC.GetY() + fR*(fR*vPmC.GetY() + vPmC.GetX()*fRoot)*fInvSqrLen)
	vT2.SetX(vC.GetX() + fR*(fR*vPmC.GetX() + vPmC.GetY()*fRoot)*fInvSqrLen)
	vT2.SetY(vC.GetY() + fR*(fR*vPmC.GetY() - vPmC.GetX()*fRoot)*fInvSqrLen)
	return True

def DistToLineSegment(vA, vB, vP):
	fDotA = (vP.GetX() - vA.GetX())*(vB.GetX() - vA.GetX()) + (vP.GetY() - vA.GetY())*(vB.GetY() - vA.GetY())
	if fDotA <= 0:
		return Vec2DDistance(vA, vP)
	fDotB = (vP.GetX() - vB.GetX())*(vA.GetX() - vB.GetX()) + (vP.GetY() - vB.GetY())*(vA.GetY() - vB.GetY())
	if fDotB <= 0:
		return Vec2DDistance(vB, vP)

	# Vector2D Point = A + ((B - A) * dotA)/(dotA + dotB);
	vPoint = vA.Plus(((vB.Minus(vA) ).Multiply(fDotA) ).Divide(fDotA + fDotB) )

	return Vec2DDistance(vP, vPoint)

def DistToLineSegmentSq(vA, vB, vP):
	fDotA = (vP.GetX() - vA.GetX())*(vB.GetX() - vA.GetX()) + (vP.GetY() - vA.GetY())*(vB.GetY() - vA.GetY())
	if fDotA <= 0:
		return Vec2DDistanceSq(vA, vP)
	fDotB = (vP.GetX() - vB.GetX())*(vA.GetX() - vB.GetX()) + (vP.GetY() - vB.GetY())*(vA.GetY() - vB.GetY())
	if fDotB <= 0:
		return Vec2DDistanceSq(vB, vP)

	# Vector2D Point = A + ((B - A) * dotA)/(dotA + dotB);
	vPoint = vA.Plus(((vB.Minus(vA) ).Multiply(fDotA) ).Divide(fDotA + fDotB) )

	return Vec2DDistanceSq(vP, vPoint)

def LineIntersection2D(vA, vB, vC, vD):
	fRTop = (vA.GetY() - vC.GetY())*(vD.GetX() - vC.GetX()) - (vA.GetX() - vC.GetX())*(vD.GetY() - vC.GetY())
	fSTop = (vA.GetY() - vC.GetY())*(vB.GetX() - vA.GetX()) - (vA.GetX() - vC.GetX())*(vB.GetY() - vA.GetY())
	fBot = (vB.GetX() - vA.GetX())*(vD.GetY() - vC.GetY()) - (vB.GetY() - vA.GetY())*(vD.GetX() - vC.GetX())

	if fBot == 0:
		return False

	fInvBot = 1.0 / fBot
	fR = fRTop * fInvBot
	fS = fSTop * fInvBot

	if (fR > 0) and (fR < 1) and (fS > 0) and (fS < 1):
		return True
	return False

def LineIntersection2DByDist(vA, vB, vC, vD, fDist):
	fRTop = (vA.GetY() - vC.GetY())*(vD.GetX() - vC.GetX()) - (vA.GetX() - vC.GetX())*(vD.GetY() - vC.GetY())
	fSTop = (vA.GetY() - vC.GetY())*(vB.GetX() - vA.GetX()) - (vA.GetX() - vC.GetX())*(vB.GetY() - vA.GetY())
	fBot = (vB.GetX() - vA.GetX())*(vD.GetY() - vC.GetY()) - (vB.GetY() - vA.GetY())*(vD.GetX() - vC.GetX())

	if fBot == 0:
		if isEqual(fRTop, 0) and isEqual(fSTop, 0):
			# 分别平行于x轴和y轴，此时相交
			return -2 # True
		else:
			return -1 # False

	fR = fRTop / fBot
	fS = fSTop / fBot
	if (fR > 0) and (fR < 1) and (fS > 0) and (fS < 1):
		return Vec2DDistance(vA, vB) * fR
	else:
		return 0 # fDist = 0 and False

def LineIntersection2DByDistAndPoint(vA, vB, vC, vD, fDist, vPoint):
	fRTop = (vA.GetY() - vC.GetY())*(vD.GetX() - vC.GetX()) - (vA.GetX() - vC.GetX())*(vD.GetY() - vC.GetY())
	fRBot = (vB.GetX() - vA.GetX())*(vD.GetY() - vC.GetY()) - (vB.GetY() - vA.GetY())*(vD.GetX() - vC.GetX())

	fSTop = (vA.GetY() - vC.GetY())*(vB.GetX() - vA.GetX()) - (vA.GetX() - vC.GetX())*(vB.GetY() - vA.GetY())
	fSBot = (vB.GetX() - vA.GetX())*(vD.GetY() - vC.GetY()) - (vB.GetY() - vA.GetY())*(vD.GetX() - vC.GetX())

	if (fRBot == 0) or (fSBot == 0):
		return -1 # False

	fR = fRTop / fRBot
	fS = fSTop / fSBot
	if (fR > 0) and (fR < 1) and (fS > 0) and (fS < 1):
		return (Vec2DDistance(vA, vB) * fR, vA.Plus((vB.Minus(vA) ).Multiply(fR) ) )
	else:
		return 0 # fDist = 0 and False

def ObjectIntersection2D(lList1, lList2):
	for r in xrange(len(lList1) - 1):
		for t in xrange(len(lList2) - 1):
			if LineIntersection2D(lList2[t], lList2[t + 1], lList1[r], lList1[r + 1]):
				return True

	return False

def SegmentObjectIntersection2D(vA, vB, lList):
	for r in xrange(len(lList) - 1):
		if LineIntersection2D(vA, vB, lList[r], lList[r + 1]):
			return True

	return False

def TwoCirclesOverlapped(fX1, fY1, fR1, fX2, fY2, fR2):
	fDistBetweenCenters = math.sqrt((fX1 - fX2)**2 + (fY1 - fY2)**2)
	if (fDistBetweenCenters < (fR1 + fR2)) or (fDistBetweenCenters < math.fabs(fR1 - fR2)):
		return True

	return False

def TwoCirclesOverlappedByVec(vC1, fR1, vC2, fR2):
	fDistBetweenCenters = math.sqrt((vC1.GetX() - vC2.GetX())**2 + (vC1.GetY() - vC2.GetY())**2)
	if (fDistBetweenCenters < (fR1 + fR2)) or (fDistBetweenCenters < math.fabs(fR1 - fR2)):
		return True

	return False

def TwoCirclesEnclosed(fX1, fY1, fR1, fX2, fY2, fR2):
	fDistBetweenCenters = math.sqrt((fX1 - fX2)**2 + (fY1 - fY2)**2)
	if fDistBetweenCenters < math.fabs(fR1 - fR2):
		return True
	return False

def TwoCirclesIntersectionPoints(fX1, fY1, fR1, fX2, fY2, fR2):
	if not TwoCirclesOverlapped(fX1, fY1, fR1, fX2, fY2, fR2):
		return None
	fD = math.sqrt((fX1 - fX2)**2 + (fY1 - fY2)**2)

	fA = (fR1 - fR2 + fD**2) / (2 * fD)
	fB = (fR2 - fR1 + fD**2) / (2 * fD)

	fP2X = fX1 + fA*(fX2 - fX1) / fD
	fP2Y = fY1 + fA*(fY2 - fY1) / fD

	fH1 = math.sqrt(fR1**2 - fA**2)

	fP3X = fP2X - fH1*(fY2 - fY1) / fD
	fP3Y = fP2Y + fH1*(fX2 - fX1) / fD

	fH2 = math.sqrt(fR2**2 - fA**2)
	fP4X = fP2X + fH2*(fY2 - fY1) / fD
	fP4Y = fP2Y + fH2*(fX2 - fX1) / fD

	return (fP3X, fP3Y, fP4X, fP4Y)

def TwoCirclesIntersectionArea(fX1, fY1, fR1, fX2, fY2, fR2):
	tTuple = TwoCirclesIntersectionPoints(fX1, fY1, fR1, fX2, fY2, fR2)
	if tTuple == None:
		return 0.0
	fD = math.sqrt((fX1 - fX2)**2 + (fY1 - fY2)**2)
	fCBD = 2 * math.acos((fR2**2 + fD**2 - fR1**2) / (fR2 * fD * 2))
	fCAD = 2 * math.acos((fR1**2 + fD**2 - fR2**2) / (fR1 * fD * 2))

	fArea = 0.5*fCBD*fR2*fR2 - 0.5*fR2*fR2*math.sin(fCBD) + 0.5*fCAD*fR1*fR1 - 0.5*fR1*fR1*math.sin(fCAD)
	return fArea

def CircleArea(fRadius):
	return Data.PI*fRadius*fRadius

def PointInCircle(vPos, fRadius, vP):
	fDistFromCenterSquared = (vP.Minus(vPos)).LengthSq()
	if fDistFromCenterSquared < fRadius**2:
		return True
	return False

def LineSegmentCircleIntersection(vA, vB, vP, fRadius):
	fDistToLineSq = DistToLineSegmentSq(vA, vB, vP)
	if fDistToLineSq < fRadius**2:
		return True
	else:
		return False

def GetLineSegmentCircleClosestIntersectionPoint(vA, vB, vPos, fRadius):
	vToBNorm = Vec2DNormalize(vB.Minus(vA))
	vLocalPos = PointToLocalSpace(vPos, vToBNorm, vToBNorm.Perp(), vA)
	vIntersectionPoint = None
	if (vLocalPos.GetX() + fRadius >= 0) and ((vLocalPos.GetX() - fRadius)**2 <= Vec2DDistanceSq(vB, vA)):
		if math.fabs(vLocalPos.GetY()) < fRadius:
			fA = vLocalPos.GetX()
			fB = vLocalPos.GetY()
			fIp = fA - math.sqrt(fRadius**2 - fB**2)

			if fIp <= 0:
				fIp = fA + math.sqrt(fRadius**2 - fB**2)
			vIntersectionPoint = vA.Plus(vToBNorm.Multiply(fIp))

	return vIntersectionPoint