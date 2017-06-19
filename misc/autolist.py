# -*- coding: UTF-8 -*-

class AutoList:
	# 继承该类的子类会自动添加到AutoList.lMembers中
	lMembers = []

	def __init__(self):
		AutoList.lMembers.append(self)

	def __del__(self):
		# 引用计数器为0会自动回收
		return

	@classmethod
	def GetAllMembers(cls):
		# 类方法
		return AutoList.lMembers

