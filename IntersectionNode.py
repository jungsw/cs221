import pandas as pd
import uuid, googlemaps

'''
Created on Nov 28, 2015

@author: m_machine
'''

class IntersectionNode(object):
    # haha
    def __init__(self, x_loc, y_loc, gmap):
        '''
        Node is defined as an intersection of two or more roads, represented by lat/longitude.
        Node contains all of its adjacent nodes and their respective distance from it.
        '''
        self.id = uuid.uuid4()
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.client = googlemaps.Client(gmap)
        self.adjacent = []
        self.distances = []
    
    def parseLoc(self):
        return str(self.x_loc) + ', ' + str(self.y_loc)
    
    def setAdjacents(self, node_map):
        self.adjacent = node_map[self.parseLoc()]
        print self.adjacent
    
    def setDistances(self, node_map):
        key = self.parseLoc()
        distance_dict = self.client.distance_matrix(key, self.adjacent)
        for res_dict in distance_dict['rows'][0]['elements']:
            self.distances.append(res_dict['distance']['value'])
        print self.distances

nodemap = {'37.764861, -122.422886': ['37.764835, -122.423143', '37.764029, -122.422814', '37.764922, -122.421910'], \
           '37.763967, -122.424070': ['37.764777, -122.424146','37.764027, -122.422799']}

node = IntersectionNode(37.764861, -122.422886, 'AIzaSyCufQQEadq3JZOx5sXfwpfy4AUcR1AIXMM')
node.setAdjacents(nodemap)
node.setDistances(nodemap)
