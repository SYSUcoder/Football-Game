# -*- coding: UTF-8 -*-

from FSM.State import *
from Messaging.Telegram import *
from Football.SoccerTeam import *
from Data import *

def ChangePlayerHomeRegions(oTeam, lNewRegions):
	for plyr in xrange(len(lNewRegions)):
		oTeam.SetPlayerHomeRegion(plyr, lNewRegions[plyr])

class Singleton(object):
	# 单例模式
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance

class Attacking(State, Singleton):
	def __init__(self):
		return

	def Enter(self, oTeam):
		lBlueRegions = [1,12,14,6,4]
		lRedRegions = [16,3,5,9,13]

		if oTeam.Color() == Data.BLUE:
			ChangePlayerHomeRegions(oTeam, lBlueRegions)
		else:
			ChangePlayerHomeRegions(oTeam, lRedRegions)

		oTeam.UpdateTargetsOfWaitingPlayers() # SoccerTeam暂未实现

	def Execute(self, oTeam):
		if not oTeam.InControl():
			oTeam.GetFSM().ChangeState(oDefending)
			return

		oTeam.DetermineBestSupportingPosition()

	def Exit(self, oTeam):
		oTeam.SetSupportingPlayer(None)

	def OnMessage(self, oTeam, tMsg):
		return False

class Defending(State, Singleton):
	def __init__(self):
		return

	def Enter(self, oTeam):
		lBlueRegions = [1,6,8,3,5]
		lRedRegions = [16,9,11,12,14]

		if oTeam.Color() == Data.BLUE:
			ChangePlayerHomeRegions(oTeam, lBlueRegions)
		else:
			ChangePlayerHomeRegions(oTeam, lRedRegions)

		oTeam.UpdateTargetsOfWaitingPlayers()

	def Execute(self, oTeam):
		if oTeam.InControl():
			oTeam.GetFSM().ChangeState(oAttacking)
			return

	def Exit(self, oTeam):
		return

	def OnMessage(self, oTeam, tMsg):
		return

class PrepareForKickOff(State, Singleton):
	def __init__(self):
		return

	def Enter(self, oTeam):
		oTeam.SetControllingPlayer(None)
		oTeam.SetSupportingPlayer(None)
		oTeam.SetReceiver(None)
		oTeam.SetPlayerClosestToBall(None)

		oTeam.ReturnAllFieldPlayersToHome()

	def Execute(self, oTeam):
		if oTeam.AllPlayersAtHome() and oTeam.Opponents().AllPlayersAtHome():
			oTeam.GetFSM().ChangeState(oDefending)

	def Exit(self, oTeam):
		oTeam.Pitch().SetGameOn()

	def OnMessage(self, oTeam, tMsg):
		return