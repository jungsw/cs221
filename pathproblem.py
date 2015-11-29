import util
import math

#name = string, x,y = latitude, longitude of the node, adjNodeName = list of names of nodes that are adjacent to the node, 
class Node:
    def __init__(self, name, x, y, adjNodeName): self.name, self.location, self.adjNodeName = name, (x,y), adjNodeName

def dist(a,b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] -b[1])**2)

#name to Node map: returns Node object when called by NodeMap[name]
class PathProblem(util.SearchProblem):
    def __init__(self, startStateName, endStateName, NodeMap): self.start, self.end, self.NodeMap = startStateName, endStateName, NodeMap
    def startState(self): return self.start
    def isGoal(self, state): return state == self.end
    def succAndCost(self, state):
        results = []
        for adjNode in self.NodeMap[state].adjNodeName:
            results.append((state+'->'+adjNode, adjNode, dist(self.NodeMap[state].location, self.NodeMap[adjNode].location)))
        return results

def main():
    AANode = Node('AA', 0, 0, ['AB', 'BA'])
    #AB->BC is possible!
    ABNode = Node('AB', 1, 0, ['AA', 'BB','AC','BC'])
    ACNode = Node('AC', 2, 0, ['AB', 'BC'])
    BANode = Node('BA', 0, 1, ['AA', 'BB','CA'])
    BBNode = Node('BB', 1, 1, ['AB', 'BA','CB','BC'])
    BCNode = Node('BC', 2, 1, ['AC', 'CC','BB'])
    CANode = Node('CA', 0, 2, ['BA', 'CB'])
    CBNode = Node('CB', 1, 2, ['CA', 'BB','CC'])
    CCNode = Node('CC', 2, 2, ['BC', 'CB'])
    NodeMap = {'AA':AANode, 'AB':ABNode, 'AC':ACNode, 'BA':BANode, 'BB':BBNode, 'BC':BCNode, 'CA':CANode, 'CB':CBNode, 'CC':CCNode}
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(PathProblem('AA','CC',NodeMap))
    actions = ucs.actions
    print actions

if __name__ == "__main__":
    main()
