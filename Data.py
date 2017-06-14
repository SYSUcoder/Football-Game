# -*- coding: UTF-8 -*-

class Data:
	MINDOUBLE = 0.0000001
	CLOCKWISE = 1
	ANTICLOCKWISE = -1
	PLANE_BACKSIDE = 0
	PLANE_FRONT = 1
	ON_PLANE = 2
	PI = 3.14159
	LEFT_KEEPER_X = 40
	SMALLESTDELAY = 0.25
	NUMREGIONSHORIZONTAL = 6
	NUMREGIONSVERTICAL = 3
	BLUE = 0
	RED = 1
	GOAL_KEEPER = 0
	ATTACKER = 1
	DEFENDER = 2

class Miner:
	COMFORTLEVEL = 5
	MAXNUGGETS = 3
	THIRSTLEVEL = 5
	TIREDNESSTHRESHOLD = 5

class Location:
	SHACK = 0
	GOLDMINE = 1
	BANK = 2
	SALOON = 3

class Filename:
	BACKGROUND_IMAGE_FILENAME = "Football/image/background.jpg"
	RED_TEAM_MEMBER_FILENAME = "Football/image/red_team.png"
	BLUE_TEAM_MEMBER_FILENAME = "Football/image/blue_team.png"
	FOOTBALL_FILENAME = "Football/image/football.png"

class Params:
	FRICTION = -0.015
	PLAYERKICKINGACCURACY = 0.99
	GOALWIDTH = 100
	BALLSIZE = 5.0
	BALLMASS = 1.0
	NUMSWEETSPOTSX = 13
	NUMSWEETSPOTSY = 6
	SUPPORTSPOTUPDATEFREQ = 1
	MAXPASSINGFORCE = 3.0
	SPOT_CANPASSSCORE = 2.0
	MAXSHOOTINGFORCE = 6.0
	SPOT_CANSCOREFROMPOSITIONSCORE = 1.0
	SPOT_DISTFROMCONTROLLINGPLAYERSCORE = 2.0
	
class RegionData:
	HALFSIZE = 0
	NORMAL = 1