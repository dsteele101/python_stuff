#Truck Problem
#50 Trucks can each travel 100 miles. There is a payload that can fit in one truck. If the trucks can exchange fuel and payload, how far can the payload travel? Note: trucks start in the same location.
from numpy import arange

#Number of trucks
n = 50
sum = 0

#Use harmonic progression to produce our solution (100/n)
for i in arange(1.0, n+1.0, 1):
	h = float(100.0/i)
	sum = sum + h
	print sum

print sum
