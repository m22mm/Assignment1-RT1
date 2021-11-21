from __future__ import print_function

import time
from sr.robot import *


a_th = 6.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

obstacle_dist=0.6


R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
   	
def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	  	
def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	
def grab_and_move():
	"""
	Function for the robot to grab and move a token behind it
    
	"""
	print("Found it!")
	if R.grab(): # the robot grabs the token
		print("The robot has grabbed the silver token!")
		turn(20,3)
		R.release()
		drive(-9,2)
		turn(-20,3)
	
def adjust(rot_y):
	"""
	Function to adjust the orientation of the robot with the token
	
	"""
	if rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-6, 0.5)
	elif rot_y > a_th:	# if the robot is not well aligned with the token, we move it on the left or on the right
		print("Right a bit...")
		turn(6, 0.5)
		
def turn_direction(x):
	"""
	Function to detect to which direction to turn the robot in case a golden token is 		detected 
	
	"""
	
	r=100
	l=100
	for token in R.see():
		if token.info.marker_type is MARKER_TOKEN_GOLD: #if the detected token is gold
			dist=token.dist
	    		rot_y=token.rot_y
			if 75<=rot_y<=105:
				if dist<r:
					r=dist
			elif -105<=rot_y<=-75:
				if dist<l:
					l=dist
	if l<r: # if the distance of the obstacle from the left is < the distance of the obstacle from the right, turn right
		turn(x,0.5)
		print("Turning Right")
	elif l>r: # if the distance of the obstacle from the right is < the distance of the obstacle from the left, turn left
		turn(-x,0.5)
		print("Turning Left")
	
		
while 1:
	drive(22,0.2)
	silver_dist, silver_rot_y = find_silver_token()
	golden_dist, golden_rot_y = find_golden_token()
	if golden_dist > obstacle_dist: # far from golden token
		if silver_dist <= 1.5 and abs(silver_rot_y)<130: # close to silver token
			if -a_th<=silver_rot_y<=a_th: # robot well aligned with silver token
				if silver_dist <= d_th:
					grab_and_move()
			else:
				adjust(silver_rot_y)
					
	elif golden_dist < obstacle_dist and abs(golden_rot_y)<25: # close to golden token
		if silver_dist <= 1.5 and abs(silver_rot_y)<130: # close to silver token
			if -a_th<=silver_rot_y<=a_th: # robot well aligned with silver token
				if silver_dist <= d_th:
					grab_and_move()
			else:
				adjust(silver_rot_y)
		else:
			turn_direction(65)
	elif golden_dist < obstacle_dist and abs(golden_rot_y)<75: # close to golden token from the side
		if silver_dist <= 1.5 and abs(silver_rot_y)<130: # close to silver token
			if -a_th<=silver_rot_y<=a_th: # robot well aligned with silver token
				if silver_dist <= d_th:
					grab_and_move()
			else:
				adjust(silver_rot_y)
		else:
			turn_direction(20)