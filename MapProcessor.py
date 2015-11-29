import csv
import pandas as pd
import numpy as np

'''
Created on Nov 28, 2015
@author: m_machine
'''
class MapProcessor(object):
    '''
    Kaggle Crime data CSV processor, for compiling list of crime occurrences
    Data Structure: pandas.DataFrame
    Latitude and Longitude: no processing, often they are intersection or exact side of the street
    '''

    def __init__(self, trainfile, testfile):
        self.train_filename = trainfile
        self.train_data = pd.DataFrame()
    
    def processTime(self, timedata):
        return timedata.split(' ')[1]
    
    def processTrainCSV(self):
        train_data = {'date': [], 'type': [], 'district': [], 'resolution': [], 'x_loc': [], 'y_loc': []}
        
        with open(self.train_filename, 'rb') as csvfile:
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
                train_data['x_loc'].append(row[7])
                train_data['y_loc'].append(row[8])
        
        self.train_data = pd.DataFrame(train_data)
        

