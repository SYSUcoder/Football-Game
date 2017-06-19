# -*- coding: UTF-8 -*-

import math
from Data import Data

class Telegram:
	def __init__(self, fTime = -1, nSender = -1, nReceiver = -1, nMsg = -1, oInfo = None):
		self.m_fDispatchTime = fTime
		self.m_nSender = nSender
		self.m_nReceiver = nReceiver
		self.m_nMsg = nMsg
		self.m_oInfo = oInfo

	def DispatchTime(self):
		return self.m_fDispatchTime

	def Sender(self):
		return self.m_nSender

	def Receiver(self):
		return self.m_nReceiver

	def Msg(self):
		return self.m_nMsg

	def Info(self):
		return self.m_oInfo

	def Equal(self, tT2):
		return ( math.fabs(self.m_fDispatchTime - tT2.DispatchTime()) < Data.SMALLESTDELAY
			     and self.m_nSender == tT2.Sender()
			     and self.m_nReceiver == tT2.Receiver()
			     and self.m_nMsg == tT2.Msg()
			   )

	def LessThan(self, tT2):
		if self.Equal(tT2):
			return False
		else:
			return self.m_fDispatchTime < tT2.DispatchTime()

	def Print(self):
		print "time: ", self.m_fDispatchTime, ", Sender: ", self.m_nSender,
		print ", Receiver: ", self.m_nReceiver, ", Msg: ", self.m_nMsg

