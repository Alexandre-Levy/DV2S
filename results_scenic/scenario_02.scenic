
Town = "Town05"

param map = localPath(f'../maps/{Town}.xodr') 
param carla_map = Town
model scenic.simulators.carla.model
EGO_MODEL = "vehicle.lincoln.mkz_2017"

# Define behavior for bicycles
behavior BicycleBehavior():
    do FollowLaneBehavior(target_speed=5)

# Parameters for the scenario
OPT_GEO_X_DISTANCE = Range(2, 8)
OPT_GEO_Y_DISTANCE = Range(-5, 15)

# Select a lane for the scenario
lane = Uniform(*network.lanes)
egoTrajectory = lane.centerline
EgoSpawnPt = OrientedPoint on lane.centerline

# Define the ego vehicle
ego = Car at EgoSpawnPt,
    with rolename "hero",
    with regionContainedIn None,
    with blueprint EGO_MODEL

# Define the bicycles
Bicycle1SpawnPt = OrientedPoint following roadDirection from EgoSpawnPt for 10
Bicycle1 = Bicycle at Bicycle1SpawnPt,
    with heading Bicycle1SpawnPt.heading,
    with behavior BicycleBehavior()

Bicycle2SpawnPt = OrientedPoint following roadDirection from Bicycle1SpawnPt for 5
Bicycle2 = Bicycle at Bicycle2SpawnPt,
    with heading Bicycle2SpawnPt.heading,
    with behavior BicycleBehavior()
