# -*- coding: UTF-8 -*-

from FSM.State import *
from Messaging.Telegram import *
from Data import *
from V2D.Vector2D import *
from Messaging.MessageDispatcher import *

class Singleton(object):
	# 单例模式
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance

class GlobalKeeperState(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def OnMessage(self, oKeeper, tTelegram):
		if tTelegram == MessageData.MSG_GOHOME:
			oKeeper.SetDefaultHomeRegion()
			oKeeper.GetFSM().ChangeState(ReturnHome())
		elif tTelegram == MessageData.MSG_RECEIVEBALL:
			oKeeper.GetFSM().ChangeState(InterceptBall())

		return False

class TendGoal(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def Enter(self, oKeeper):
		oKeeper.Steering().InterposeOn(Params.GOALKEEPERTENDINGDISTANCE)

		oKeeper.Steering().SetTarget(oKeeper.GetRearInterposeTarget())

	def Execute(self, oKeeper):
		oKeeper.Steering().SetTarget(oKeeper.GetRearInterposeTarget())

		if oKeeper.BallWithinKeeperRange():
			oKeeper.Ball().Trap()
			oKeeper.Pitch().SetGoalKeeperHasBall(True)
			oKeeper.GetFSM().ChangeState(PutBallBackInPlay())
			return

		if oKeeper.BallWithinRangeForIntercept() and (not oKeeper.Team().InControl()):
			oKeeper.GetFSM().ChangeState(InterceptBall())

		if oKeeper.TooFarFromGoalMouth() and oKeeper.Team().InControl():
			oKeeper.GetFSM().ChangeState(ReturnHome())
			return

	def Exit(self, oKeeper):
		oKeeper.Steering().InterposeOff()

	def OnMessage(self, oKeeper, tTelegram):
		return False

class ReturnHome(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def Enter(self, oKeeper):
		oKeeper.Steering().ArriveOn()

	def Execute(self, oKeeper):
		oKeeper.Steering().SetTarget(oKeeper.HomeRegion().Center())

		if oKeeper.InHomeRegion() or (not oKeeper.Team().InControl()):
			oKeeper.GetFSM().ChangeState(TendGoal())

	def Exit(self, oKeeper):
		oKeeper.Steering().ArriveOff()

	def OnMessage(self, oKeeper, tTelegram):
		return False

class InterceptBall(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def Enter(self, oKeeper):
		oKeeper.Steering().PursuitOn()

		print "Goaly", oKeeper.ID(), "enters InterceptBall\n"

	def Execute(self, oKeeper):
		if oKeeper.TooFarFromGoalMouth() and (not oKeeper.isClosestPlayerOnPitchToBall()):
			oKeeper.GetFSM().ChangeState(ReturnHome())
			return

		if oKeeper.BallWithinKeeperRange():
			oKeeper.Ball().Trap()
			oKeeper.Pitch().SetGoalKeeperHasBall(True)
			oKeeper.GetFSM().ChangeState(PutBallBackInPlay())
			return

	def Exit(self, oKeeper):
		oKeeper.Steering().PursuitOff()

	def OnMessage(self, oKeeper, tTelegram):
		return False

class PutBallBackInPlay(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def Enter(self, oKeeper):
		oKeeper.Team().SetControllingPlayer(oKeeper)

		oKeeper.Team().Opponents().ReturnAllFieldPlayersToHome()
		oKeeper.Team().ReturnAllFieldPlayersToHome()

	def Execute(self, oKeeper):
		vBallTarget = Vector2D()

		tReceiverAndTarget = oKeeper.Team().FindPass(oKeeper,
			                       Params.MAXPASSINGFORCE, Params.GOALKEEPERMINPASSDISTANCE)
		
		if tReceiverAndTarget:
			oReceiver = tReceiverAndTarget[0]
			vBallTarget = tReceiverAndTarget[1]

			oKeeper.Ball().Kick(Vec2DNormalize(vBallTarget.Minus(oKeeper.Ball().Pos()) ),
			                    Params.MAXPASSINGFORCE)

			oKeeper.Pitch().SetGoalKeeperHasBall(False)

			MessageDispatcher().DispatchMsg(MessageData.SEND_MSG_IMMEDIATELY,
				                            oKeeper.ID(),
				                            oReceiver.ID(),
				                            MessageData.MSG_RECEIVEBALL,
				                            vBallTarget)

			oKeeper.GetFSM().ChangeState(TendGoal())
			return

		oKeeper.SetVelocity(Vector2D())

	def OnMessage(self, oKeeper, tTelegram):
		return False
