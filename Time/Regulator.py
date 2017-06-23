# -*- coding: UTF-8 -*-

import time
import random
from misc.utils import *

class Regulator:
	# 源码timeGetTime()获得的时间单位为毫秒，time.time()的单位为秒
	fUpdatePeriodVariator = 10.0

	def __init__(self, fNumUpdatesPerSecondRqd):
		random.seed()
		self.m_nNextUpdateTime = int(time.time() + random.random()) # 源码用DWORD，无符号双字长整型

		if fNumUpdatesPerSecondRqd > 0:
			self.m_fUpdatePeriod = 1.0 / fNumUpdatesPerSecondRqd
		elif isEqual(0.0, fNumUpdatesPerSecondRqd):
			self.m_fUpdatePeriod = 0.0
		elif fNumUpdatesPerSecondRqd < 0:
			self.m_fUpdatePeriod = -1

	def isReady(self):
		if isEqual(0.0, self.m_fUpdatePeriod):
			return True

		if self.m_fUpdatePeriod < 0:
			return False

		nCurrentTime = int(time.time())
		if nCurrentTime >= self.m_nNextUpdateTime:
			self.m_nNextUpdateTime = int(nCurrentTime + self.m_fUpdatePeriod)
			return True

		return False
