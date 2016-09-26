#method that takes in config
#method for finding distance

#(Focal length * actual width of object) = (distance from camera * pixel width)
#F * W = D * P

import math

#variable from dictionary
x1 = (434,546)
x2 = (31,245)


def distance(x1, x2):
	return math.sqrt((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2)	
	

D = float(input("Enter distance from camera in inches: "))
W = float(input("Enter width of object: "))	
	
P = distance(x1, x2)
F = ((D * P) / W)

"""def cdistance():
	P = distance(x1, x2)
	D1 = (( F * W)/ P)"""
	
D1 = (( F * W)/ P)	

print("Distance: ", D1)
print ("Set Distance: %.2f" % (P))
print("Width of object is: ", W)
print("Focal length is: %.2f " % (F))

#output the screen 