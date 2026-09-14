# Description: The ego vehicle is turning left at an intersection; the adversarial pedestrian on the opposite sidewalk suddenly crosses the road from the right front.

Town = "Town05"

param map = localPath(f'../maps/{Town}.xodr') 
param carla_map = Town
model scenic.simulators.carla.model
EGO_MODEL = "vehicle.lincoln.mkz_2017"

behavior AdvBehavior():
    do CrossingBehavior(ego, OPT_ADV_SPEED, OPT_ADV_DISTANCE)
        
OPT_GEO_X_DISTANCE = Range(2, 8)
OPT_GEO_Y_DISTANCE = Range(-5, 15)
OPT_ADV_SPEED = Range(0, 5)
OPT_ADV_DISTANCE = Range(0, 15)
OPT_STOP_DISTANCE = Range(0, 1)

intersection = Uniform(*filter(lambda i: i.is4Way or i.is3Way, network.intersections))
egoManeuver = Uniform(*filter(lambda m: m.type is ManeuverType.LEFT_TURN, intersection.maneuvers))
egoInitLane = egoManeuver.startLane
egoTrajectory = egoInitLane.centerline
EgoSpawnPt = OrientedPoint on egoInitLane.centerline
ego = Car at EgoSpawnPt,
    with rolename "hero",
    with regionContainedIn None,
    with blueprint EGO_MODEL
    
IntSpawnPt = egoManeuver.endLane.centerline.start
SHIFT = OPT_GEO_X_DISTANCE @ OPT_GEO_Y_DISTANCE
AdvAgent = Pedestrian at IntSpawnPt offset along IntSpawnPt.heading by SHIFT,
    with heading IntSpawnPt.heading + 90 deg,
    with regionContainedIn None,
    with behavior AdvBehavior()
    
    
