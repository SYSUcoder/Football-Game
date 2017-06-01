# -*- coding: UTF-8 -*-
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
		self.nID = -1
		self.nType = -1
		self.bTag = False
		self.vPosition = None
		self.vScale = None
		self.fBoundingRadius = 0.0

		self.SetID(nID)

	def SetID(self, nVal):
		if nVal < BaseGameEntity.nNextValidID:
			print "Invalid ID!"
			return
		self.nID = nVal
		BaseGameEntity.nNextValidID = self.nID + 1

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
		return self.vPosition

	def SetPos(self, vNewPos):
		self.vPosition = vNewPos

	def BRadius(self):
		return self.fBoundingRadius

	def SetBRadius(self, fR):
		self.fBoundingRadius = fR

	def ID(self):
		return self.nID

	def IsTagged(self):
		return self.bTag

	def Tag(self):
		self.bTag = True

	def UnTag(self):
		self.bTag = False

	def Scale(self):
		return self.vScale

	def SetScaleByVec(self, vVal):
		self.fBoundingRadius *= MaxOf(vVal.GetX(), vVal.GetY()) / MaxOf(self.vScale.GetX(), self.vScale.GetY())
		self.vScale = vVal

	def SetScale(self, fVal):
		self.fBoundingRadius *= fVal / MaxOf(self.vScale.GetX(), self.vScale.GetY())
		self.vScale = Vector2D(fVal, fVal)

	def EntityType(self):
		return self.nType

	def SetEntityType(self, nNewType):
		self.nType = nNewType
