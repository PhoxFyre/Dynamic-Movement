# --------------- Main Entry Begins Below -------------
from asyncio.windows_events import NULL
from math import pi
import math
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# this class is likely unneeded.
class Dynamic:
    print ("hello world") # TODO: figure out dynamic class

# Definition of a vector
class vector:
    # put function definitions here
    # two variables go here
    accel_x=0
    accel_z=0
    vector2D=np.array([accel_x, accel_z])

# Generic character definition
class character0:
    char_id=0
    steering_behavior_code=0 
    position=[0,0]
    position_x=0
    position_z=0   
    velocity=np.array([0,0])
    velocity_x=0
    velocity_z=0
    linear_x=0
    linear_z=0
    orientation=0 #in radians
    max_velocity=0
    max_acceleration=0
    target=1
    arrival_radius=0
    slowing_radius=0
    time=0.0
    rotation=0
    collision_status=False

# Init the characters with their member variables
character1 = character0() # Character 1 is the target character
character2 = character0() # Character 2 flees from Character 1
character3 = character0() # Character 3 seeks Character 1
character4 = character0() # Character 4 arrives to character 1

# Create character list for printing to file
charList=[character1, character2, character3, character4]

# Set the character steering behaviors
character1.steering_behavior_code=1 # Continue
character2.steering_behavior_code=7 # Flee
character3.steering_behavior_code=3 # Seek
character4.steering_behavior_code=8 # Arrive

# Set characters variables
# Character 1 init
character1.char_id = 2601
character1.position = [0,0]
character1.velocity = np.array([0,0])

# Character 2 init
character2.char_id = 2602
character2.position = np.array([-30,-50])
character2.velocity = np.array([2,7])
character2.orientation = pi / 4
character2.max_velocity = 8
character2.max_acceleration = 1.5
character2.target = 1

# Character 3 init
character3.char_id = 2603
character3.position = np.array([-50,40])
character3.velocity = np.array([0,8])
character3.orientation = 3 * pi / 2
character3.max_velocity = 8
character3.max_acceleration = 2
character3.target = 1

# Character 4 init
character4.char_id = 2604
character4.position = np.array([50,75])
character4.velocity = np.array([-9,4])
character4.orientation = pi
character4.max_velocity = 10
character4.max_acceleration = 2
character4.target = 1
character4.arrival_radius = 4
character4.slowing_radius = 32
character4.timeToTarget = 1

# Steering Output
class steeringOutput:
    #linear=np.array([0,0])
    linear: vector   # Linear acceleration, 2D vector # linear is variable, vector is type
    angular: float   # Angular acceleration, scalar
    
# Movement Update
def update(steering: steeringOutput, maxSpeed: float, time: float):
    # Update the position and orientation
    character0.position += character0.velocity * time
    character0.orientation += character0.rotation * time
    # Update the velocity and rotation
    character0.velocity += steeringOutput.linear * time
    character0.rotation += steeringOutput.angular * time
    # Check for speed above max and clip
    if velocity.length() > maxSpeed:
        velocity.normalize()
        velocity *= maxSpeed

# Dynamic Flee
class flee:
    character: character2   # Position and orientation for character
    
    maxAcceleration: float  # Maximum acceleration rate for character
    def getsteering() -> steeringOutput():
        target=character1      # Position and orientation for target
        # Create output structure
        result = steeringOutput()
        # Get the direction to the target
        result.linear = character.position = target.position
        # Accelerate at maximum rate
        result.linear.normalize()
        result.linear *= character.maxAcceleration
        # Output steering
        result.angular = 0
        return result

# Dynamic Seek
class seek:
    character: character3           # Position and orientation for character
    # target: character1              # Position and orientation for target
    maxAcceleration: float          # Maximum acceleration rate for character
    
    def getSteering() -> steeringOutput():
        target = character1
        # Create output strcuture
        result = steeringOutput() 
        # Get the direction to the target
        result.linear = target.position - character.position 
        # Accelerate at maximum rate
        result.linear.normalize()
        result.linear *= character.maxAcceleration        
        # Output steering
        result.angular = 0
        return result    

# Dynamic Arrive
class arrive:
    character: character4   # Position and orientation for character
    target: character1      # Position and orientation for target
    maxAcceleration: float  
    maxSpeed: float         
    targetRadius: float         # Arrival radius
    slowRadius: float           # Slowing-down radius
    timeToTarget: float = 0.1   # Time over which to achieve target speed
    
    def getSteering() -> steeringOutput:
        result = steeringOutput()
        # Get the direction and distance to the target
        target=character1
        direction = target.position - character.position
        distance = direction.length()
        # Test for arrival
        if distance < character.targetRadius:
            return NULL
        # Outside slowing-down (outer) radius, move at max speed
        if distance > character.slowRadius:
            targetSpeed = character.maxSpeed
        # Between radii, scale speed to slow down
        else:
            targetSpeed = character.maxSpeed * distance / character.slowRadius
        # Target velocity combines speed and direction
        targetVelocity = direction
        targetVelocity.normalize()
        targetVelocity *= targetSpeed
        # Accelerate to target velocity
        result.linear = targetVelocity - character.velocity
        result.linear /= character.timeToTarget
        # Test for too fast acceleration
        if result.linear.length() > character.maxAcceleration:
            result.linear.normalize()
            result.linear *= character.maxAcceleration
        # Output steering
        result.angular = 0
        return result
        

class Continue:
    character1.position = np.array([0,0])
    def getSteering():
        result = steeringOutput()
        result.linear = character1.position

# ------------ Output to .txt file -------------------
# Find user home directory and use relative path to place output in downloads folder
usr_home_dir=os.path.expanduser("~")
output_path_file=os.path.join(usr_home_dir, "Downloads", "TestOutput.txt")

# Definition of starting time, ending time, and the step between each time
time=0
end_time=50
timestep=0.5

while (time < end_time):
    with open(output_path_file, "a") as file:
        time = timestep + time
        print("Current time: " + str(time))
        # TODO: 1 call the character's steering behavior
        for character in charList:
            if character.steering_behavior_code == 1:
                #file.write("hi\n")
                file.write(str(time) + ',' + str(character1.char_id) + ',' +
                   str(character1.position_x) + ',' + str(character1.position_z) + ',' +
                   str(character1.velocity_x) + ',' + str(character1.velocity_z) + ',' + 
                   str(character1.linear_x) + ',' + str(character1.linear_z) + ',' +
                   str(character1.orientation) + ',' + str(character1.steering_behavior_code) + ',' + 
                   str(character.collision_status) + ',')
        update(character1.position,steeringOutput, time)