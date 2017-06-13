# -*- coding: UTF-8 -*-

import math
import random
from Data import Data

def isEqual(oA, oB):
	if math.fabs(oA - oB) < 0.000000000001:
		return True
	else:
		return False

def RandomClamped():
	# 返回-1 < n < 1
	random.seed()
	return random.random() - random.random()

def RandInRange(fX, fY):
	random.seed()
	return fX + random.random()*(fY - fX)