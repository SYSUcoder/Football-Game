# -*- coding: UTF-8 -*-

import pygame
import time
from pygame.locals import *
from sys import exit
from Data import *
from Football.SoccerPitch import *
from Football.SpriteRender import *

def LoadImage():
	oBackground = pygame.image.load(Filename.BACKGROUND_IMAGE_FILENAME).convert()
	oFootball = pygame.image.load(Filename.FOOTBALL_FILENAME).convert_alpha()

	oRedGoalKeeper = pygame.image.load(Filename.RED_TEAM_MEMBER_FILENAME).convert_alpha()
	oRedFieldPlayer1 = pygame.image.load(Filename.RED_TEAM_MEMBER_FILENAME).convert_alpha()
	oRedFieldPlayer2 = pygame.image.load(Filename.RED_TEAM_MEMBER_FILENAME).convert_alpha()
	oRedFieldPlayer3 = pygame.image.load(Filename.RED_TEAM_MEMBER_FILENAME).convert_alpha()
	oRedFieldPlayer4 = pygame.image.load(Filename.RED_TEAM_MEMBER_FILENAME).convert_alpha()

	oBlueGoalKeeper = pygame.image.load(Filename.BLUE_TEAM_MEMBER_FILENAME).convert_alpha()
	oBlueFieldPlayer1 = pygame.image.load(Filename.BLUE_TEAM_MEMBER_FILENAME).convert_alpha()
	oBlueFieldPlayer2 = pygame.image.load(Filename.BLUE_TEAM_MEMBER_FILENAME).convert_alpha()
	oBlueFieldPlayer3 = pygame.image.load(Filename.BLUE_TEAM_MEMBER_FILENAME).convert_alpha()
	oBlueFieldPlayer4 = pygame.image.load(Filename.BLUE_TEAM_MEMBER_FILENAME).convert_alpha()

	SpriteRender.dRenderDict["Screen"] = oScreen
	SpriteRender.dRenderDict["Background"] = oBackground
	SpriteRender.dRenderDict["Football"] = oFootball
	SpriteRender.dRenderDict["RedGoalKeeper"] = oRedGoalKeeper
	SpriteRender.dRenderDict["RedFieldPlayer1"] = oRedFieldPlayer1
	SpriteRender.dRenderDict["RedFieldPlayer2"] = oRedFieldPlayer2
	SpriteRender.dRenderDict["RedFieldPlayer3"] = oRedFieldPlayer3
	SpriteRender.dRenderDict["RedFieldPlayer4"] = oRedFieldPlayer4
	
	SpriteRender.dRenderDict["BlueGoalKeeper"] = oBlueGoalKeeper
	SpriteRender.dRenderDict["BlueFieldPlayer1"] = oBlueFieldPlayer1
	SpriteRender.dRenderDict["BlueFieldPlayer2"] = oBlueFieldPlayer2
	SpriteRender.dRenderDict["BlueFieldPlayer3"] = oBlueFieldPlayer3
	SpriteRender.dRenderDict["BlueFieldPlayer4"] = oBlueFieldPlayer4

	return oBackground

if __name__ == '__main__':
	pygame.init()
	oScreen = pygame.display.set_mode((696, 352), 0, 32)
	pygame.display.set_caption("Football Game")

	# 加载图片
	oBackground = LoadImage()

	# 背景宽和高
	fBackgroundWidth = oBackground.get_width()
	fBackgroundHeight = oBackground.get_height()

	oPitch = SoccerPitch(fBackgroundWidth, fBackgroundHeight)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

		oPitch.Update()
		pygame.display.update()


		x, y = pygame.mouse.get_pos()
		print (x, y)


		time.sleep(0.005)