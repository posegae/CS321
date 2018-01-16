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
        avgTempCheck = avgTemp - 72 < 1
        avgHumidityCheck = avgHumidity - 47 < 1
        stdDevTempCheck  = stdDevTemp <= 1.5
        stdDevHumidityCheck = stdDevHumidity <= 1.75

        printFloorState(officeList)
        print('\n')

        if (avgTempCheck and avgHumidityCheck and stdDevTempCheck and stdDevHumidityCheck):
            break

        curOffice = (curOffice + 1) % 12
    return officeVisits

def _calculateNewAvg(oldAvg, newDataPoint):
    return ((oldAvg * 11 / 12) + newDataPoint) / 12

def heatMiserRunV2(officeList):
    '''
    Look forward to the change in averages after each move.
    '''

    avgTemp, avgHumidity, c, d = getFloorMetrics(officeList)
    curOffice = 0
    officeVisits = 0
    while (True):
        officeVisits += 1
        # office = officeList[curOffice]
        avgTemp, avgHumidity, stdDevTemp, stdDevHumidity = getFloorMetrics(officeList)

        raiseTempNewAvg = _calculateNewAvg(avgTemp, officeList[curOffice].getTemp() + 1)
        lowerTempNewAvg = _calculateNewAvg(avgTemp, officeList[curOffice].getTemp() - 1)
        raiseHumidityNewAvg = _calculateNewAvg(avgHumidity, officeList[curOffice].getTemp() + 1)
        lowerHumidityNewAvg = _calculateNewAvg(avgHumidity, officeList[curOffice].getTemp() - 1)

        tempDone = avgTemp < 73 and avgTemp >= 72
        humidityDone = avgHumidity < 48 and avgHumidity >= 47


        scores = [abs(72 - raiseTempNewAvg), abs(72 - lowerTempNewAvg),
                  abs(47 - raiseHumidityNewAvg), abs(47 - lowerHumidityNewAvg),
                  max(abs(72 - avgTemp), abs(47 - avgHumidity))]

        if (officeList[curOffice].getTemp() == 75):
            scores[0] = 999
        if (officeList[curOffice].getTemp() == 65):
            scores[1] = 999
        if (officeList[curOffice].getHumidity() == 55):
            scores[2] = 999
        if (officeList[curOffice].getHumidity() == 45):
            scores[3] = 999

        if tempDone:
            scores[0] = 999
            scores[1] = 999

        if humidityDone:
            scores[2] = 999
            scores[3] = 999

        if tempDone and not humidityDone:
            scores[4] = 999
        if not tempDone and humidityDone:
            scores[4] = 999


        # if tempDone or humidityDone:
        #     scores[4] = 999

        best = scores.index(min(scores))
        # print()


        if (best == 0):
            officeList[curOffice].setTemp(officeList[curOffice].getTemp() + 1)
        elif (best == 1):
            officeList[curOffice].setTemp(officeList[curOffice].getTemp() - 1)
        elif (best == 2):
            officeList[curOffice].setHumidity(officeList[curOffice].getHumidity() + 1)
        elif (best == 3):
            officeList[curOffice].setHumidity(officeList[curOffice].getHumidity() - 1)
        elif (best == 4):
            pass
        else:
            print("something went horribly wrong")



        avgTemp, avgHumidity, stdDevTemp, stdDevHumidity = getFloorMetrics(officeList)
        avgTempCheck = avgTemp - 72 < 1
        avgHumidityCheck = avgHumidity - 47 < 1
        stdDevTempCheck  = stdDevTemp <= 1.5
        stdDevHumidityCheck = stdDevHumidity <= 1.75
        if (avgTempCheck and avgHumidityCheck and stdDevTempCheck and stdDevHumidityCheck):
            break
        print(avgTemp, avgHumidity)

        curOffice = (curOffice + 1) % 12
    return officeVisits

def heatMiserRunV3(officeList):
    '''
    change settings naively if it gets you closer to the ideal
    If neither does, change temperature to get closer to the average
    '''

    curOffice = 0
    while (True):
        officeVisits += 1
        # office = officeList[curOffice]
        avgTemp, avgHumidity, stdDevTemp, stdDevHumidity = getFloorMetrics(officeList)

        # trying to get towards the ideal


        avgTemp, avgHumidity, stdDevTemp, stdDevHumidity = getFloorMetrics(officeList)
        avgTempCheck = avgTemp - 72 < 1
        avgHumidityCheck = avgHumidity - 47 < 1
        stdDevTempCheck  = stdDevTemp <= 1.5
        stdDevHumidityCheck = stdDevHumidity <= 1.75
        if (avgTempCheck and avgHumidityCheck and stdDevTempCheck and stdDevHumidityCheck):
            break
        print(avgTemp, avgHumidity)

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

        print("=== Run {} initial state===".format(i))
        printFloorState(officeList)
        print("\n\n")
        runs.append(heatMiserRun(officeList))

        print("=== Run {} final state===".format(i))
        printFloorState(officeList)
        print("\n\n")

    print("Across {} runs, HeatMiser visited {} offices on average with a standard deviation of {}.".format(len(runs), statistics.mean(runs), statistics.stdev(runs)))

if __name__ == '__main__':
    main()
