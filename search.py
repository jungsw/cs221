import pandas as pd
import internode, processor

'''
Created on Dec 10, 2015

@author: m_machine
'''

class Search(object):
    '''
    this is a search algorithm involving already processed x-loc/y-loc, 
    adjacency map of nodes, and applies UCS/MDP to find the optimal path.
    '''


    def __init__(self, nodemap, traffic_data, train_data):
        self.nodemap = nodemap
        self.traffic_data = traffic_data
        self.train_data = train_data
    
    def stringParse(self, inter):
        return inter[0] + ' | ' + inter[1]
    
    '''
    start_loc, end_loc: list. ex) [1st st, Market st]
    returns search result
    '''   
    def searchIt(self, start_loc, end_loc):
        start_key = self.stringParse(start_loc)
        end_key = self.stringParse(end_loc)
        