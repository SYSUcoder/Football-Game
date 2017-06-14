# -*- coding: UTF-8 -*-

import math

from V2D.Vector2D import *
from Data import *

class Region:
	def __init__(self, fLeft = 0, fTop = 0, fRight = 0, fBottom = 0, nID = -1):
		self.m_fTop = fTop
		self.m_fBottom = fBottom
		self.m_fLeft = fLeft
		self.m_fRight = fRight
		self.m_nID = nID
		self.m_vCenter = Vector2D( (fLeft + fRight) * 0.5, (fTop + fBottom) * 0.5 )
		self.m_fWidth = math.fabs(fRight - fLeft)
		self.m_fHeight = math.fabs(fBottom - fTop)

	def Render(self):
		return

	def Inside(self, vPos, nModifier = RegionData.NORMAL):
		if nModifier == RegionData.NORMAL:
			return ((vPos.GetX() > self.m_fLeft) and
				    (vPos.GetX() < self.m_fRight) and
				    (vPos.GetY() > self.m_fTop) and 
				    (vPos.GetY() < self.m_fBottom)
				   )
		else:
			fMarginX = self.m_fWidth * 0.25
			fMarginY = self.m_fHeight * 0.25

			return ((vPos.GetX() > (self.m_fLeft + fMarginX)) and
				    (vPos.GetX() < (self.m_fRight - fMarginX)) and
				    (vPos.GetY() > (self.m_fTop + fMarginY)) and
				    (vPos.GetY() < (self.m_fBottom - fMarginY))
				   )

	def GetRandomPosition(self):
		return Vector2D(RandInRange(self.m_fLeft, self.m_fRight),
			            RandInRange(self.m_fTop, self.m_fBottom)
			           )

	def Top(self):
		return self.m_fTop

	def Bottom(self):
		return self.m_fBottom

	def Left(self):
		return self.m_fLeft

	def Right(self):
		return self.m_fRight

	def Width(self):
		return math.fabs(self.m_fRight - self.m_fLeft)

	def Height(self):
		return math.fabs(self.m_fTop - self.m_fBottom)

	def Length(self):
		return max(self.Width(), self.Height())

	def Breadth(self):
		return min(self.Width(), self.Height())

	def Center(self):
		return self.m_vCenter

	def ID(self):
		return self.m_nID

