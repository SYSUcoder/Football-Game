# -*- coding: UTF-8 -*-

import copy
from V2D.Vector2D import *
from Football.SoccerBall import *
from V2D.Geometry import *

class Goal:
	def __init__(self, vLeft, vRight, vFacing):
		self.m_vLeftPost = copy.deepcopy(vLeft)
		self.m_vRightPost = copy.deepcopy(vRight)
		self.m_vCenter = (vLeft.Plus(vRight)).Divide(2.0)
		self.m_nNumGoalsScored = 0
		self.m_vFacing = copy.deepcopy(vFacing)

	def Scored(self, oBall):
		if LineIntersection2D(oBall.Pos(), oBall.OldPos(), self.m_vLeftPost, self.m_vRightPost):
			self.m_nNumGoalsScored += 1
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