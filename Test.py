#method that takes in config
#method for finding distance

#(Focal length * actual width of object) = (distance from camera * pixel width)
#F * W = D * P

import math

class mathing():
	D = 0.0
	F = 0.0
	W = 0.0
	P = 0.0
	D1 = 0.0
	
	#variable from dictionary
	x1 = (434,546)
	x2 = (31,245)
	
	def distance(self, x1, x2):
		self.P = math.sqrt((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2)	
	
	def input(self):
		self.D = float(input("Enter distance from camera in inches: "))
		self.W = float(input("Enter width of object: "))	
		
	def calculatefocal(self):
		self.F = ((self.D * self.P) / self.W)
	
	def calculatedistance(self):
		self.D1 = ((self.F * self.W)/ self.P)	

	def print(self):
		print("Input Distance", self.D)
		print("Input Width", self.W)
		print("Pixel Distance", self.P)
		print("Focal Length", self.F)
		
	#def __init__(self):


	
math1 = mathing()	
math1.distance(math1.x1, math1.x2)		
math1.input()	
math1.calculatefocal()
math1.calculatedistance()	
math1.print()
