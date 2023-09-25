# --------------- Main Entry Begins Below -------------
from asyncio.windows_events import NULL
from math import e, pi
import math
import os
from pathlib import Path
from re import A
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
character1.char_id = 2601
character1.position = np.array([0.0,0.0])
character1.velocity = np.array([0.0,0.0])

# Character 2 init
character2.char_id = 2602
character2.position = np.array([-30.0,-50.0])
character2.velocity = np.array([2.0,7.0])
character2.orientation = pi / 4
character2.max_velocity = 8
character2.max_acceleration = 1.5
character2.target = 1

# Character 3 init
character3.char_id = 2603
character3.position = np.array([-50.0,40.0])
character3.velocity = np.array([0.0,8.0])
character3.orientation = 3 * pi / 2
character3.max_velocity = 8
character3.max_acceleration = 2
character3.target = 1

# Character 4 init
character4.char_id = 2604
character4.position = np.array([50.0,75.0])
character4.velocity = np.array([-9.0,4.0])
character4.orientation = pi
character4.max_velocity = 10
character4.max_acceleration = 2
character4.target = 1
character4.arrival_radius = 4
character4.slowing_radius = 32
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
class steeringOutput:
    linear: np.array
    angular: float
    def __init__(self, linear: np.array, angular: float):
        self.linear = linear
        self.angular = angular

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
        normalize(character.velocity)
        character.velocity *= character.maxVelocity

        
# Dynamic Flee
class flee:
    character: character0           # Position and orientation for character
    target: character0              # Position and orientation for target
    maxAcceleration: float  # Maximum acceleration rate for character
    def getsteering(self):
        # Create output structure
        result = steeringOutput()
        # Get the direction to the target
        result.linear = self.character.position = self.target.position
        # Accelerate at maximum rate
        normalize(result.linear)
        result.linear *= self.character.maxAcceleration
        # Output steering
        result.angular = 0
        return result

# Dynamic Seek
class seek:
    character: character0           # Position and orientation for character
    target: character0              # Position and orientation for target
    maxAcceleration: float          # Maximum acceleration rate for character
    def getSteering(self):
        # Create output strcuture
        result = steeringOutput() 
        # Get the direction to the target
        result.linear = self.target.position - self.character.position 
        # Accelerate at maximum rate
        normalize(result.linear)
        result.linear *= self.character.maxAcceleration        
        # Output steering
        result.angular = 0
        return result    

# Dynamic Arrive
class arrive:
    character: character0  # Position and orientation for character
    target: character0      # Position and orientation for target
    maxAcceleration: float  
    maxSpeed: float         
    targetRadius: float         # Arrival radius
    slowRadius: float           # Slowing-down radius
    timeToTarget: float = 0.1   # Time over which to achieve target speed
    def getSteering(self):
        result = steeringOutput()
        # Get the direction and distance to the target
        direction = self.target.position - self.character.position
        distance = length(direction)
        # Test for arrival
        if distance < self.character.targetRadius:
            return NULL
        # Outside slowing-down (outer) radius, move at max speed
        if distance > self.character.slowRadius:
            targetSpeed = self.character.maxSpeed
        # Between radii, scale speed to slow down
        else:
            targetSpeed = self.character.maxSpeed * distance / self.character.slowRadius
        # Target velocity combines speed and direction
        targetVelocity = direction
        normalize(targetVelocity)
        targetVelocity *= targetSpeed
        # Accelerate to target velocity
        result.linear = targetVelocity - self.character.velocity
        result.linear /= self.character.timeToTarget
        # Test for too fast acceleration
        if length(result.linear) > character.maxAcceleration:
            normalize(result.linear)
            result.linear *= self.character.maxAcceleration
        # Output steering
        result.angular = 0
        return result
        
class Continue:
    character1.position = np.array([0.0,0.0])
    def getSteering(self):
        result = steeringOutput()
        result.linear = character1.position
        return result

# ------------ Output to .txt file -------------------
# Find user home directory and use relative path to place output in downloads folder
usr_home_dir=os.path.expanduser("~")
output_path_file=os.path.join(usr_home_dir, "Downloads", "TestOutput.txt")

# Definition of starting time, ending time, and the step between each time
time=0
end_time=4
timestep=0.5

open(output_path_file, "w")
while (time <= end_time):
    with open(output_path_file, "a") as file:
        for character in charList:
            if character.steeringBehaviorCode == 1:
                steering = Continue#(character)
            elif character.steeringBehaviorCode == 6:
                steering = seek(character, character.target.position)
            elif character.steeringBehaviorCode == 7:
                steering = flee(character, character.target.positon)
            elif character.steeringBehaviorCode == 8:
                steering = arrive(character, character.target.position)
            character = update(character, timestep, steering)
            print(time, character.id, character.position[0], character.position[1], character.velocity[0], character.velocity[1], character.linear[0],
                  character.linear[1], character.orientation, character.steeringBehaviorCode, character.collisionStatus, sep = ", ", end = "\n", file = file)
    time = time+timestep