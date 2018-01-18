'''
HeatMiser.py
Emma Posega Rappleye and Ju Yun Kim
CS 321
Carleton College

For assignment 1
'''

import random
import statistics
import math

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

def prepOffices():
    officeList = []
    for i in range(1,13):
        randTemp = random.randint(65, 75)
        randHumidity = random.randint(45, 55)
        newOffice = Office(i, randTemp, randHumidity)
        officeList.append(newOffice)
    return officeList

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

def getFloorMetrics(officeList):
    '''
    Calculates floor averages and standard deviations for temperature and humidity
    '''
    temps = [office.temp for office in officeList]
    humidities = [office.humidity for office in officeList]
    avgTemp = statistics.mean(temps)
    avgHumidity = statistics.mean(humidities)
    stdDevTemp = statistics.stdev(temps)
    stdDevHumidity = statistics.stdev(humidities)
    return (avgTemp, avgHumidity, stdDevTemp, stdDevHumidity)

def printFloorState(officeList):
    for office in officeList:
        print("Office {}: {}F, {}%".format(office.getNumber(), office.getTemp(), office.getHumidity()))
    avgTemp, avgHumidity, stdDevTemp, stdDevHumidity = getFloorMetrics(officeList)
    print("Average temperature: {}".format(avgTemp))
    print("Average humidity: {}".format(avgHumidity))
    print("Temperature standard deviation: {}".format(stdDevTemp))
    print("Humidity standard deviation: {}".format(stdDevHumidity))

def main():
    runs = []
    for i in range(100):
        officeList = prepOffices()

        avgTemp, avgHumidity, stdDevTemp, stdDevHumidity = getFloorMetrics(officeList)

        print("=== Run {} initial state===".format(i))
        printFloorState(officeList)
        print("\n\n")
        runs.append(heatMiserRun(officeList))

        print("=== Run {} final state===".format(i))
        printFloorState(officeList)
        print("\n\n")

        # if you want get initial office settings and number of rounds: 
        # with open("b.txt", 'a') as f:
        #     f.write("{}, {}, {}, {}, {}\n".format(avgTemp, avgHumidity, stdDevTemp, stdDevHumidity, runs[-1]))



    print("Across {} runs, HeatMiser visited {} offices on average with a standard deviation of {}.".format(len(runs), statistics.mean(runs), statistics.stdev(runs)))

if __name__ == '__main__':
    main()
