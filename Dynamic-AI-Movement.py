# --------------- Main Entry Begins Below -------------
from math import pi
import math
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

class Dynamic:
    print ("hello world") # TODO: figure out dynamic class

class Vector:
    # put function definitions here
    # two variables go here
    accel_x=0
    accel_z=0
    vector2D=np.array([accel_x, accel_z])

class Character0:
    char_id=0
    steering_behavior_code=0 
    #position=[0,0]
    position_x=0
    position_z=0   
    #velocity=[0,0]
    velocity_x=0
    velocity_z=0
    linear_x=0
    linear_z=0
    orientation=0 #in radians
    max_velocity=0
    max_acceleration=0
    target=0
    arrival_radius=0
    slowing_radius=0
    time=0.0
    collision_status=False

# Init the characters with their member variables
Character1 = Character0() # Character 1 is the target character
Character2 = Character0()
Character3 = Character0()
Character4 = Character0()

# Create character list for printing to file
charList=[Character1, Character2, Character3, Character4]

# Set the character steering behaviors
Character1.steering_behavior_code=1 # continue
Character2.steering_behavior_code=7 # flee
Character3.steering_behavior_code=3 # seek
Character4.steering_behavior_code=8 # arrive

# Set characters variables
# Character 1 init
Character1.postion_x=0
Character1.position_z=0
Character1.velocity_x=0
Character1.velocity_z=0
Character1.linear_x=0
Character1.linear_z=0
Character1.orientation=0
Character1.collision_status=False

# Character 2 init
Character2.position=np.array([-30,-50])
Character2.velocity=np.array([2,7])
Character2.orientation=pi/4
Character2.max_velocity=8
Character2.max_acceleration=1.5
Character2.target=1

# Character 3 init
Character3.position=np.array([-50,40])
Character3.velocity=np.array([0,8])
Character3.orientation=3*pi/2
Character3.max_velocity=8
Character3.max_acceleration=2
Character3.target=1

# Character 4 init
Character4.position=np.array([-50,40])
Character4.velocity=np.array([0,8])
Character4.orientation=3*pi/2
Character4.max_velocity=8
Character4.max_acceleration=2
Character4.target=1

#Steering Output
class SteeringOutput:
    linear: Vector #linear acceleration, 2D vector # linear is variable, vector is type
    angular: float   #angular acceleration, scalar

#Movement Update
def update(steering: SteeringOutput, maxSpeed: float, time: float):
    #Update the position and orientation
    position += velocity * time
    orientation += rotation * time
 
    #Update the velocity and rotation
    velocity += steering.linear * time
    rotation += steering.angular * time
 
    #Check for speed above max and clip
    if velocity.length() > maxSpeed:
        velocity.normalize()
        velocity *= maxSpeed

#Dynamic Seek
class Seek:
    character: Dynamic    #position and orientation for character
    target: Dynamic      #position and orientation for target
    max_acceleration: float  #maximum acceleration rate for character
    
    
    def getSteering() -> SteeringOutput():
        #Create output strcuture
        result = SteeringOutput()
 
        #Get the direction to the target
        result.linear = Character1.position - Character0.position # TODO
 
        #Accelerate at maximum rate
        result.linear.normalize()
        result.linear *= max_acceleration
        
        #Output steering
        result.angular = 0
        return result
    
class Continue():
    def getSteering():
        result = SteeringOutput()
        result.linear = Character1.position

# ------------ Output to .txt file -------------------
# Find user home directory and use relative path to place output in downloads folder
usr_home_dir=os.path.expanduser("~")
output_path_file=os.path.join(usr_home_dir, "Downloads", "TestOutput.txt")

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
                file.write(str(time) + ',' + str(Character1.char_id) + ',' +
                   str(Character1.position_x) + ',' + str(Character1.position_z) + ',' +
                   str(Character1.velocity_x) + ',' + str(Character1.velocity_z) + ',' + 
                   str(Character1.linear_x) + ',' + str(Character1.linear_z) + ',' +
                   str(Character1.orientation) + ',' + str(Character1.steering_behavior_code) + ',' + 
                   str(Character1.collision_status) + ',')