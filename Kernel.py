import IntersectionNode
import processor
import googlemaps 
'''
Created on Nov 28, 2015

@author: m_machine
'''

if __name__ == '__main__':
    processor = processor('train-2.csv', 'train 2.csv')
    gmap = googlemaps.Client(key = 'AIzaSyCufQQEadq3JZOx5sXfwpfy4AUcR1AIXMM')
    node = IntersectionNode(100, 100, gmap)