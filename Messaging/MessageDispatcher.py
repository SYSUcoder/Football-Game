# -*- coding: UTF-8 -*-

from Messaging.Telegram import *
from Game.BaseGameEntity import *
from Game.EntityManager import *
from misc.FrameCounter import *

class Singleton(object):
	# 单例模式
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance

class MessageDispatcher(Singleton):
	def __init__(self, fDelay, nSender, nReceiver, nMsg, oAdditionalInfo = None):
		oReceiver = EntityManager().GetEntityFromID(nReceiver)
		self.m_lPriorityQ = []

		if oReceiver == None:
			print "Warning! No Receiver with ID of", nReceiver, "found\n"
			return
		tTelegram = Telegram(0, nSender, nReceiver, nMsg, oAdditionalInfo)

		if fDelay <= 0.0:
			print "Telegram dispatched at time:", FrameCounter().GetCurrentFrame(),
			print "by", nSender << "for", nReceiver, ". Msg is", nMsg

			self.Discharge(oReceiver, tTelegram)
		else:
			fCurrentTime = FrameCounter().GetCurrentFrame()
			tTelegram.m_fDispatchTime = fCurrentTime + fDelay
			self.m_lPriorityQ.append(tTelegram)

			print "Delayed telegram from", nSender, "recorded at time",
			print FrameCounter().GetCurrentFrame(), "for", nReceiver,
			print ". Msg is", nMsg

	def Discharge(self, oReceiver, tTelegram):
		if not oReceiver.HandleMessage(tTelegram):
			print "Message not handled\n"

	def DispatchDelayedMessages(self):
		fCurrentTime = FrameCounter().GetCurrentFrame()
		while (not len(self.m_lPriorityQ) == 0) and (
			   self.m_lPriorityQ[0].m_fDispatchTime < fCurrentTime) and (
			   self.m_lPriorityQ[0].m_fDispatchTime > 0):
			tTelegram = self.m_lPriorityQ[0]
			oReceiver = EntityManager().GetEntityFromID(tTelegram.m_nReceiver)
			print "Queued telegram ready for dispatch: Sent to", oReceiver.ID(),
			print ". Msg is", tTelegram.m_nMsg

			self.Discharge(oReceiver, tTelegram)
			self.m_lPriorityQ = self.m_lPriorityQ[1:]
