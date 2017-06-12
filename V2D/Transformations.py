# -*- coding: UTF-8 -*-

import copy
from V2D.Vector2D import *
from V2D.C2DMatrix import C2DMatrix

def WorldTransformWithScale(lPoints, vPos, vForward, vSide, vScale):
	lTranVector2Ds = copy.deepcopy(lPoints)
	mMatTransform = C2DMatrix()
	if vScale.GetX() != 1.0 or vScale.GetY() != 1.0:
		mMatTransform.Scale(vScale.GetX(), vScale.GetY())
	mMatTransform.Rotate(vForward, vSide)
	mMatTransform.Translate(vPos.GetX(), vPos.GetY())
	mMatTransform.TransformVector2Ds(lTranVector2Ds)
	return lTranVector2Ds

def WorldTransform(lPoints, vPos, vForward, vSide):
	lTranVector2Ds = copy.deepcopy(lPoints)
	mMatTransform = C2DMatrix()
	mMatTransform.Rotate(vForward, vSide)
	mMatTransform.Translate(vPos.GetX(), vPos.GetY())
	mMatTransform.TransformVector2Ds(lTranVector2Ds)
	return lTranVector2Ds

def PointToWorldSpace(vPoint, vAgentHeading, vAgentSide, vAgentPosition):
	vTransPoint = vPoint
	mMatTransform = C2DMatrix()
	mMatTransform.Rotate(vAgentHeading, vAgentSide)
	mMatTransform.Translate(vAgentPosition.GetX(), vAgentPosition.GetY())
	vTransPoint = mMatTransform.TransformVector2D(vTransPoint)
	return vTransPoint

def VectorToWorldSpace(vVec, vAgentHeading, vAgentSide):
	vTransVec = vVec
	mMatTransform = C2DMatrix()
	mMatTransform.Rotate(vAgentHeading, vAgentSide)
	vTransVec = mMatTransform.TransformVector2D(vTransVec)
	return vTransVec

def PointToLocalSpace(vPoint, vAgentHeading, vAgentSide, vAgentPosition):
	vTransPoint = vPoint
	mMatTransform = C2DMatrix()
	fTx = -vAgentPosition.Dot(vAgentHeading)
	fTy = -vAgentPosition.Dot(vAgentSide)

	lFirstLine = mMatTransform.GetFirstLine()
	lSecondLine = mMatTransform.GetSecondLine()
	lThirdLine = mMatTransform.GetThirdLine()

	mMatTransform.SetFirstLine(vAgentHeading.GetX(), vAgentSide.GetX(), lFirstLine[2])
	mMatTransform.SetSecondLine(vAgentHeading.GetY(), vAgentSide.GetY(), lSecondLine[2])
	mMatTransform.SetThirdLine(fTx, fTy, lThirdLine[2])

	vTransPoint = mMatTransform.TransformVector2D(vTransPoint)
	return vTransPoint

def VectorToLocalSpace(vVec, vAgentHeading, vAgentSide):
	vTransPoint = copy.deepcopy(vVec)
	mMatTransform = C2DMatrix()

	lFirstLine = mMatTransform.GetFirstLine()
	lSecondLine = mMatTransform.GetSecondLine()
	lThirdLine = mMatTransform.GetThirdLine()

	mMatTransform.SetFirstLine(vAgentHeading.GetX(), vAgentSide.GetX(), lFirstLine[2])
	mMatTransform.SetSecondLine(vAgentHeading.GetY(), vAgentSide.GetY(), lSecondLine[2])

	vTransPoint = mMatTransform.TransformVector2D(vTransPoint)
	return vTransPoint

def Vec2DRotateAroundOrigin(vVec, fAng):
	mMatTransform = C2DMatrix()
	mMatTransform.Rotate(fAng)
	return mMatTransform.TransformVector2D(vVec)

def CreateWhiskers(nNumWhiskers, fWhiskerLength, fFov, vFacing, vOrigin):
	fSectorSize = fFov / (nNumWhiskers - 1)
	lWhiskers = []
	fAngle = -fFov * 0.5
	for w in xrange(nNumWhiskers):
		vTemp = Vec2DRotateAroundOrigin(vFacing, fAngle)
		lWhiskers.append(vOrigin.Plus(vTemp.Multiply(fWhiskerLength) ))
		fAngle += fSectorSize
	return lWhiskers