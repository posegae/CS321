import random

class Office:
    def __init__(self, number, temp, humidity):
        self.number = number
        self.temp = temp
        self.humidity = humidity

    def getTemp():
        return self.temp

    def setTemp(newTemp):
        self.temp = newTemp

    def getHumidity():
        return self.humidity

    def setHumidty(newHumidity):
        self.humidity = newHumidity

    def getNumber():
        return self.number

    def setNumber(newNumber):
        self.number = newNumber

def prepOffices():
    officeList = []
    for i in range(1,13):
        randTemp = random.randint(65, 75)
        randHumidity = random.randint(45, 55)
        newOffice = Office(i, randTemp, randHumidity)
        officeList.append(newOffice)
    return officeList

def heatMiserFloorRound(officeList):
    print("Make sure that the offices are in order")
    metricsTuple = getAvgFloorMetrics(officeList)
    for office in officeList:
        # RUN SERVICE

def getAvgFloorMetrics(officeList):
    avgTemp = 0
    avgHumidity = 0
    for office in officeList:
        avgTemp += 1
        avgHumidity += 1
    avgTemp = avgTemp / len(officeList)
    avgHumidity = avgHumidity / len(officeList)
    return (avgTemp, avgHumidity)

def main():
    officeList = prepOffices()


if __name__ == '__main__':
    main()
