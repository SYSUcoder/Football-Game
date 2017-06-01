# -*- coding: UTF-8 -*-
import math
from Data import Data

class Vector2D:
	"""二维向量"""

	def __init__(self, x = 0.0, y = 0.0):
		self.x = x
		self.y = y

	def GetX(self):
		return self.x

	def GetY(self):
		return self.y

	def SetX(self, fX):
		self.x = fX

	def SetY(self, fY):
		self.y = fY
	
	def Zero(self):
		self.x = 0.0
		self.y = 0.0

	def isZero(self):
		fNum = self.x*self.x + self.y*self.y
		if fNum < Data.MINDOUBLE:
			return True
		else:
			return False

	def Length(self):
		return math.sqrt(self.x*self.x + self.y*self.y)

	def LengthSq(self):
		return self.x*self.x + self.y*self.y

	def Dot(self, vVec):
		# 点乘
		return self.x*vVec.GetX() + self.y*vVec.GetY()

	def Sign(self, vVec):
		if self.y*vVec.GetX() > self.x*vVec.GetY():
			return Data.ANTICLOCKWISE
		else:
			return Data.CLOCKWISE

	def Perp(self):
		return Vector2D(-self.y, self.x)

	def Distance(self, vVec):
		# 向量距离
		fYSeparation = vVec.GetY() - self.y
		fXSeparation = vVec.GetX() - self.x
		return math.sqrt(fYSeparation**2 + fXSeparation**2)

	def DistanceSq(self, vVec):
		fYSeparation = vVec.GetY() - self.y
		fXSeparation = vVec.GetX() - self.x
		return fYSeparation**2 + fXSeparation**2

	def Truncate(self, fMax):
		# 缩短
		if self.Length() > fMax:
			self.Normalize()
			self.x *= fMax
			self.y *= fMax

	def GetReverse(self):
		return Vector2D(-self.x, -self.y)

	def Reflect(self, vVec):
		# vVec必须为Normalized
		# 反射函数，vVec为墙壁，self为球
		vRVec = vVec.GetReverse()
		self.x += 2.0 * self.Dot(vVec) * vRVec.GetX()
		self.y += 2.0 * self.Dot(vVec) * vRVec.GetY()

	def Normalize(self):
		fVecLength = self.Length()
		if fVecLength > Data.MINDOUBLE:
			self.x /= fVecLength
			self.y /= fVecLength

	# ==================
	# + - * / 
	# ==================
	def Plus(self, vVec):
		# +
		fX = self.x + vVec.GetX()
		fY = self.y + vVec.GetY()
		return Vector2D(fX, fY)

	def Minus(self, vVec):
		# -
		fX = self.x - vVec.GetX()
		fY = self.y - vVec.GetY()
		return Vector2D(fX, fY)

	def Multiply(self, fNum):
		# *
		fX = self.x * fNum
		fY = self.y * fNum
		return Vector2D(fX, fY)

	def Divide(self, fNum):
		# /
		fX = self.x / fNum
		fY = self.y / fNum
		return Vector2D(fX, fY)


	def Print(self):
		print "(", self.x, ",", self.y, ")\n"



def Vec2DNormalize(vVec):
	vNewVec = vVec
	fVecLength = vVec.Length()
	if fVecLength > Data.MINDOUBLE:
		vNewVec.SetX(vVec.GetX() / fVecLength)
		vNewVec.SetY(vVec.GetY() / fVecLength)
	return vNewVec

def Vec2DDistance(vVec1, vVec2):
	fYSeparation = vVec2.GetY() - vVec1.GetY()
	fXSeparation = vVec2.GetX() - vVec1.GetX()
	return math.sqrt(fYSeparation**2 + fXSeparation**2)

def Vec2DDistanceSq(vVec1, vVec2):
	fYSeparation = vVec2.GetY() - vVec1.GetY()
	fXSeparation = vVec2.GetX() - vVec1.GetX()
	return fYSeparation**2 + fXSeparation**2

def Vec2DLength(vVec):
	return math.sqrt(vVec.GetX()**2 + vVec.GetY()**2)

def Vec2DLengthSq(vVec):
	return vVec.GetX()**2 + vVec.GetY()**2


def WrapAround(vVec, nMaxX, nMaxY):
	if vVec.GetX() > nMaxX:
		vVec.SetX(0.0)
	if vVec.GetX() < 0:
		vVec.SetX(float(nMaxX))
	if vVec.GetY() < 0:
		vVec.SetY(float(nMaxY))
	if vVec.GetY() > nMaxY:
		vVec.SetY(0.0)

def NotInsideRegion(vPos, vTopLeft, vBotRgt):
	# 源代码有问题
	return (vPos.GetX() < vTopLeft.GetX()) or (
		   vPos.GetX() > vBotRgt.GetX())   or (
		   vPos.GetY() > vTopLeft.GetY())  or (
		   vPos.GetY() < vBotRgt.GetY())

def InsideRegionByVec(vPos, vTopLeft, vBotRgt):
	return not( (vPos.GetX() < vTopLeft.GetX()) or (
		        vPos.GetX() > vBotRgt.GetX())   or (
		        vPos.GetY() > vTopLeft.GetY())  or (
		        vPos.GetY() < vBotRgt.GetY()) )

def InsideRegion(vPos, nLeft, nTop, nRight, nBottom):
	return not( (vPos.GetX() < nLeft) or (
		        vPos.GetX() > nRight) or (
		        vPos.GetY() > nTop)   or (
		        vPos.GetY() < nBottom) )

def isSecondInFOVOfFirst(vPosFirst, vFacingFirst, vPosSecond, fFov):
	vToTarget = Vec2DNormalize(vPosSecond.Minus(vPosFirst))
	
	return vFacingFirst.Dot(vToTarget) >= math.cos(fFov / 2.0)