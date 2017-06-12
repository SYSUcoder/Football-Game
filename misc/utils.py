# -*- coding: UTF-8 -*-

import math
from Data import Data

def isEqual(oA, oB):
	if math.fabs(oA - oB) < 0.000000000001:
		return True
	else:
		return False