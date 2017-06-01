# -*- coding: UTF-8 -*-

import math
from misc.utils import *
from V2D.Vector2D import *


class C2DMatrix:
	def __init__(self):
		self.Identity()

	def SetFirstLine(self, fX, fY, fZ):
		self._11, self._12, self._13 = fX, fY, fZ

	def GetFirstLine(self):
		return [self._11, self._12, self._13]

	def SetSecondLine(self, fX, fY, fZ):
		self._21, self._22, self._23 = fX, fY, fZ

	def GetSecondLine(self):
		return [self._21, self._22, self._23]

	def SetThirdLine(self, fX, fY, fZ):
		self._31, self._32, self._33 = fX, fY, fZ

	def GetThirdLine(self):
		return [self._31, self._32, self._33]

	def CopyValue(self, mIn):
		# 将mIn的值赋值给self
		lFirstLine = mIn.GetFirstLine()
		lSecondLine = mIn.GetSecondLine()
		lThirdLine = mIn.GetThirdLine()

		self._11, self._12, self._13 = lFirstLine[0], lFirstLine[1], lFirstLine[2]
		self._21, self._22, self._23 = lSecondLine[0], lSecondLine[1], lSecondLine[2]
		self._31, self._32, self._33 = lThirdLine[0], lThirdLine[1], lThirdLine[2]



	def MatrixMultiply(self, mIn):
		mTemp = C2DMatrix()
		lFirstLine = mIn.GetFirstLine()
		lSecondLine = mIn.GetSecondLine()
		lThirdLine = mIn.GetThirdLine()

		fX = self._11*lFirstLine[0] + self._12*lSecondLine[0] + self._13*lThirdLine[0]
		fY = self._11*lFirstLine[1] + self._12*lSecondLine[1] + self._13*lThirdLine[1]
		fZ = self._11*lFirstLine[2] + self._12*lSecondLine[2] + self._13*lThirdLine[2]
		mTemp.SetFirstLine(fX, fY, fZ)

		fX = self._21*lFirstLine[0] + self._22*lSecondLine[0] + self._23*lThirdLine[0]
		fY = self._21*lFirstLine[1] + self._22*lSecondLine[1] + self._23*lThirdLine[1]
		fZ = self._21*lFirstLine[2] + self._22*lSecondLine[2] + self._23*lThirdLine[2]
		mTemp.SetSecondLine(fX, fY, fZ)

		fX = self._31*lFirstLine[0] + self._32*lSecondLine[0] + self._33*lThirdLine[0]
		fY = self._31*lFirstLine[1] + self._32*lSecondLine[1] + self._33*lThirdLine[1]
		fZ = self._31*lFirstLine[2] + self._32*lSecondLine[2] + self._33*lThirdLine[2]
		mTemp.SetThirdLine(fX, fY, fZ)

		self.CopyValue(mTemp)

	def TransformVector2Ds(self, lPoint):
		for i, vPoint in enumerate(lPoint):
			fTempX = self._11*lPoint[i].GetX() + self._21*lPoint[i].GetY() + self._31
			fTempY = self._12*lPoint[i].GetX() + self._22*lPoint[i].GetY() + self._32
			lPoint[i].SetX(fTempX)
			lPoint[i].SetY(fTempY)

	def TransformVector2D(self, vPoint):
		fTempX = self._11*vPoint.GetX() + self._21*vPoint.GetY() + self._31
		fTempY = self._12*vPoint.GetX() + self._22*vPoint.GetY() + self._32
		return Vector2D(fTempX, fTempY)

	def Identity(self):
		self._11, self._12, self._13 = 1, 0, 0
		self._21, self._22, self._23 = 0, 1, 0
		self._31, self._32, self._33 = 0, 0, 1

	def Translate(self, fX, fY):
		mMat = C2DMatrix()
		mMat.SetFirstLine(1, 0, 0)
		mMat.SetSecondLine(0, 1, 0)
		mMat.SetThirdLine(fX, fY, 1)

		self.MatrixMultiply(mMat)

	def Scale(self, fXScale, fYScale):
		mMat = C2DMatrix()
		mMat.SetFirstLine(fXScale, 0, 0)
		mMat.SetSecondLine(0, fYScale, 0)
		mMat.SetThirdLine(0, 0, 1)

		self.MatrixMultiply(mMat)

	def Rotate(self, fRot):
		mMat = C2DMatrix()
		fSin = math.sin(fRot)
		fCos = math.cos(fRot)

		mMat.SetFirstLine(fCos, fSin, 0)
		mMat.SetSecondLine(-fSin, fCos, 0)
		mMat.SetThirdLine(0, 0, 1)

		self.MatrixMultiply(mMat)

	def RotateByVec(self, vFwd, vSide):
		mMat = C2DMatrix()
		mMat.SetFirstLine(vFwd.GetX(), vFwd.GetY(), 0)
		mMat.SetSecondLine(vSide.GetX(), vSide.GetY(), 0)
		mMat.SetThirdLine(0, 0, 1)

		self.MatrixMultiply(mMat)

	def Print(self):
		print self._11, self._12, self._13
		print self._21, self._22, self._23
		print self._31, self._32, self._33
