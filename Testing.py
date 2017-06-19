# -*- coding: UTF-8 -*-
import copy
import time
import random

from Football.SoccerPitch import *

from misc.autolist import *

if __name__ == '__main__':
	oPitch = SoccerPitch(640, 480)

	for i in xrange(100):
		oPitch.Update()

	