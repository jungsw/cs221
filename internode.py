import pandas as pd
import uuid, googlemaps

'''
Created on Nov 28, 2015

@author: m_machine
'''

class IntersectionNode(object):
    
    def __init__(self, inter1, inter2, gmap):
        '''
        Node is defined as an intersection of two or more roads, represented by lat/longitude.
        Node contains all of its adjacent nodes and their respective distance from it.
        '''
        self.id = uuid.uuid4()
        self.street1 = inter1
        self.street2 = inter2
        # self.client = googlemaps.Client(gmap)
        self.adjacent = []
        self.distances = []
    
    def parseLoc(self):
        return str(self.street1) + ', ' + str(self.street2)
    
    def setAdjacents(self, adjacent_list):
        self.adjacent = adjacent_list
    
    def setDistances(self, node_map):
        key = self.parseLoc()
        distance_dict = self.client.distance_matrix(key, self.adjacent)
        for res_dict in distance_dict['rows'][0]['elements']:
            self.distances.append(res_dict['distance']['value'])

nodemap = {'37.764861, -122.422886': ['37.764835, -122.423143', '37.764029, -122.422814', '37.764922, -122.421910'], \
           '37.763967, -122.424070': ['37.764777, -122.424146','37.764027, -122.422799']}

node = IntersectionNode(37.764861, -122.422886, 'AIzaSyCufQQEadq3JZOx5sXfwpfy4AUcR1AIXMM')
