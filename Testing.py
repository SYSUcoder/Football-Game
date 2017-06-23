# -*- coding: UTF-8 -*-
import copy
import time
import random

from misc.utils import *
from Football.SoccerPitch import *
from Football.FieldPlayer import *
from misc.autolist import *
from V2D.Vector2D import *
from Time.Regulator import *


if __name__ == '__main__':
	v1 = Vector2D(0, 1)
	v2 = Vector2D(-1, -1)

	print CalculateAngle(v2, v1)