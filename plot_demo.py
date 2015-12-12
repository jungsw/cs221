import numpy as np
import matplotlib.pyplot as plt
import csv


def processcrimeCSV(crime_filename):
    crime_data = {'x_loc': [], 'y_loc': []}
        
    with open(crime_filename, 'rb') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)            
        mapreader = csv.reader(csvfile, delimiter=',')
            
        if has_header:
            next(mapreader)
            
        for row in mapreader:
            crime_data['x_loc'].append(float(row[1]))
            crime_data['y_loc'].append(float(row[2]))
    return crime_data
        


crime_data = processcrimeCSV('Bigger_retion_crimes.csv')
x = crime_data['x_loc']
y = crime_data['y_loc']
plt.scatter(x, y)
plt.show()