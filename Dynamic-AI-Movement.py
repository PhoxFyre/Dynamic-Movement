# Names:
# Class: CS 330 -01
# Teacher: Jay Sebastian
# 9/9/2023
# Description: Program 1

# Revisions Log:

# --------------- Main Entry Begins Below -------------
from ast import Str
from math import pi
import os
from pathlib import Path
from tkinter import CHAR

# debug statement to verify file works
print ("Hello World!")
print("Nice to meet you!")

class Character0:
    sim_time=0
    char_id=0
    pos_x=0
    pos_y=0
    velocity_x=0
    velocity_y=0
    linear_x=0
    linear_y=0
    orientation=0
    steering_behavior_code=0 #continue
    collision_status=False
    
# steer, position, velocity, orientation, max.velocity, max.linear, target - mentioned in r code

# init the characters with their member variables
Character1 = Character0()
Character2 = Character0()
Character3 = Character0()
Character4 = Character0()

# Test print the character member variables 
# Seperate the characters by comma delimeter

Character1.steering_behavior_code=1
Character2.steering_behavior_code=7
Character3.steering_behavior_code=3
Character4.steering_behavior_code=8

print(Character1.steering_behavior_code, Character1.collision_status, Character1.sim_time, sep=',')
print(Character2.steering_behavior_code, Character2.collision_status, Character2.sim_time, sep=',')
print(Character3.steering_behavior_code, Character3.collision_status, Character3.sim_time, sep=',')
print(Character4.steering_behavior_code, Character4.collision_status, Character4.sim_time, sep=',')

# ------------ Output to .txt file test -------------------
# Find user home directory and use relative path to place output in downloads folder
usr_home_dir=os.path.expanduser("~")
output_path_file=os.path.join(usr_home_dir, "Downloads", "TestOutput.txt")
# Open an output file, say hello world and print character data
# NOTE: you must concatenate all variables and words to *one* string. file.write only allows for one arg
with open(output_path_file, "w") as file:
    file.write("Hello World\n")
    file.write("Char1 steering:" + str(Character1.steering_behavior_code) + "," + str(Character1.collision_status)+ "," 
               + str( Character1.sim_time) + "\n")
    file.write("Char2 steering:" + str(Character2.steering_behavior_code) + "," + str(Character2.collision_status)+ "," 
               + str( Character2.sim_time) + "\n")
    file.write("Char3 steering:" + str(Character3.steering_behavior_code) + "," + str(Character3.collision_status)+ "," 
               + str( Character3.sim_time) + "\n")
    file.write("Char4 steering:" + str(Character4.steering_behavior_code) + "," + str(Character4.collision_status)+ "," 
               + str( Character4.sim_time) + "\n")

# TODO: #SteeringOuput function
        # Character classes
        # Movement update function
        # Seek class
        # Flee class
        # Arrive class
        # Continue class

# General structure of the program?
# create generic character