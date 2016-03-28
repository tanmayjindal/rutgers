# Simulated Annealing simulation for hashing
# CS513 Assignment
# Tanmay Jindal

from random import randint
import random
import math

# k number of hash functions
# sizeKeys = size of universe
# sizeSet = number of values universe gets mapped to i.e. m
# time = the time simulated annealing runs
# hashes = hash function list with k number of functions

k = 20
sizeKeys = 12
sizeSet = 4
time = 3000

hashes = [[0 for y in xrange(sizeKeys)] for x in xrange(k)]

# Initialize the functions
def initialize():
    global hashes
    for i in xrange(k):
        for j in xrange(sizeKeys):
            hashes[i][j] = randint(1, sizeSet)
 
# Get the number of times an x-y pair clashes in the functions   
def numOfClashes(x, y, hashes):
    count = 0.0
    for i in xrange(k):
        if hashes[i][x] == hashes[i][y]:
            count += 1
    return count
 
# Get the x-y pair that clashes the most  
def clashingPair(hashes):
    maxClashes = 0
    pair = []
    for i in xrange(k):
        for x in xrange(sizeKeys):
            for y in xrange(x+1, sizeKeys):
                temp = numOfClashes(x, y, hashes)
                if temp > maxClashes:
                    maxClashes = temp
                    pair = [x,y]
    return [pair, maxClashes]
   
# Helper function to copy one set of hash functions to another 
def duplicateHashes(hashes):
    tempHashes = [[0 for y in xrange(sizeKeys)] for x in xrange(k)]
    for i in xrange(k):
        for j in xrange(sizeKeys):
            tempHashes[i][j] = hashes[i][j]
    return tempHashes
    
# Generating a neighbour for a given hash function. Hello neighbour!
def helloNeighbour(hashes):
    neighbour = duplicateHashes(hashes)
    clashInfo = clashingPair(neighbour)
    numClashes = clashInfo[1]
    clashPair = clashInfo[0]
    x = clashPair[0]
    y = clashPair[1]
    ratio = (numClashes * sizeSet) / k
    timer = 0
    while ratio > 1:
        for i in xrange(k):
            if neighbour[i][x] == neighbour[i][y]:
                temp = neighbour[i][y]
                while temp == neighbour[i][y]:
                    temp = randint(1, sizeSet)
                neighbour[i][y] = temp
        
        numClashes = numOfClashes(x, y, neighbour)
        ratio = (numClashes * sizeSet) / k
    return neighbour
    
# Calculate the cost of a hash function
def cost(hashes):
    totalClashes = 0
    
    for i in xrange(k):
        for x in xrange(sizeKeys):
            for y in xrange(x+1, sizeKeys):
                if x != y:
                    if hashes[i][x] == hashes[i][y]:
                        totalClashes += 1
    return totalClashes
    
# The simulated annealing cooling function
def cooling(cost, newCost, time):
    return math.exp((cost - newCost) / time)
    
# Simulated Annealing. Initialize, get cost, find neighbour, get neighbour's cost, decide whether to shift
def simAnnealing():
    global hashes, time
    currentCost = cost(hashes)
    newCost = 0
    
    initialize()
    
    print "Cost before annealing: ", cost(hashes)
    
    for t in xrange(time, 0, -1):
    
        currentCost = cost(hashes)
        candidate = helloNeighbour(hashes)
        newCost = cost(candidate)
        
    
        if newCost < currentCost:
            hashes = duplicateHashes(candidate)
        
        else:
            p = min(1, cooling(currentCost, newCost, t))
            switch = random.random()
            
            if switch < p:
                hashes = duplicateHashes(candidate)
                
    clashInfo = clashingPair(hashes)
    numClashes = clashInfo[1]
    c = numClashes * sizeSet / k

    print "Cost after annealing: ", newCost
    print "c value: ",c*1.0

# Main function that runs simulated annealing 5 times
def main():
    print "Running simulation for 5 times..."
    print "Current parameters are: k = %d time = 3000"%k
    
    for i in xrange(5):
        print "Simulation number:", i+1
        simAnnealing()

# Calling the main function
if __name__ == '__main__': main()                
                