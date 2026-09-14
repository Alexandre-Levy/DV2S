
Town = "Town05"

param map = localPath(f'../maps/{Town}.xodr') 
param carla_map = Town
model scenic.simulators.carla.model
EGO_MODEL = "vehicle.lincoln.mkz_2017"

behavior PedestrianBehavior():
    do CrossingBehavior(ego, OPT_PED_SPEED, OPT_PED_DISTANCE)

# Parameters for the scenario
OPT_PED_SPEED = Range(0, 5)
OPT_PED_DISTANCE = Range(8, 15)
OPT_GEO_X_DISTANCE = Range(2, 8)
OPT_GEO_Y_DISTANCE = Range(2, 6)
OPT_BLOCKER_X_DISTANCE = Range(2, 8)
OPT_BLOCKER_Y_DISTANCE = Range(15, 50)

# Select a lane for the ego vehicle
lane = Uniform(*network.lanes)
egoTrajectory = lane.centerline
EgoSpawnPt = OrientedPoint on lane.centerline

# Define the ego vehicle
ego = Car at EgoSpawnPt,
    with rolename "hero",
    with regionContainedIn None,
    with blueprint EGO_MODEL

# Define the position of the bus stop as a blocker
IntSpawnPt = OrientedPoint following roadDirection from EgoSpawnPt for OPT_BLOCKER_Y_DISTANCE
Blocker = BusStop right of IntSpawnPt by OPT_BLOCKER_X_DISTANCE,
    with heading IntSpawnPt.heading,
    with regionContainedIn None

# Define the pedestrian, offset from the bus stop
SHIFT = OPT_GEO_X_DISTANCE @ OPT_GEO_Y_DISTANCE
pedestrian = Pedestrian at Blocker offset along IntSpawnPt.heading by SHIFT,
    with heading IntSpawnPt.heading + 90 deg,
    with regionContainedIn None,
    with behavior PedestrianBehavior()

# Define a parked car near the bus stop
parkedCar = Car at Blocker offset along IntSpawnPt.heading by (OPT_GEO_X_DISTANCE, -OPT_GEO_Y_DISTANCE),
    with heading IntSpawnPt.heading,
    with regionContainedIn None
