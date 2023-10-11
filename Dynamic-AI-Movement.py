# --------------- Main Entry Begins Below -------------
from asyncio.windows_events import NULL
from math import pi
import math
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Generic character definition
class character0:
    def __init__(self):
        self.id = 0
        self.steeringBehaviorCode = 0 
        self.position = np.array([0.0,0.0])
        self.velocity = np.array([0.0,0.0])
        self.linear = np.array([0.0,0.0])
        self.orientation = 0 #in radians
        self.maxVelocity = 0
        self.maxAcceleration = 0
        self.angular = 0
        self.target = 0
        self.arrivalRadius = 0
        self.slowingRadius = 0
        self.rotation = 0  
        self.collisionStatus = False

# Init the characters with their member variables
character1 = character0() # Character 1 is the target character
character2 = character0() # Character 2 flees from Character 1
character3 = character0() # Character 3 seeks Character 1
character4 = character0() # Character 4 arrives to character 1

# Create character list for printing to file
charList=[character1, character2, character3, character4]

# Set the character steering behaviors
character1.steeringBehaviorCode=1 # Continue
character2.steeringBehaviorCode=7 # Flee
character3.steeringBehaviorCode=6 # Seek
character4.steeringBehaviorCode=8 # Arrive

# Set characters variables
# Character 1 init
character1.id = 2601
character1.position = np.array([0.0,0.0])
character1.velocity = np.array([0.0,0.0])

# Character 2 init
character2.id = 2602
character2.position = np.array([-30.0,-50.0])
character2.velocity = np.array([2.0,7.0])
character2.orientation = pi / 4
character2.maxVelocity = 8
character2.maxAcceleration = 1.5
character2.target = character1

# Character 3 init
character3.id = 2603
character3.position = np.array([-50.0,40.0])
character3.velocity = np.array([0.0,8.0])
character3.orientation = 3 * pi / 2
character3.maxVelocity = 8
character3.maxAcceleration = 2
character3.target = character1

# Character 4 init
character4.id = 2604
character4.position = np.array([50.0,75.0])
character4.velocity = np.array([-9.0,4.0])
character4.orientation = pi
character4.maxVelocity = 10
character4.maxAcceleration = 2
character4.target = character1
character4.arrivalRadius = 4
character4.slowingRadius = 32
character4.timeToTarget = 1

# Helper Functions
# Length
def length(vector):
    length = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return length

# Normalize
def normalize(vector):
    vLength = length(vector)
    if vLength == 0:
        return vector
    result = np.array([vector[0]/vLength,vector[1]/vLength])
    return result

# Steering Output
class steeringOutput():
    def __init__(self):
        self.linear = np.array([0.0,0.0])
        self.angular = 0.0

# Movement Update
def update(character: character0, timestep: float, steering: steeringOutput):
    # Update the position and orientation
    character.position += character.velocity * timestep
    character.orientation += character.rotation * timestep
    # Update the velocity and rotation
    character.velocity += steering.linear * timestep
    character.rotation += steering.angular * timestep
    # Check for speed above max and clip
    if length(character.velocity) > character.maxVelocity:
        character.velocity = normalize(character.velocity)
        character.velocity *= character.maxVelocity
    character.linear = steering.linear
    return character

        
# Dynamic Flee
#class flee:
#   character: character0           # Position and orientation for character
#    target: character0              # Position and orientation for target
#    maxAcceleration: float  # Maximum acceleration rate for character
def getSteeringFlee(character, target):
    # Create output structure
    result = steeringOutput()
    # Get the direction to the target
    result.linear = character.position - target.position
    # Accelerate at maximum rate
    result.linear = normalize(result.linear)
    result.linear *= character.maxAcceleration
    # Output steering
    result.angular = 0
    return result

# Dynamic Seek
#class seek:
#    character: character0           # Position and orientation for character
#    target: character0              # Position and orientation for target
#    maxAcceleration: float          # Maximum acceleration rate for character
def getSteeringSeek(character, target):
    # Create output strcuture
    result = steeringOutput() 
    # Get the direction to the target
    result.linear = target.position - character.position 
    # Accelerate at maximum rate
    result.linear = normalize(result.linear)
    result.linear *= character.maxAcceleration        
    # Output steering
    result.angular = 0
    return result    

# Dynamic Arrive
#class arrive:
#    character: character0  # Position and orientation for character
#    target: character0      # Position and orientation for target
#    maxAcceleration: float  
#    maxSpeed: float         
#    targetRadius: float         # Arrival radius
#    slowRadius: float           # Slowing-down radius
#    timeToTarget: float = 0.1   # Time over which to achieve target speed
def getSteeringArrive(character, target):
    result = steeringOutput()
    # Get the direction and distance to the target
    direction = target.position - character.position
    distance = length(direction)
    # Test for arrival
    if distance < character.arrivalRadius:
            return result
    # Outside slowing-down (outer) radius, move at max speed
    if distance > character.slowingRadius:
        targetSpeed = character.maxVelocity
    # Between radii, scale speed to slow down
    else:
        targetSpeed = character.maxVelocity * distance / character.slowingRadius
    # Target velocity combines speed and direction
    targetVelocity = direction
    targetVelocity = normalize(targetVelocity)
    targetVelocity *= targetSpeed
    # Accelerate to target velocity
    result.linear = targetVelocity - character.velocity
    result.linear /= character.timeToTarget
    # Test for too fast acceleration
    if length(result.linear) > character.maxAcceleration:
        result.linear = normalize(result.linear)
        result.linear *= character.maxAcceleration
    # Output steering
    result.angular = 0
    return result
        
#class Continue:
    #character1.position = np.array([0.0,0.0])
def getSteeringContinue(character):
    result = steeringOutput()
    result.linear = character.linear
    return result

# ------------ Output to .txt file -------------------
# Find user home directory and use relative path to place output in downloads folder
usr_home_dir=os.path.expanduser("~")
output_path_file=os.path.join(usr_home_dir, "Desktop", "data.txt")

# Definition of starting time, ending time, and the step between each time
time=0
end_time=50
timestep=0.5

initialOpen = open(output_path_file, "w")
initialOpen.close()
while (time <= end_time):
    with open(output_path_file, "a") as file:
        for character in charList:
            print(time, character.id, character.position[0], character.position[1], character.velocity[0], character.velocity[1], character.linear[0],
                  character.linear[1], character.orientation, character.steeringBehaviorCode, character.collisionStatus, sep = ", ", end = "\n", file = file)
            if character.steeringBehaviorCode == 1:
                steering = getSteeringContinue(character)
            elif character.steeringBehaviorCode == 6:
                steering = getSteeringSeek(character, character.target)
            elif character.steeringBehaviorCode == 7:
                steering = getSteeringFlee(character, character.target)
            elif character.steeringBehaviorCode == 8:
                steering = getSteeringArrive(character, character.target)
            character = update(character, timestep, steering)
    time = time+timestep