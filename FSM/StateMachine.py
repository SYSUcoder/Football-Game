# -*- coding: UTF-8 -*-

import copy
from FSM.State import *

class StateMachine:
	def __init__(self, oOwner):
		self.m_oOwner = copy.deepcopy(oOwner)
		self.m_oCurrentState = None
		self.m_oPreviousState = None
		self.m_oGlobalState = None

	def SetCurrentState(self, oS):
		self.m_oCurrentState = copy.deepcopy(oS)

	def SetGlobalState(self, oS):
		self.m_oGlobalState = copy.deepcopy(oS)

	def SetPreviousState(self, oS):
		self.m_oPreviousState = copy.deepcopy(oS)

	def Update(self):
		if self.m_oGlobalState:
			self.m_oGlobalState.Execute(self.m_oOwner)

		if self.m_oCurrentState:
			self.m_oCurrentState.Execute(self.m_oOwner)

	def HandleMessage(self, tMsg):
		if self.m_oCurrentState and self.m_oCurrentState.OnMessage(self.m_oOwner, tMsg):
			return True

		if self.m_oGlobalState and self.m_oGlobalState.OnMessage(self.m_oOwner, tMsg):
			return True

		return False

	def ChangeState(self, oNewState):
		if not oNewState:
			print "NewState is none!\n"
			return
		self.m_oPreviousState = self.m_oCurrentState
		self.m_oCurrentState.Exit(self.m_oOwner)
		self.m_oCurrentState = copy.deepcopy(oNewState)
		self.m_oCurrentState.Enter(self.m_oOwner)

	def RevertToPreviousState(self):
		self.ChangeState(self.m_oPreviousState)

	def isInState(self, oSt):
		if type(self.m_oCurrentState) == type(oSt):
			return True
		return False

	def CurrentState(self):
		return self.m_oCurrentState

	def GlobalState(self):
		return self.m_oGlobalState

	def PreviousState(self):
		return self.m_oPreviousState

	def GetNameOfCurrentState(self):
		return self.m_oCurrentState