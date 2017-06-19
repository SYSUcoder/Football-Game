# -*- coding: UTF-8 -*-

import random
from FSM.State import *
from Messaging.Telegram import *
from Data import *
from Messaging.MessageDispatcher import *
from V2D.Vector2D import *
from V2D.Transformations import *

class Singleton(object):
	# 单例模式
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance

class GlobalPlayerState(State, Singleton):
	def __init__(self):
		State.__init__(self)

	def Execute(self, oPlayer):
		if oPlayer.BallWithinReceivingRange() and oPlayer.isControllingPlayer():
			oPlayer.SetMaxSpeed(Params.PLAYERMAXSPEEDWITHBALL)
		else:
			oPlayer.SetMaxSpeed(Params.PLAYERMAXSPEEDWITHOUTBALL)

	def OnMessage(self, oPlayer, tTelegram):
		if tTelegram.Msg() == MessageData.MSG_RECEIVEBALL:
			oPlayer.Steering().SetTarget(tTelegram.Info() ) # 源码强制类型转换为Vector2D
			oPlayer.GetFSM().ChangeState(ReceiveBall())
			return True
		elif tTelegram.Msg() == MessageData.MSG_SUPPORTATTACKER:
			if oPlayer.GetFSM().isInState(SupportAttacker()):
				return True

			oPlayer.Steering().SetTarget(oPlayer.Team().GetSupportSpot())
			oPlayer.GetFSM().ChangeState(SupportAttacker())
			return True
		elif tTelegram.Msg() == MessageData.MSG_WAIT:
			oPlayer.GetFSM().ChangeState(Wait())
			return True
		elif tTelegram.Msg() == MessageData.MSG_GOHOME:
			oPlayer.SetDefaultHomeRegion()
			oPlayer.GetFSM().ChangeState(ReturnToHomeRegion())
			return True
		elif tTelegram.Msg() == MessageData.MSG_PASSTOME:
			oReceiver = tTelegram.Info()

			print "Player", oPlayer.ID(), "received request from", oReceiver.ID(), "to make pass\n"

			if oPlayer.Team().Receiver() != None or (not oPlayer.BallWithinKickingRange()):
				print "Player", oPlayer.ID(), "cannot make requested pass <cannot kick ball>\n"
				return True

			oPlayer.Ball().Kick(oReceiver.Pos().Minus(oPlayer.Ball().Pos()), Params.MAXPASSINGFORCE)

			print "Player", oPlayer.ID(), "Passed ball to requesting player\n"

			MessageDispatcher().DispatchMsg(MessageData.SEND_MSG_IMMEDIATELY,
				                            oPlayer.ID(),
				                            oReceiver.ID(),
				                            MessageData.MSG_RECEIVEBALL,
				                            oReceiver.Pos())

			oPlayer.GetFSM().ChangeState(Wait())
			oPlayer.FindSupport()

			return True

		return False

class ChaseBall(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def Enter(self, oPlayer):
		oPlayer.Steering().SeekOn()

		print "Player", oPlayer.ID(), "enters chase state\n"

	def Execute(self, oPlayer):
		if oPlayer.BallWithinKickingRange():
			oPlayer.GetFSM().ChangeState(KickBall())
			return

		if oPlayer.isClosestTeamMemberToBall():
			oPlayer.Steering().SetTarget(oPlayer.Ball().Pos())
			return

		oPlayer.GetFSM().ChangeState(ReturnToHomeRegion())

	def Exit(self, oPlayer):
		oPlayer.Steering().SeekOff()

	def OnMessage(self, oPlayer, tTelegram):
		return False

class SupportAttacker(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def Enter(self, oPlayer):
		oPlayer.Steering().ArriveOn()
		oPlayer.Steering().SetTarget(oPlayer.Team().GetSupportSpot())

		print "Player", oPlayer.ID(), "enters support state\n"

	def Execute(self, oPlayer):
		if not oPlayer.Team().InControl():
			oPlayer.GetFSM().ChangeState(ReturnToHomeRegion())
			return

		if oPlayer.Team().GetSupportSpot() != oPlayer.Steering().Target():
			oPlayer.Steering().SetTarget(oPlayer.Team().GetSupportSpot())
			oPlayer.Steering().ArriveOn()

		if oPlayer.Team().CanShoot(oPlayer.Pos(), Params.MAXPASSINGFORCE):
			oPlayer.Team().RequestPass(oPlayer)

		if oPlayer.AtTarget():
			oPlayer.Steering().ArriveOff()
			oPlayer.TrackBall()
			oPlayer.SetVelocity(Vector2D(0, 0))

			if not oPlayer.isThreatened():
				oPlayer.Team().RequestPass(oPlayer)

	def Exit(self, oPlayer):
		oPlayer.Team().SetSupportingPlayer(None)
		oPlayer.Steering().ArriveOff()

	def OnMessage(self, oPlayer, tTelegram):
		return False


class ReturnToHomeRegion(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def Enter(self, oPlayer):
		oPlayer.Steering().ArriveOn()

		if not oPlayer.HomeRegion().Inside(oPlayer.Steering().Target(), RegionData.HALFSIZE):
			oPlayer.Steering().SetTarget(oPlayer.HomeRegion().Center())

		print "Player", oPlayer.ID(), "enters ReturnToHome state\n"

	def Execute(self, oPlayer):
		if oPlayer.Pitch().GameOn():
			if oPlayer.isClosestTeamMemberToBall() and (
			   oPlayer.Team().Receiver() == None) and (
			   not oPlayer.Pitch().GoalKeeperHasBall()):

				oPlayer.GetFSM().ChangeState(ChaseBall())
				return

		if oPlayer.Pitch().GameOn() and oPlayer.HomeRegion().Inside(oPlayer.Pos(), RegionData.HALFSIZE):
			oPlayer.Steering().SetTarget(oPlayer.Pos())
			oPlayer.GetFSM().ChangeState(Wait())
		elif (not oPlayer.Pitch().GameOn()) and oPlayer.AtTarget():
			oPlayer.GetFSM().ChangeState(Wait())

	def Exit(self, oPlayer):
		oPlayer.Steering().ArriveOff()

	def OnMessage(self, oPlayer, tTelegram):
		return False


class Wait(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def Enter(self, oPlayer):
		print "Player", oPlayer.ID(), "enters wait state\n"

		if not oPlayer.Pitch().GameOn():
			oPlayer.Steering().SetTarget(oPlayer.HomeRegion().Center())

	def Execute(self, oPlayer):
		if not oPlayer.AtTarget():
			oPlayer.Steering().ArriveOn()
			return
		else:
			oPlayer.Steering().ArriveOff()
			oPlayer.SetVelocity(Vector2D(0, 0))
			oPlayer.TrackBall()

		if oPlayer.Team().InControl() and (
		   not oPlayer.isControllingPlayer()) and (
		   oPlayer.isAheadOfAttacker()):
			oPlayer.Team().RequestPass(oPlayer)
			return

		if oPlayer.Pitch().GameOn():
			if oPlayer.isClosestTeamMemberToBall() and (
			   oPlayer.Team().Receiver() == None) and (
			   not oPlayer.Pitch().GoalKeeperHasBall()):
				
				oPlayer.GetFSM().ChangeState(ChaseBall())
				return

	def Exit(self, oPlayer):
		return

	def OnMessage(self, oPlayer, tTelegram):
		return False


class KickBall(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def Enter(self, oPlayer):
		oPlayer.Team().SetControllingPlayer(oPlayer)
		if not oPlayer.isReadyForNextKick():
			oPlayer.GetFSM().ChangeState(ChaseBall())

		print "Player", oPlayer.ID(), "enters kick state\n"

	def Execute(self, oPlayer):
		vToBall = oPlayer.Ball().Pos().Minus(oPlayer.Pos())
		fDot = oPlayer.Heading().Dot(Vec2DNormalize(vToBall))

		if oPlayer.Team().Receiver() != None or (
		   oPlayer.Pitch().GoalKeeperHasBall()) or (
		   fDot < 0):

			print "Goaly has ball / ball behind player\n"

			oPlayer.GetFSM().ChangeState(ChaseBall())
			return

		vBallTarget = Vector2D()
		fPower = Params.MAXSHOOTINGFORCE * fDot

		if oPlayer.Team().CanShoot(oPlayer.Ball().Pos(), fPower, vBallTarget) or (
		   random.random() < Params.CHANCEPLAYERATTEMPTSPOTSHOT):
			print "Player", oPlayer.ID(), "attempts a shot at", vBallTarget

			vBallTarget = AddNoiseToKick(oPlayer.Ball().Pos(), vBallTarget)
			vKickDirection = vBallTarget.Minus(oPlayer.Ball().Pos())
			oPlayer.Ball().Kick(vKickDirection, fPower)

			oPlayer.GetFSM().ChangeState(Wait())
			oPlayer.FindSupport()
			return

		oReceiver = None
		fPower = Params.MAXPASSINGFORCE * fDot

		if oPlayer.isThreatened() and oPlayer.Team().FindPass(oPlayer,
															  oReceiver,
															  vBallTarget,
															  fPower,
															  Params.MINPASSDIST):
			vBallTarget = AddNoiseToKick(oPlayer.Ball().Pos(), vBallTarget)
			vKickDirection = vBallTarget.Minus(oPlayer.Ball().Pos())
			oPlayer.Ball().Kick(vKickDirection, fPower)

			print "Player", oPlayer.ID(), "passes the ball with force", fPower,
			print "to player", oReceiver.ID(), "Target is", vBallTarget

			MessageDispatcher().DispatchMsg(MessageData.SEND_MSG_IMMEDIATELY,
											oPlayer.ID(),
											oReceiver.ID(),
											MessageData.MSG_RECEIVEBALL,
											vBallTarget)

			oPlayer.GetFSM().ChangeState(Wait())
			oPlayer.FindSupport()
			return
		else:
			oPlayer.FindSupport()
			oPlayer.GetFSM().ChangeState(Dribble())

	def OnMessage(self, oPlayer, tTelegram):
		return False


class Dribble(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def Enter(self, oPlayer):
		oPlayer.Team().SetControllingPlayer(oPlayer)

		print "Player", oPlayer.ID(), "enters dribble state"

	def Execute(self, oPlayer):
		fDot = oPlayer.Team().HomeGoal().Facing().Dot(oPlayer.Heading())
		if fDot < 0:
			vDirection = oPlayer.Heading()
			fAngle = Data.PI / 4 * -1 * oPlayer.Team().HomeGoal().Facing().Sign(oPlayer.Heading())

			Vec2DRotateAroundOrigin(vDirection, fAngle)
			fKickingForce = 0.8

			oPlayer.Ball().Kick(vDirection, fKickingForce)
		else:
			oPlayer.Ball().Kick(oPlayer.Team().HomeGoal().Facing(), Params.MAXDRIBBLEFORCE)

		oPlayer.GetFSM().ChangeState(ChaseBall())
		return

	def OnMessage(self, oPlayer, tTelegram):
		return False


class ReceiveBall(State, Singleton):
	def __init__(self):
		State.__init__(self)
		return

	def Enter(self, oPlayer):
		oPlayer.Team().SetReceiver(oPlayer)
		oPlayer.Team().SetControllingPlayer(oPlayer)

		fPassThreatRadius = 70.0

		if (oPlayer.InHotRegion() or random.random() < Params.CHANCEOFUSINGARRIVETYPERECEIVEBEHAVIOR) and (
			not oPlayer.Team().isOpponentWithinRadius(oPlayer.Pos(), fPassThreatRadius)):
			
			oPlayer.Steering().ArriveOn()

			print "Player", oPlayer.ID(), "enters receive state (Using Arrive)"
		else:
			oPlayer.Steering().PursuitOn()

			print "Player", oPlayer.ID(), "enters receive state (Using Pursuit)"

	def Execute(self, oPlayer):
		if oPlayer.BallWithinReceivingRange() or (not oPlayer.Team().InControl()):
			oPlayer.GetFSM().ChangeState(ChaseBall())
			return

		if oPlayer.Steering().PursuitOn():
			oPlayer.Steering().SetTarget(oPlayer.Ball().Pos())

		if oPlayer.AtTarget():
			oPlayer.Steering().ArriveOff()
			oPlayer.Steering().PursuitOff()
			oPlayer.TrackBall()
			oPlayer.SetVelocity(Vector2D(0, 0))

	def Exit(self, oPlayer):
		oPlayer.Steering().ArriveOff()
		oPlayer.Steering().PursuitOff()

		oPlayer.Team().SetReceiver(None)

	def OnMessage(self, oPlayer, tTelegram):
		return False