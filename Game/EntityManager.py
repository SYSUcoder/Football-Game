# -*- coding: UTF-8 -*-

from Game.BaseGameEntity import *

class Singleton(object):
	# 单例模式
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance

class EntityManager(Singleton):
	def __init__(self):
		self.m_dEntityMap = {}
		return

	def GetEntityFromID(self, nID):
		bIsHasKey = self.m_dEntityMap.has_key(nID)
		if bIsHasKey:
			return self.m_dEntityMap[nID]
		else:
			print "This id is not register\n"
			return None

	def RemoveEntity(self, oEntity):
		bIsHasKey = self.m_dEntityMap.has_key(oEntity.ID())
		if bIsHasKey:
			del self.m_dEntityMap[oEntity.ID()]
		else:
			print "This entity is not in the dict\n"
			
	def RegisterEntity(self, oNewEntity):
		self.m_dEntityMap[oNewEntity.ID()] = oNewEntity

	def Reset(self):
		self.m_dEntityMap.clear()