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

class Floor:
    offices = []
    def __init__(self, numOffices):
        self.numOffices = numOffices

    def generateInitialState(self):
        for i in range(self.numOffices):
            randomTemp = random.randint(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT)
            randomHum = random.randint(HUM_LOWER_LIMIT, HUM_UPPER_LIMIT)
            offices.append(Office(i, randomTemp, randomHum))

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

def heatMiserRun(officeList):
    '''
    HeatMiser goes through all of the offices in order repeatedly until
    the floor reaches the desired settings
    '''
    metricsTuple = getFloorMetrics(officeList)
    curOffice = 0
    officeVisits = 0
    while (True):
        officeVisits += 1
        office = officeList[curOffice]
        print("HeatMiser is in office {}".format(office.getNumber()))

        officeTemp = office.getTemp()
        officeHumidity = office.getHumidity()
        print("Temperature: {}F, Humidity: {}%".format(officeTemp, officeHumidity))
        if (abs(officeTemp - 72) >= abs(officeHumidity - 47)):
            if (officeTemp > 72):
                office.setTemp(officeTemp - 1)
                print("HeatMiser lowers the temperature")
            elif (officeTemp < 72):
                office.setTemp(officeTemp + 1)
                print("HeatMiser raises the temperature")
            else:
                print("HeatMiser does nothing")
                pass
        else:
            if (officeHumidity > 47):
                office.setHumidity(officeHumidity - 1)
                print("HeatMiser lowers the humidity")
            elif (office.getHumidity() < 47):
                office.setHumidity(officeHumidity + 1)
                print("HeatMiser raises the humidity")
            else:
                print("HeatMiser does nothing")
                pass

        officeTemp = office.getTemp()
        officeHumidity = office.getHumidity()
        print("Temperature: {}F, Humidity: {}%".format(officeTemp, officeHumidity))


        avgTemp, avgHumidity, stdDevTemp, stdDevHumidity = getFloorMetrics(officeList)
        avgTempCheck = (avgTemp - 72 < 1) and (avgTemp - 72 >= 0)
        avgHumidityCheck = (avgHumidity - 47 < 1) and (avgHumidity - 47 >= 0)
        stdDevTempCheck  = stdDevTemp <= 1.5
        stdDevHumidityCheck = stdDevHumidity <= 1.75

        #printFloorState(officeList)
        print('\n')

        if (avgTempCheck and avgHumidityCheck and stdDevTempCheck and stdDevHumidityCheck):
            printFloorState(officeList)
            break

        curOffice = (curOffice + 1) % 12
    return officeVisits


def main():
    pass

if __name__ == '__main__':
    main()
