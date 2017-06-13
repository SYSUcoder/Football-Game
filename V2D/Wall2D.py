# -*- coding: UTF-8 -*-

from V2D.Vector2D import *

class Wall2D:
	def __init__(self, vA = None, vB = None, vN = None):
		self.m_vA = vA
		self.m_vB = vB
		if vN == None:
			self.CalculateNormal()

	def CalculateNormal(self):
		self.m_vN = Vector2D(0, 0)
		vTemp = Vec2DNormalize(self.m_vB.Minus(self.m_vA))
		self.m_vN.SetX(-vTemp.GetY())
		self.m_vN.SetY(vTemp.GetX())

	def Render(self, bRenderNormals = False):
		# 画出线条
		return

	def From(self):
		return self.m_vA

	def SetFrom(self, vVec):
		self.m_vA = vVec
		self.CalculateNormal()

	def To(self):
		return self.m_vB

	def SetTo(self, vVec):
		self.m_vB = vVec
		self.CalculateNormal()

	def Normal(self):
		return self.m_vN

	def SetNormal(self, vN):
		self.m_vN = vN

	def Center(self):
		return (self.m_vA.Plus(self.m_vB)).Divide(2.0)
