# -*- coding: UTF-8 -*-

class Singleton(object):
	# 单例模式
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance

class FrameCounter(Singleton):
	def __init__(self):
		self.m_nCount = 0
		self.m_nFramesElapsed = 0

	def Update(self):
		self.m_nCount = self.m_nCount + 1
		self.m_nFramesElapsed = self.m_nFramesElapsed + 1

	def GetCurrentFrame(self):
		return self.m_nCount

	def Reset(self):
		self.m_nCount = 0

	def Start(self):
		self.m_nFramesElapsed = 0

	def FramesElapsedSinceStartCalled(self):
		return self.m_nFramesElapsed
