# -*- coding: UTF-8 -*-

import pygame
from pygame.locals import *
from sys import exit

BACKGROUND_IMAGE_FILENAME = "Football/image/image1.jpg"
MOUSE_IMAGE_FILENAME = "Football/image/image2.jpg"

pygame.init()
oScreen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption("Hello World")

oBackground = pygame.image.load(BACKGROUND_IMAGE_FILENAME).convert()
oMouseCursor = pygame.image.load(MOUSE_IMAGE_FILENAME).convert()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

	oScreen.blit(oBackground, (0, 0))
	x, y = pygame.mouse.get_pos()

	x -= oMouseCursor.get_width() / 2
	y -= oMouseCursor.get_height() / 2

	oScreen.blit(oMouseCursor, (x, y))

	pygame.display.update()