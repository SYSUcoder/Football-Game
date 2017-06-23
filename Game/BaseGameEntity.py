# -*- coding: UTF-8 -*-

import copy
from Data import Data
from V2D.Vector2D import *

def MaxOf(fX, fY):
	if fX >= fY:
		return fX
	else:
		return fY

class BaseGameEntity:
	nNextValidID = 0

	def __init__(self, nID):
		self.m_nID = -1
		self.m_nType = -1
		self.m_bTag = False
		self.m_vPosition = None
		self.m_vScale = Vector2D(1, 1)
		self.m_fBoundingRadius = 0.0

		self.SetID(nID)

	def SetID(self, nVal):
		assert nVal >= BaseGameEntity.nNextValidID

		self.m_nID = nVal
		BaseGameEntity.nNextValidID = self.m_nID + 1

	def Update(self):
		return

	def Render(self):
		return

	def HandleMessage(self, tMsg):
		return False

	def Write(self, fOs):
		return

	def Read(self, fIs):
		return

	def GetNextValidID(self):
		return BaseGameEntity.nNextValidID

	def ResetNextValidID(self):
		BaseGameEntity.nNextValidID = 0

	def Pos(self):
		return self.m_vPosition

	def SetPos(self, vNewPos):
		self.m_vPosition = copy.deepcopy(vNewPos)

	def BRadius(self):
		return self.m_fBoundingRadius

	def SetBRadius(self, fR):
		self.m_fBoundingRadius = fR

	def ID(self):
		return self.m_nID

	def IsTagged(self):
		return self.m_bTag

	def Tag(self):
		self.m_bTag = True

	def UnTag(self):
		self.m_bTag = False

	def Scale(self):
		return self.m_vScale

	def SetScaleByVec(self, vVal):
		self.m_fBoundingRadius *= MaxOf(vVal.GetX(), vVal.GetY()) / MaxOf(self.m_vScale.GetX(), self.m_vScale.GetY())
		self.m_vScale = copy.deepcopy(vVal)

	def SetScale(self, fVal):
		self.m_fBoundingRadius *= fVal / MaxOf(self.m_vScale.GetX(), self.m_vScale.GetY())
		self.m_vScale = Vector2D(fVal, fVal)

	def EntityType(self):
		return self.m_nType

	def SetEntityType(self, nNewType):
		self.m_nType = nNewType
