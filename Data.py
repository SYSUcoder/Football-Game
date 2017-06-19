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
	SLOW = 3
	NORMAL = 2
	FAST = 1

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
	NUMATTEMPTSTOFINDVALIDSTRIKE = 5
	BNONPENETRATIONCONSTRAINT = 0
	GOALKEEPERINTERCEPTRANGE = 100.0
	GOALKEEPERTENDINGDISTANCE = 20.0
	GOALKEEPERMINPASSDISTANCE = 50.0
	PLAYERKICKFREQUENCY = 8
	CHANCEPLAYERATTEMPTSPOTSHOT = 0.005
	MINPASSDIST = 120.0
	MAXDRIBBLEFORCE = 1.5
	CHANCEOFUSINGARRIVETYPERECEIVEBEHAVIOR = 0.5
	SEPARATIONCOEFFICIENT = 10.0
	VIEWDISTANCE = 30.0
	PLAYERCOMFORTZONE = 60.0
	KEEPERINBALLRANGE = 10.0
	BALLWITHINRECEIVINGRANGE = 10.0
	PLAYERKICKINGDISTANCE = 6.0
	PLAYERINTARGETRANGE = 10.0


	PLAYERMASS = 3.0
	PLAYERMAXFORCE = 1.0
	PLAYERMAXSPEEDWITHBALL = 1.2
	PLAYERMAXSPEEDWITHOUTBALL = 1.6
	PLAYERMAXTURNRATE = 0.4
	PLAYERSCALE = 1.0
	
class RegionData:
	HALFSIZE = 0
	NORMAL = 1

class MessageData:
	SEND_MSG_IMMEDIATELY = 0.0
	MSG_RECEIVEBALL = 0
	MSG_PASSTOME = 1
	MSG_SUPPORTATTACKER = 2
	MSG_GOHOME = 3
	MSG_WAIT = 4

class BehaviorType:
	NONE = 0x0000
	SEEK = 0x0001
	ARRIVE = 0x0002
	SEPARATION = 0x0004
	PURSUIT = 0x0008
	INTERPOSE = 0x0010
