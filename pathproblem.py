from __future__ import print_function
import util
import math
import show_map
from ast import literal_eval
import sys

#name = string, x,y = latitude, longitude of the node, adjNodeName = list of names of nodes that are adjacent to the node, 
# 
class Node:
    def __init__(self, name, location, adjNodeName, crimeOccurrence, crimeList): 
        self.name, self.location, self.adjNodeName, self.crimeOccurrence, self.crimeList = name, location, adjNodeName, crimeOccurrence, crimeList

    def __str__(self):
        return str(self.name) + ',' + str(self.location) + ',' + str(self.adjNodeName) + ',' + str(self.crimeOccurrence) + ',' + str(self.crimeList)


def dist(a,b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] -b[1])**2)

def tupleToString(streetTuple):
    return '(' + streetTuple[0] + ',' + streetTuple[1] + ')' 

#name to Node map: returns Node object when called by NodeMap[name]
class PathProblem(util.SearchProblem):
    def __init__(self, startStateName, endStateName, NodeMap, gaussianTrue, penalty_constant): self.start, self.end, self.NodeMap, self.gaussianTrue, self.penalty_constant \
                                                                                                = startStateName, endStateName, NodeMap, gaussianTrue, penalty_constant
    def startState(self): return self.start
    def isGoal(self, state): return state == self.end
    def succAndCost(self, state):
        #penalty_constant = 0.001
        sigma = 0.001625   #Average distance of a block
        results = []
        for adjNode in self.NodeMap[state].adjNodeName:
            if adjNode not in self.NodeMap: continue
            if dist(self.NodeMap[state].location, self.NodeMap[adjNode].location) > 0.005: continue
            
            #Gaussian filtering - used as default
            #crime_penalty = 0
            #node_location = self.NodeMap[state].location
            #for value in self.NodeMap[adjNode].crimeList.values():
            #    for x in value:
            #        crime_penalty = crime_penalty + penalty_constant * math.exp(- (dist(node_location, x)**2) / (2 * sigma ** 2) )
            
            #Linear penalty
            if self.gaussianTrue == 0:
                crime_penalty = self.penalty_constant * sum(self.NodeMap[adjNode].crimeOccurrence.values())
            else:
                crime_penalty = 0
                node_location = self.NodeMap[state].location
                for value in self.NodeMap[adjNode].crimeList.values():
                    for x in value:
                        crime_penalty = crime_penalty + self.penalty_constant * math.exp(- (dist(node_location, x)**2) / (2 * sigma ** 2) )
            
            #Without A* enhancement
            #results.append((tupleToString(state)+'->'+ tupleToString(adjNode), adjNode, dist(self.NodeMap[state].location, self.NodeMap[adjNode].location)))
            
            #A* cost - using Euclidean as heuristic h - used as default
            #results.append(( tupleToString(state)+'->'+ tupleToString(adjNode), adjNode, crime_penalty + dist(self.NodeMap[state].location, self.NodeMap[adjNode].location) + dist(self.NodeMap[adjNode].location, self.NodeMap[self.end].location) - dist(self.NodeMap[state].location, self.NodeMap[self.end].location)))
            
            #printing out in x_loc, y_loc for show_map.py usage --> will become a google map!
            results.append(( self.NodeMap[state].location, adjNode, crime_penalty + dist(self.NodeMap[state].location, self.NodeMap[adjNode].location) + dist(self.NodeMap[adjNode].location, self.NodeMap[self.end].location) - dist(self.NodeMap[state].location, self.NodeMap[self.end].location)))
        return results

#Makes crime map: key is (x_loc, y_loc), value is crime type
def makeCrimeMap():
    inputfile = open('../train.csv', 'r')
    crimeMap = {}
    
    count = 0
    for line in inputfile.readlines():
        if count == 0:
            count += 1
            continue
        lined = line.split('"')
        if len(lined) > 1:
            lined[1] = lined[1].replace(',', '')
        data = ''.join(lined).split(',')
        if (len(data) == 9):
            crime_type = data[1]

            loc_key = (float(data[8].strip(' ')), float(data[7].strip(' ')))
            crimeMap[loc_key] = crime_type
    
    #print crimeMap
    return crimeMap

def makeCrimeLocs(x_loc, y_loc, xpm, ypm, crimeMap):
    crimeLocs = {}
    for key in crimeMap.keys():
        if key[0] > x_loc - xpm and key[0] < x_loc + xpm and key[1] > y_loc - ypm and key[1] < y_loc + ypm:
            if crimeMap[key] in crimeLocs:
                crimeLocs[crimeMap[key]].append(key)
            else:
                crimeLocs[crimeMap[key]] = []
                crimeLocs[crimeMap[key]].append(key)
    
    return crimeLocs

#Makes crime dictionary: key is the type of the crime, value is the occurrence, in square range
def makeCrimeOccurrence(x_loc, y_loc, xpm, ypm, crimeMap):
    crimeOccurrence = {}
    for key in crimeMap.keys():
        if key[0] > x_loc - xpm and key[0] < x_loc + xpm and key[1] > y_loc - ypm and key[1] < y_loc + ypm:
            if crimeMap[key] in crimeOccurrence:
                crimeOccurrence[crimeMap[key]] += 1
            else:
                crimeOccurrence[crimeMap[key]] = 1
                
    #print crime_dict
    return crimeOccurrence

#Function that makes NodeMapList that contains all required information regards nodes - called only once to produce 'NodeMapList.csv'
def process():
    inputFile = open('traffic_result.csv', 'r')
    NodeMap = {}
    result = {}
    crimeMap = makeCrimeMap()

    for line in inputFile.readlines():
        if line[0]==',': continue
    
        s1 = line.split('|')[0].split(',')
        sKey = (s1[1], s1[2])
        
        s2 = line.split('|')[-1].split(',')
        latLng = (float(s2[-2]), float(s2[-1].replace('\n','')))

        adjacentList = []
        for x, y in zip(*[iter(s2[0:-2])]*2):
            x = x.replace('"', '')
            y = y.replace('"', '')
            adjacentList.append((x.strip(), y.strip()))
        #NodeMap[sKey] = Node(sKey, latLng, adjacentList)
        crimeOcc = makeCrimeOccurrence(latLng[0], latLng[1], 0.00325016538, 0.00325016538, crimeMap)
        crimeLocs = makeCrimeLocs(latLng[0], latLng[1], 0.00325016538, 0.00325016538, crimeMap)
        NodeMap[sKey] = Node(sKey, latLng, adjacentList, crimeOcc, crimeLocs)

    outputFile = open('NodeMapList.csv', 'w')
    for sKey, node in NodeMap.iteritems():
        line = str(node.name) + '|' + str(node.location) + '|' + str(node.adjNodeName) + '|' + str(node.crimeOccurrence) + '|' + str(node.crimeList) + '\n'
        print(line)
        outputFile.write(line)
    outputFile.close()

def main():

    #Change the startIntersection and endIntersection here, whether to use Gaussian or Linear model, and penalty constant here!
    startIntersection = ('GOLDEN GATE AVE', 'WEBSTER ST')
    endIntersection = ('CHESTNUT ST', 'POWELL ST')

    gaussianTrue = 0
    penalty_constant = 0.001

    print("The output path is drawn in output.html file")
    #elif len(sys.argv) == 5:
    #    startIntersectoin = (sys.argv[2], sys.argv[3])
    #    endIntersection = (sys.argv[4], sys.argv[5])
    #else:
    #    print "Wrong number of arguments"
    #    return

    # Read from processed CSV
    processedFile = open('NodeMapList.csv', 'r')

    NodeMap = {}
    for line in processedFile.readlines():
        d = line.split('|')
        sKey = literal_eval(d[0])
        latLng = literal_eval(d[1])
        adjacent = literal_eval(d[2])
        crimeOccur = literal_eval(d[3])
        crimeList = literal_eval(d[4])

        NodeMap[sKey] = Node(sKey, latLng, adjacent, crimeOccur, crimeList)
    
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(PathProblem(startIntersection, endIntersection,NodeMap, gaussianTrue, penalty_constant))
    actions = ucs.actions
    points = actions

    #Draws points on Google Map
    map = show_map.Map(points)
    with open("output.html", "w") as out:
        print(map, file=out)
    
    #Mockup for UCS
    #AANode = Node('AA', (0, 0), ['AB', 'BA'])
    #AB->BC is possible!
    #ABNode = Node('AB', (1, 0), ['AA', 'BB','AC','BC'])
    #ACNode = Node('AC', (2, 0), ['AB', 'BC'])
    #BANode = Node('BA', (0, 1), ['AA', 'BB','CA'])
    #BBNode = Node('BB', (1, 1), ['AB', 'BA','CB','BC'])
    #BCNode = Node('BC', (2, 1), ['AC', 'CC','BB'])
    #CANode = Node('CA', (0, 2), ['BA', 'CB'])
    #CBNode = Node('CB', (1, 2), ['CA', 'BB','CC'])
    #CCNode = Node('CC', (2, 2), ['BC', 'CB'])
    #NodeMap = {'AA':AANode, 'AB':ABNode, 'AC':ACNode, 'BA':BANode, 'BB':BBNode, 'BC':BCNode, 'CA':CANode, 'CB':CBNode, 'CC':CCNode}
 

#Not used anymore - replaced by process() function
def writeToCSV():
    inputFile = open('traffic_result.csv', 'r')
    NodeMap = {}
    result = {}
    crimeMap = makeCrimeMap()

    for line in inputFile.readlines():
        if line[0]==',': continue
    
        s1 = line.split('|')[0].split(',')
        sKey = (s1[1], s1[2])
        
        s2 = line.split('|')[-1].split(',')
        latLng = (float(s2[-2]), float(s2[-1].replace('\n','')))

        adjacentList = []
        for x, y in zip(*[iter(s2[0:-2])]*2):
            x = x.replace('"', '')
            y = y.replace('"', '')
            adjacentList.append((x.strip(), y.strip()))
        #NodeMap[sKey] = Node(sKey, latLng, adjacentList)
        crimeOccurrence = makeCrimeOccurrence(latLng[0], latLng[1], 0.00325016538, 0.00325016538, crimeMap)
        NodeMap[sKey] = Node(sKey, latLng, adjacentList, crimeOccurrence)

    outputFile = open('NodeMap.csv', 'w')
    for sKey, node in NodeMap.iteritems():
        line = str(node.name) + '|' + str(node.location) + '|' + str(node.adjNodeName) + '|' + str(node.crimeOccurrence) + '\n'
        print(line)
        outputFile.write(line)
    outputFile.close()


if __name__ == "__main__":
    main()
