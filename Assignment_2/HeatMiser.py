'''
HeatMiser.py
Emma Posega Rappleye and Ju Yun Kim
CS 321
Carleton College

For assignment 2
'''

TEMP_LOWER_LIMIT = 65
TEMP_UPPER_LIMIT = 75
HUM_LOWER_LIMIT = 45
HUM_UPPER_LIMIT = 55

import random
import statistics
import math

### hard-coded paths for the specific simulation floor:
OFFICE_CONF = {
    '1': ['2', '3'],
    '2': ['1', '4'],
    '3': ['1', '7'],
    '4': ['2', '5', '6', '9'],
    '5': ['4', '8'],
    '6': ['4', '7'],
    '7': ['3', '6', '10'],
    '8': ['5', '9'],
    '9': ['4', '8', '10'],
    '10': ['7', '9'],
    '11': ['10', '12'],
    '12': ['11']
}

OFFICE_WEIGHTS = {
    ('1', '2'): 13,
    ('1', '3'): 15,
    ('2', '1'): 13,
    ('2', '4'): 7,
    ('3', '1'): 15,
    ('3', '7'): 23,
    ('4', '2'): 7,
    ('4', '5'): 6,
    ('4', '6'): 10,
    ('4', '9'): 16,
    ('5', '4'): 6,
    ('5', '8'): 4,
    ('6', '4'): 10,
    ('6', '7'): 9,
    ('7', '3'): 23,
    ('7', '6'): 9,
    ('7', '10'): 17,
    ('8', '5'): 4,
    ('8', '9'): 5,
    ('9', '4'): 16,
    ('9', '8'): 5,
    ('9', '10'): 8,
    ('10', '7'): 17,
    ('10', '9'): 8,
    ('11', '10'): 2,
    ('11', '12'): 19,
    ('12', '11'): 19
}


class Floor:
    offices = []
    paths = {}
    weights = {}
    def __init__(self, numOffices):
        self.numOffices = numOffices

    def generateInitialState(self, paths, weights):
        for i in range(self.numOffices):
            randomTemp = random.randint(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT)
            randomHum = random.randint(HUM_LOWER_LIMIT, HUM_UPPER_LIMIT)
            self.offices.append(Office(i, randomTemp, randomHum))
        self.paths = paths
        self.weights = weights

    def get(self, n):
        if n < numOffices:
            return self.numOffices[n]
        else:
            print("that office doesn't exist.")
            return None


    def getAvgTemp(self):
        temps = [office.getTemp() for office in self.offices]
        return statistcs.mean(temps)

    def getAvgHum(self):
        hums = [office.getHumidity() for office in self.offices]
        return statistics.mean(hums)

    def getTempSD(self):
        temps = [office.getTemp() for office in self.offices]
        return statistics.stdev(temps)

    def getHumSD(self):
        hums = [office.getHumidity() for office in self.offices]
        return statistics.stdev(hums)

    def getAllMetrics(self):
        temps = [office.getTemp() for office in self.offices]
        hums = [office.getHumidity() for office in self.offices]
        avgTemp = statistics.mean(temps)
        avgHum = statistics.mean(humidities)
        tempSD = statistics.stdev(temps)
        humSD = statistics.stdev(humidities)
        return (avgTemp, avgHum, tempSD, humSD)



class Office:
    def __init__(self, number, temp, humidity):
        self.number = number
        self.temp = temp
        self.humidity = humidity

    def getTemp(self):
        return self.temp

    def setTemp(self, newTemp):
        self.temp = newTemp

    def getHumidity(self):
        return self.humidity

    def setHumidity(self, newHumidity):
        self.humidity = newHumidity

    def getNumber(self):
        return self.number

    def setNumber(self, newNumber):
        self.number = newNumber

class HeatMiser:
    position = -1
    def __init__(self, floor):
        self.floor = floor

    def generateInitialState(self):
        self.position = random.randint(0, self.floor.numOffices)

    def moveTo(self, n):
        if n < self.floor.numOffices and n >= 0:
            self.position = n
        else:
            print("HeatMiser can't go to an office that doesn't exist")

    def incTemp(self):
        self.floor.office

    def DFSChange(self):
        ''' use DFS to find  next office to go to '''
        curDestination = None
        consideredOffices = []
        


def main():
    floor = Floor(12)
    floor.generateInitialState(OFFICE_CONF, OFFICE_WEIGHTS)
    hm = HeatMiser(floor)

    pass

if __name__ == '__main__':
    main()
