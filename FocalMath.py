#method that takes in config
#method for finding distance

#(Focal length * actual width of object) = (distance from camera * pixel width)
#F * W = D * P

import math

#Distance from camera to object (For calibration)
#D = 0.0
#Focal length of camera (Calculated from calibration)
#F = 0.0
#Actual width of object (User input)
#W = 0.0
#Percieved width(User input)
#P = 0.0
#Distance from camera to object (For images)
#D1 = 0.0

def distance(point1, point2):
	P = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
	return P

def calculatefocal(D, P, W):
	F = ((float(D) * float(P)) / float(W))
	return F

def calculatedistance(F, W, P):
	D1 = ((float(F) * float(W))/ float(P))
	return D1
