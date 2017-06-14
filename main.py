# -*- coding: UTF-8 -*-

import pygame
from pygame.locals import *
from sys import exit
from Data import *


if __name__ == '__main__':
	pygame.init()
	oScreen = pygame.display.set_mode((640, 480), 0, 32)
	pygame.display.set_caption("Football Game")

	# 加载图片
	oBackground = pygame.image.load(Filename.BACKGROUND_IMAGE_FILENAME).convert()
	oRedTeam = pygame.image.load(Filename.RED_TEAM_MEMBER_FILENAME).convert_alpha()
	oBlueTeam = pygame.image.load(Filename.BLUE_TEAM_MEMBER_FILENAME).convert_alpha()
	oFootball = pygame.image.load(Filename.FOOTBALL_FILENAME).convert_alpha()

	# 背景宽和高
	fBackgroundWidth = oBackground.get_width()
	fBackgroundHeight = oBackground.get_height()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

		# 定义初始位置		
		oScreen.blit(oBackground, (0, 0))
		oScreen.blit(oRedTeam, (Data.LEFT_KEEPER_X - oRedTeam.get_width() / 2, 
					            fBackgroundHeight / 2 - oRedTeam.get_height() / 2))
		oScreen.blit(oBlueTeam, (fBackgroundWidth - Data.LEFT_KEEPER_X - oRedTeam.get_width() / 2,
								 fBackgroundHeight /  2 - oBlueTeam.get_height() / 2))
		oScreen.blit(oFootball, (fBackgroundWidth / 2 - oFootball.get_width() / 2,
								 fBackgroundHeight / 2 - oFootball.get_height() / 2))

		x, y = pygame.mouse.get_pos()
		print (x, y)

		pygame.display.update()