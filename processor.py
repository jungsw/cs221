import pandas as pd
import numpy as np
import internode
import responses, googlemaps, csv
#from _snap import count
from _Res import Count1Resources

'''
Created on Nov 28, 2015
@author: m_machine
'''
class Processor(object):
    '''
    Traffic Intersection data CSV processor, as well as Kaggle Crime data CSV processor, 
    for compiling list of crime occurrences
    Data Structure: pandas.DataFrame
    Latitude and Longitude: no processing, often they are intersection or exact side of the street
    '''

    def __init__(self, gmap):
        # crime map data and dataframe
        self.train_data = pd.DataFrame()
        # traffic map data and dataframe
        self.traffic_data = pd.DataFrame()
        # google maps API Key
        self.apikey = gmap
        self.client = googlemaps.Client(gmap)
        self.node_map = {}
    
    def processTime(self, timedata):
        return timedata.split(' ')[1]
    
    def processStreetName(self, inter):
        inter = inter.split('\\')[0].strip(' ')
        if inter[0] == '0':
            inter = inter[1:]
        return inter
    
    def processNode(self, inter1, inter2):
        node = internode.IntersectionNode(inter1, inter2, self.apikey)
        return node
    
    """
    Given an intersection as part of traffic_data, returns a list of adjacent streets
    based on the order of intersections in Intersections_only.csv
    """
    def processTrafficData(self):
        for index, row in self.traffic_data.iterrows():

            adjacent_list = []
            if index > 1 and index < 18467:
                if self.traffic_data.ix[index - 1]['inter1'] == row[0]:
                    key1 = self.traffic_data.ix[index - 1]['inter1'] + ', ' + self.traffic_data.ix[index - 1]['inter2']
                    adjacent_list.append(key1)
                    
                if self.traffic_data.ix[index + 1]['inter1'] == row[0]:
                    key2 = self.traffic_data.ix[index + 1]['inter1'] + ', ' + self.traffic_data.ix[index + 1]['inter2']
                    adjacent_list.append(key2)
                
                keylist = np.where(self.traffic_data['inter1'] == row[1])[0]
                keylist1 = np.where(self.traffic_data['inter2'] == row[0])[0]
                
                ind_list = np.intersect1d(keylist, keylist1)
                if len(ind_list) >= 1:
                    ind = ind_list[0]
                    
                    if ind > 1 and ind < 18467:
                        if self.traffic_data.ix[ind - 1]['inter1'] == row[1]:
                            key3 = self.traffic_data.ix[ind - 1]['inter1'] + ', ' + self.traffic_data.ix[ind - 1]['inter2']
                            adjacent_list.append(key3)
                        
                        if self.traffic_data.ix[ind + 1]['inter1'] == row[1]:
                            key4 = self.traffic_data.ix[ind + 1]['inter1'] + ', ' + self.traffic_data.ix[ind + 1]['inter2']
                            adjacent_list.append(key4)
                
            node = row['node']
            node.setAdjacents(adjacent_list)
    """
    Processes traffic intersection data and populates it with relevant information
    as a Pandas Data Frame
    """
    def processTrafficCSV(self, traffic_filename):
        traffic_data = {'inter1': [], 'inter2': [], 'x_loc': [], 'y_loc': [], 'node': []}
        with open(traffic_filename, 'rb') as csvfile:
            has_header = csv.Sniffer().has_header(csvfile.read(1024))
            csvfile.seek(0)            
            mapreader = csv.reader(csvfile, delimiter=',')
            
            if has_header:
                next(mapreader)
                
            for row in mapreader:
                st1 = self.processStreetName(row[1])
                st2 = self.processStreetName(row[2])
                traffic_data['inter1'].append(st1)
                traffic_data['inter2'].append(st2)
                traffic_data['x_loc'].append(0.0)
                traffic_data['y_loc'].append(0.0)
                traffic_data['node'].append(self.processNode(st1, st2))

        self.traffic_data = pd.DataFrame(traffic_data)
        print self.traffic_data
        #print self.traffic_data
        
    """
    Processes crime data and populates it with relevant information
    as a Pandas Data Frame
    """
    def processTrainCSV(self, train_filename):
        train_data = {'date': [], 'type': [], 'district': [], 'resolution': [], \
                      'x_loc': [], 'y_loc': []}
        
        with open(train_filename, 'rb') as csvfile:
            has_header = csv.Sniffer().has_header(csvfile.read(1024))
            csvfile.seek(0)            
            mapreader = csv.reader(csvfile, delimiter=',')
            
            if has_header:
                next(mapreader)
            
            for row in mapreader:
                train_data['date'].append(self.processTime(row[0]))
                train_data['type'].append(row[1])
                train_data['district'].append(row[4])
                train_data['resolution'].append(row[5])
                train_data['x_loc'].append(float(row[7]))
                train_data['y_loc'].append(float(row[8]))
        
        self.train_data = pd.DataFrame(train_data)  
        #print self.train_data

    def printCrimesInRegion(self, xlow, xhigh, ylow, yhigh):
        train_data = {'date': [], 'type': [], 'district': [], 'resolution': [], \
                      'x_loc': [], 'y_loc': []}

        xlowerbound = (self.train_data['x_loc'] >= xlow) 
        xupperbound = (self.train_data['x_loc'] <= xhigh)
        ylowerbound = (self.train_data['y_loc'] >= ylow) 
        yupperbound = (self.train_data['y_loc'] <= yhigh)

        selectedCrimes = self.train_data[xlowerbound & xupperbound & ylowerbound & yupperbound].reindex(columns=['x_loc', 'y_loc'])
        #selectedCrimes = self.train_data.reindex(columns=['x_loc', 'y_loc'])
        selectedCrimes = selectedCrimes.reset_index(drop=True)
        #print selectedCrimes.to_string(index=False)
        #selectedCrimes.to_csv('Tenderloin_crimes.csv')
        selectedCrimes.to_csv('Tenderloin_passing_region_crimes.csv')

#        selectedCrimes = pd.DataFrame(train_data)

 #       for index, row in self.train_data.iterrows():
 #           x = row[4]
 #           y = row[5]

 #           if (x >= xlow) and (x <= xhigh) and (y >= ylow) and (y <= yhigh):
 #               selectedCrimes.append(row, ignore_index=True)
#        print selectedCrimes
    
    def processIntersectionToLatLong(self, lat_long_filename):
        print 'I am at lat long'
        with open(lat_long_filename, 'rb') as csvfile:
            mapreader = csv.reader(csvfile, delimiter = '|')
            next(mapreader, None)
            
            for row in mapreader:
                latlong_list = row[0].strip('*').split(',')
                latlong_list[0] = latlong_list[0].strip(' ')
                latlong_list[1] = latlong_list[1].strip(' ')
                
                if float(latlong_list[0]) < 10000 and float(latlong_list[0]) > 37:
                    
                    stnames = row[1].split(',')[0].strip(' ').split('&')
                    stnames[0] = stnames[0].strip(' ').upper()
                    if stnames[0][0] =='0':
                        stnames[0] = stnames[0][1:]
                    
                    if len(stnames) == 2 and stnames[0] != 'SAN FRANCISCO':
                        stnames[1] = stnames[1].strip(' ').upper()
                        if stnames[1][0] =='0':
                            stnames[1] = stnames[1][1:]
                        
                        self.traffic_data.loc[(self.traffic_data.inter1 == stnames[0]) \
                                              & (self.traffic_data.inter2 == stnames[1]), 'x_loc'] = latlong_list[0]
                        self.traffic_data.loc[(self.traffic_data.inter1 == stnames[0]) \
                                              & (self.traffic_data.inter2 == stnames[1]), 'y_loc'] = latlong_list[1]

                        self.traffic_data.loc[(self.traffic_data.inter1 == stnames[1]) \
                                              & (self.traffic_data.inter2 == stnames[0]), 'x_loc'] = latlong_list[0]
                        self.traffic_data.loc[(self.traffic_data.inter1 == stnames[1]) \
                                              & (self.traffic_data.inter2 == stnames[0]), 'y_loc'] = latlong_list[1]
            
            self.traffic_data = self.traffic_data[self.traffic_data.x_loc != 0.0]
            self.traffic_data.to_csv('traffic_result.csv', ',')
            print self.traffic_data
  
    
    def processDistances(self):
        pass
        # for elem in self.node_map.keys():
        #   print self.client.distance_matrix(elem, self.node_map[elem])
        
        

nodemap = {'37.764861, -122.422886': ['37.764835, -122.423143', '37.764029, -122.422814', '37.764922, -122.421910'], \
           '37.763967, -122.424070': ['37.764777, -122.424146','37.764027, -122.422799']}
process = Processor('AIzaSyCufQQEadq3JZOx5sXfwpfy4AUcR1AIXMM')
#<<<<<<< HEAD
#process.processTrafficCSV('List_of_Intersections_only.csv')
process.processTrainCSV('../train.csv')
#process.processTrafficData()
#process.printCrimesInRegion(-122.42372, -122.40668, 37.78251, 37.78852) - for Tenderloin
process.printCrimesInRegion(-122.423800, -122.389200, 37.778508, 37.805400)
#=======
#process.processTrafficCSV('List_of_Intersections_only.csv')
# process.processTrainCSV('train.csv')
#process.processTrafficData()
#process.processIntersectionToLatLong('IntersectionsWithLatLng.csv')
#>>>>>>> ecadb059561463a961a10bdf4796a32dfb7904cb
