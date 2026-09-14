# Description: The ego vehicle, a large station wagon, attempts a left turn from a parking lot onto a busy southbound highway and gets struck on its left side by an oncoming pickup truck approaching in the right lane. The impact results in a secondary collision as the ego car spins and receives another hit on its side. Both vehicles are severely damaged, and all occupants sustain various injuries. The ego vehicle should have waited for a clear path before turning.

Town = 'Town10HD'
param map = localPath(f'../maps/{Town}.xodr') 
param carla_map = Town
model scenic.simulators.carla.model
EGO_MODEL = "vehicle.lincoln.mkz_2017"

# Define parameters for the scenario
OPT_ADV_SPEED = Range(0, 5)
OPT_ADV_DISTANCE = Range(0, 15)
OPT_STOP_DISTANCE = Range(0, 1)



scenario ParkedCar(gap=3.0):
    setup:
        parkedCarfront = Car ahead of ego by gap
        parkedCarback = Car behind ego by gap

scenario destroyCar(vehicle):
    setup:
        leadCar = vehicle
        SHIFT = -1000 @ -1000
        newpos = OrientedPoint offset along ego.heading by SHIFT
        leadCar.setPosition(newpos, 0)
        terminate after 1 seconds
    
scenario waitDistancedEgo(vehicle):
    setup:
        leadCar = vehicle
    compose:
        while (distance from ego to vehicle) < 50:
            wait
        do destroyCar(vehicle)

scenario CarFlows(gap=3.0):   
    compose:
        flow = laneFlow()
        do flow until (distance from ego to flow.leadCar) < 5
        
        carflow = CarFlows(5)
        
        # flow2 = laneFlow(flow.leadCar)
        # do flow2 until (distance from ego to flow.leadCar) > 50
        comeb = waitDistancedEgo(flow.leadCar)
        do comeb, carflow
       


scenario laneFlow(vehicle=None):
    setup:
        if vehicle:
            leadCar = vehicle
            # SHIFT = -1000 @ -1000
            # newpos = OrientedPoint offset along ego.heading by SHIFT
            # leadCar.setPosition(newpos, 0)
        else:
            SHIFT = -3 @ 0
            newpos = OrientedPoint offset along ego.heading by SHIFT
            posbehind = OrientedPoint following network.laneSectionAt(newpos).lane.orientation from newpos for -10
            leadCar = Car at posbehind,
                with regionContainedIn None,
                with behavior AutopilotBehavior()
scenario Main():
    setup:
        laneSecsWithRightLane = []
        for lane in network.lanes:
            laneGroup = lane.group
            if laneGroup._shoulder is not None and laneGroup._sidewalk is not None:
                    laneSecsWithRightLane.append(laneGroup.shoulder)
        lane = Uniform(*laneSecsWithRightLane)  

        roadDirection = lane.orientation
        # Ego trajectory follows the centerline of the lane and respects traffic flow
        EgoTrajectory = lane.centerline

        # Spawn point for ego vehicle, aligned with the lane's centerline and traffic direction
        EgoSpawnPt = OrientedPoint on lane.centerline

        # Define the ego vehicle, starting at the spawn point, and ensuring it follows the road
        ego = Car at EgoSpawnPt,
    with rolename "hero",
            with heading EgoSpawnPt.heading,
            with blueprint EGO_MODEL
        
    compose:
        subScenario = ParkedCar(5)
        carflow = CarFlows(5)
        do subScenario, carflow
