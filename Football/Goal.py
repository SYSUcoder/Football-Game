# -*- coding: UTF-8 -*-

from V2D.Vector2D import *
from Football.SoccerBall import *
from V2D.Geometry import *

class Goal:
	def __init__(self, vLeft, vRight, vFacing):
		self.m_vLeftPost = vLeft
		self.m_vRightPost = vRight
		self.m_vCenter = (vLeft.Plus(vRight)).Divide(2.0)
		self.m_nNumGoalsScored = 0
		self.m_vFacing = vFacing

	def Scored(self, oBall):
		if LineIntersection2D(oBall.Pos(), oBall.OldPos(), self.m_vLeftPost, self.m_vRightPost):
			self.m_nNumGoalsScored++
			return True
		return False

	def Center(self):
		return self.m_vCenter

	def Facing(self):
		return self.m_vFacing

	def LeftPost(self):
		return self.m_vLeftPost

	def RightPost(self):
		return self.m_vRightPost

	def NumGoalsScored(self):
		return self.m_nNumGoalsScored

	def ResetGoalsScored(self):
		self.m_nNumGoalsScored = 0