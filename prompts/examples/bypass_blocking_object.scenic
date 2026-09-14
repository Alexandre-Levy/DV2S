# Description: Ego-vehicle must go around a blocking object using the opposite lane, yielding to oncoming traffic.

Town = 'Town07'
param map = localPath(f'../maps/{Town}.xodr') 
model scenic.simulators.carla.model


#CONSTANTS
ONCOMING_THROTTLE = 0.6
EGO_SPEED = 7
ONCOMING_CAR_SPEED = 10
DIST_THRESHOLD = 13
YIELD_THRESHOLD = 5
BLOCKING_CAR_DIST = Range(15, 20)
BREAK_INTENSITY = 0.8
BYPASS_DIST = 5
DIST_BTW_BLOCKING_ONCOMING_CARS = 10
DIST_TO_INTERSECTION = 15

behavior EgoBehavior(path):
	current_lane = network.laneAt(self)
	laneChangeCompleted = False
	bypassed = False

	try:
		do FollowLaneBehavior(EGO_SPEED, laneToFollow=current_lane)

	interrupt when (distance to blockingCar) < DIST_THRESHOLD and not laneChangeCompleted:
		if ego can see oncomingCar:
			take SetBrakeAction(BREAK_INTENSITY)
		elif (distance to oncomingCar) > YIELD_THRESHOLD:
			do LaneChangeBehavior(path, is_oppositeTraffic=True, target_speed=EGO_SPEED)
			do FollowLaneBehavior(EGO_SPEED, is_oppositeTraffic=True) until (distance to blockingCar) > BYPASS_DIST
			laneChangeCompleted = True
		else:
			wait

	interrupt when (blockingCar can see ego) and (distance to blockingCar) > BYPASS_DIST and not bypassed:
		current_laneSection = network.laneSectionAt(self)
		rightLaneSec = current_laneSection._laneToLeft
		do LaneChangeBehavior(rightLaneSec, is_oppositeTraffic=False, target_speed=EGO_SPEED)
		bypassed = True


behavior OncomingCarBehavior(path = []):
	do FollowLaneBehavior(ONCOMING_CAR_SPEED)

laneSecsWithLeftLane = []
for lane in network.lanes:
	for laneSec in lane.sections:
		if laneSec._laneToLeft is not None:
			if laneSec._laneToLeft.isForward is not laneSec.isForward:
				laneSecsWithLeftLane.append(laneSec)

assert len(laneSecsWithLeftLane) > 0, \
	'No lane sections with adjacent left lane with opposing \
	traffic direction in network.'

initLaneSec = Uniform(*laneSecsWithLeftLane)
leftLaneSec = initLaneSec._laneToLeft

spawnPt = OrientedPoint on initLaneSec.centerline

oncomingCar = Car on leftLaneSec.centerline,
	with behavior OncomingCarBehavior()

ego = Car at spawnPt,
	with behavior EgoBehavior(leftLaneSec)
	
blockingCar = Car following roadDirection from ego for BLOCKING_CAR_DIST,
				with viewAngle 90 deg

require blockingCar can see oncomingCar
require (distance from blockingCar to oncomingCar) < DIST_BTW_BLOCKING_ONCOMING_CARS
require (distance from blockingCar to intersection) > DIST_TO_INTERSECTION
