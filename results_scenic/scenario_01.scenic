
Town = "Town05"

param map = localPath(f'../maps/{Town}.xodr') 
param carla_map = Town
model scenic.simulators.carla.model
EGO_MODEL = "vehicle.lincoln.mkz_2017"

# Define behavior for other actors
behavior AccidentBehavior():
    wait

# Parameters for the scenario
ACCIDENT_DISTANCE = Range(50, 100)
ACCIDENT_LANE = Uniform(*network.lanes)

# Define the ego vehicle's starting point
egoLane = Uniform(*network.lanes)
egoTrajectory = egoLane.centerline
EgoSpawnPt = OrientedPoint on egoLane.centerline

# Define the ego vehicle
ego = Car at EgoSpawnPt,
    with rolename "hero",
    with regionContainedIn None,
    with blueprint EGO_MODEL

# Define other actors (e.g., accident vehicles)
AccidentSpawnPt = OrientedPoint following roadDirection from EgoSpawnPt for ACCIDENT_DISTANCE
AccidentVehicle1 = Car at AccidentSpawnPt,
    with heading AccidentSpawnPt.heading,
    with regionContainedIn None,
    with behavior AccidentBehavior()

AccidentVehicle2 = Car at AccidentSpawnPt offset along AccidentSpawnPt.heading by (5 @ 0),
    with heading AccidentSpawnPt.heading,
    with regionContainedIn None,
    with behavior AccidentBehavior()

# Additional setup for the scenario
require (distance from ego to AccidentVehicle1) > 0
require (distance from ego to AccidentVehicle2) > 0
