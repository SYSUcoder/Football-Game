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
	m_dEntityMap = {}

	def __init__(self):
		return

	def GetEntityFromID(self, nID):
		bIsHasKey = EntityManager.m_dEntityMap.has_key(nID)
		if bIsHasKey:
			return EntityManager.m_dEntityMap[nID]
		else:
			print "This id is not register\n"
			return None

	def RemoveEntity(self, oEntity):
		bIsHasKey = EntityManager.m_dEntityMap.has_key(oEntity.ID())
		if bIsHasKey:
			del EntityManager.m_dEntityMap[oEntity.ID()]
		else:
			print "This entity is not in the dict\n"
			
	def RegisterEntity(self, oNewEntity):
		EntityManager.m_dEntityMap[oNewEntity.ID()] = oNewEntity

	def Reset(self):
		EntityManager.m_dEntityMap.clear()