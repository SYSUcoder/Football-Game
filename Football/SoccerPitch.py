# -*- coding: UTF-8 -*-

from V2D.Wall2D import *
from V2D.Vector2D import *
from Game.Region import *
from Data import *
from Football.Goal import *
from Football.SoccerBall import *

class SoccerPitch:
	nTick = 0

	def __init__(self, nCxClient, nCyClient):
		self.m_nCxClient = nCxClient
		self.m_nCyClient = nCyClient
		self.m_bPaused = False
		self.m_bGoalKeeperHasBall = False
		self.m_bGameOn = True
		# 初始化Region表，预先分配长度
		self.m_lRegions = [None] * (Data.NUMREGIONSHORIZONTAL * Data.NUMREGIONSVERTICAL)
		self.m_lWalls = []
		
		self.m_oPlayingArea = Region(20, 20, nCxClient - 20, nCyClient - 20)
		self.CreateRegions(PlayingArea().Width() / float(Data.NUMREGIONSHORIZONTAL),
			               PlayingArea().Height() / float(Data.NUMREGIONSVERTICAL)
			              )

		self.m_oRedGoal = Goal(Vector2D(self.m_oPlayingArea.Left(), (nCyClient - Params.GOALWIDTH) / 2),
		                       Vector2D(self.m_oPlayingArea.Left(), nCyClient - (nCyClient - Params.GOALWIDTH) / 2),
		                       Vector2D(1, 0)
		                      )

		self.m_oBlueGoal = Goal(Vector2D(self.m_oPlayingArea.Right(), (nCyClient - Params.GOALWIDTH) / 2),
		                       Vector2D(self.m_oPlayingArea.Right(), nCyClient - (nCyClient - Params.GOALWIDTH) / 2),
		                       Vector2D(-1, 0)
		                      )

		self.m_oBall = SoccerBall(Vector2D(self.m_nCxClient / 2.0, self.m_nCyClient / 2.0),
							      Params.BALLSIZE,
							      Params.BALLMASS,
							      self.m_lWalls
			                     )

		# SoccerTeam暂未实现
		self.m_oRedTeam = SoccerTeam(self.m_oRedGoal, m_oBlueGoal, self, Data.RED)
		self.m_oBlueTeam = SoccerTeam(self.m_oBlueGoal, m_oRedGoal, self, Data.BLUE)

		self.m_oRedTeam.SetOpponents(self.m_oBlueTeam)
		self.m_oBlueTeam.SetOpponents(self.m_oRedTeam)

		vTopLeft = Vector2D(self.m_oPlayingArea.Left(), self.m_oPlayingArea.Top())
		vTopRight = Vector2D(self.m_oPlayingArea.Right(), self.m_oPlayingArea.Top())
		vBottomRight = Vector2D(self.m_oPlayingArea.Right(), self.m_oPlayingArea.Bottom())
		vBottomLeft = Vector2D(self.m_oPlayingArea.Left(), self.m_oPlayingArea.Bottom())

		self.m_lWalls.append(Wall2D(vBottomLeft, self.m_oRedGoal.RightPost() ) )
		self.m_lWalls.append(Wall2D(self.m_oRedGoal.LeftPost(), vTopLeft) )
		self.m_lWalls.append(Wall2D(vTopLeft, vTopRight) )
		self.m_lWalls.append(Wall2D(vTopRight, self.m_oBlueGoal.LeftPost()) )
		self.m_lWalls.append(Wall2D(self.m_oBlueGoal.RightPost(), vBottomRight) )
		self.m_lWalls.append(Wall2D(self.vBottomRight, vBottomLeft) )

	def Update(self):
		if self.m_bPaused:
			return
		self.m_oBall.Update()

		self.m_oRedTeam.Update()
		self.m_oBlueTeam.Update()

		if self.m_oBlueGoal.Scored(self.m_oBall) or self.m_oRedGoal.Scored(self.m_oBall):
			self.m_bGameOn = False
			self.m_oBall.PlaceAtPosition(Vector2D(self.m_nCxClient / 2.0, self.m_nCyClient / 2.0) )

			# 暂未实现
			self.m_oRedTeam.GetFSM().ChangeState()
			self.m_oBlueTeam.GetFSM().ChangeState()

	def CreateRegions(self, fWidth, fHeight):
		nIdx = len(self.m_lRegions) - 1
		for nCol in xrange(Data.NUMREGIONSHORIZONTAL):
			for nRow in xrange(Data.NUMREGIONSVERTICAL):
				self.m_lRegions[nIdx--] = Region(PlayingArea().Left() + nCol*fWidth,
												 PlayingArea().Top() + nRow*fHeight,
                                                 PlayingArea().Left() + (nCol + 1)*fWidth,
                                                 PlayingArea().Top() + (nRow + 1)*fHeight,
                                                 nIdx
												)

	def Render(self):
		return

	def TogglePause(self):
		self.m_bPaused = not self.m_bPaused

	def Paused(self):
		return self.m_bPaused

	def cxClient(self):
		return self.m_nCxClient

	def cyClient(self):
		return self.m_nCyClient

	def GoalKeeperHasBall(self):
		return self.m_bGoalKeeperHasBall

	def SetGoalKeeperHasBall(self, bB):
		self.m_bGoalKeeperHasBall = bB

	def PlayingArea(self):
		return self.m_oPlayingArea

	def Walls(self):
		return self.m_lWalls

	def Ball(self):
		return self.m_oBall

	def GetRegionFromIndex(self, nIdx):
		if not( nIdx >= 0 and nIdx < len(self.m_lRegions)):
			print "Region index wrong!\n"
			return
		return self.m_lRegions[nIdx]

	def GameOn(self):
		return self.m_bGameOn

	def SetGameOn(self):
		self.m_bGameOn = True

	def SetGameOff(self):
		self.m_bGameOn = False
