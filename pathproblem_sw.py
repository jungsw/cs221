import util
import math

#name = string, x,y = latitude, longitude of the node, adjNodeName = list of names of nodes that are adjacent to the node, 
# 
class Node:
    def __init__(self, name, location, adjNodeName, crimes): self.name, self.location, self.adjNodeName, self.crimes = name, location, adjNodeName, crimes

def dist(a,b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] -b[1])**2)

def tupleToString(streetTuple):
    return '(' + streetTuple[0] + ',' + streetTuple[1] + ')' 

#name to Node map: returns Node object when called by NodeMap[name]
class PathProblem(util.SearchProblem):
    def __init__(self, startStateName, endStateName, NodeMap): self.start, self.end, self.NodeMap = startStateName, endStateName, NodeMap
    def startState(self): return self.start
    def isGoal(self, state): return state == self.end
    def succAndCost(self, state):
        results = []
        for adjNode in self.NodeMap[state].adjNodeName:
            if adjNode not in self.NodeMap: continue
            #results.append((tupleToString(state)+'->'+ tupleToString(adjNode), adjNode, dist(self.NodeMap[state].location, self.NodeMap[adjNode].location)))
            #results.append(( tupleToString(state)+'->'+ tupleToString(adjNode), adjNode, dist(self.NodeMap[state].location, self.NodeMap[adjNode].location) + dist(self.NodeMap[adjNode].location, self.NodeMap[self.end].location) - dist(self.NodeMap[state].location, self.NodeMap[self.end].location)))
            results.append(( self.NodeMap[state].location, adjNode, dist(self.NodeMap[state].location, self.NodeMap[adjNode].location) + dist(self.NodeMap[adjNode].location, self.NodeMap[self.end].location) - dist(self.NodeMap[state].location, self.NodeMap[self.end].location)))
        return results

def processTrain():
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
    
#    print crimeMap
    return crimeMap

def crimesAt(x_loc, y_loc, xpm, ypm, crimemap):
    crime_dict = {}
    for key in crimemap.keys():
        if key[0] > x_loc - xpm and key[0] < x_loc + xpm and key[1] > y_loc - ypm and key[1] < y_loc + ypm:
            if crimemap[key] in crime_dict:
                crime_dict[crimemap[key]] += 1
            else:
                crime_dict[crimemap[key]] = 1
                
#    print crime_dict
    return crime_dict

def main():

    inputFile = open('traffic_result.csv', 'r')
    NodeMap = {}
    result = {}
    crimemap = processTrain()

    for line in inputFile.readlines():
        if line[0]==',': continue
    
        s1 = line.split('|')[0].split(',')
        sKey = (s1[1], s1[2])
        
        s2 = line.split('|')[-1].split(',')
        latLng = (float(s2[-2]), float(s2[-1].replace('\n','')))
        #print latLng
        adjacentList = []
        for x, y in zip(*[iter(s2[0:-2])]*2):
            x = x.replace('"', '')
            y = y.replace('"', '')
            adjacentList.append((x.strip(), y.strip()))
        
        crimeOccurrence = crimesAt(latLng[0], latLng[1], 0.00325016538, 0.00325016538, crimemap)
        
        NodeMap[sKey] = Node(sKey, latLng, adjacentList, crimeOccurrencd)

    #print NodeMap
    
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
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(PathProblem(('EDDY ST', 'POLK ST'), ('GEARY ST', 'MASON ST'),NodeMap))
    actions = ucs.actions
    print actions

if __name__ == "__main__":
    main()
