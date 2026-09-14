# Description: The ego vehicle is driving on a straight road; the adversarial pedestrain stands behind a bus stop on the right front, then suddenly sprints out onto the road in front of the ego vehicle.

Town = "Town05"

param map = localPath(f'../maps/{Town}.xodr') 
param carla_map = Town
model scenic.simulators.carla.model
EGO_MODEL = "vehicle.lincoln.mkz_2017"

behavior AdvBehavior():
    do CrossingBehavior(ego, OPT_ADV_SPEED, OPT_ADV_DISTANCE)


OPT_GEO_BLOCKER_X_DISTANCE = Range(2, 8)
OPT_GEO_BLOCKER_Y_DISTANCE = Range(15, 50)
OPT_GEO_X_DISTANCE = Range(-2, 2)
OPT_GEO_Y_DISTANCE = Range(2, 6)
OPT_ADV_SPEED = Range(0, 5)
OPT_ADV_DISTANCE = Range(8, 15)
OPT_STOP_DISTANCE = Range(0, 1)

lane = Uniform(*network.lanes)
egoTrajectory = lane.centerline
EgoSpawnPt = OrientedPoint on lane.centerline
ego = Car at EgoSpawnPt,
    with rolename "hero",
    with regionContainedIn None,
    with blueprint EGO_MODEL
    
IntSpawnPt = OrientedPoint following roadDirection from EgoSpawnPt for OPT_GEO_BLOCKER_Y_DISTANCE
Blocker = BusStop right of IntSpawnPt by OPT_GEO_BLOCKER_X_DISTANCE,
    with heading IntSpawnPt.heading,
    with regionContainedIn None

# pedestrian (right to left)
SHIFT = OPT_GEO_X_DISTANCE @ OPT_GEO_Y_DISTANCE
AdvAgent = Pedestrian at Blocker offset along IntSpawnPt.heading by SHIFT,
    with heading IntSpawnPt.heading + 90 deg,
    with regionContainedIn None,
    with behavior AdvBehavior()
