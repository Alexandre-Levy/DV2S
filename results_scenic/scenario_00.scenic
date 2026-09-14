
Town = "Town05"

param map = localPath(f'../maps/{Town}.xodr') 
param carla_map = Town
model scenic.simulators.carla.model
EGO_MODEL = "vehicle.lincoln.mkz_2017"

# Define behavior for other vehicles
behavior SurroundingCarBehavior():
    do FollowLaneBehavior(target_speed=Range(20, 30))

# Parameters for the scenario
OPT_GEO_X_DISTANCE = Range(-2, 2)
OPT_GEO_Y_DISTANCE = Range(5, 10)

# Select a lane for the ego vehicle
lane = Uniform(*network.lanes)
egoTrajectory = lane.centerline
EgoSpawnPt = OrientedPoint on lane.centerline

# Define the ego vehicle
ego = Car at EgoSpawnPt,
    with rolename "hero",
    with regionContainedIn None,
    with blueprint EGO_MODEL

# Define surrounding vehicles
SHIFT_FRONT = OPT_GEO_X_DISTANCE @ OPT_GEO_Y_DISTANCE
frontCar = Car at EgoSpawnPt offset along EgoSpawnPt.heading by SHIFT_FRONT,
    with behavior SurroundingCarBehavior()

SHIFT_BACK = OPT_GEO_X_DISTANCE @ -OPT_GEO_Y_DISTANCE
backCar = Car at EgoSpawnPt offset along EgoSpawnPt.heading by SHIFT_BACK,
    with behavior SurroundingCarBehavior()

SHIFT_LEFT = -OPT_GEO_Y_DISTANCE @ OPT_GEO_X_DISTANCE
leftCar = Car at EgoSpawnPt offset along EgoSpawnPt.heading by SHIFT_LEFT,
    with behavior SurroundingCarBehavior()

SHIFT_RIGHT = OPT_GEO_Y_DISTANCE @ OPT_GEO_X_DISTANCE
rightCar = Car at EgoSpawnPt offset along EgoSpawnPt.heading by SHIFT_RIGHT,
    with behavior SurroundingCarBehavior()
