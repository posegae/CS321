'''
HeatMiser.py
Emma Posega Rappleye and Ju Yun Kim
CS 321
Carleton College

For assignment 2
'''
TEMP_IDEAL = 72
TEMP_IDEAL_SD = 1.5
TEMP_LOWER_LIMIT = 65
TEMP_UPPER_LIMIT = 75
HUM_IDEAL = 47
HUM_IDEAL_SD = 1.75
HUM_LOWER_LIMIT = 45
HUM_UPPER_LIMIT = 55

import random
import statistics
import math
import copy

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
    '10': ['7', '9', '11'],
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
    ('10', '11'): 2,
    ('11', '10'): 2,
    ('11', '12'): 19,
    ('12', '11'): 19
}


HEURISTIC = {
    ('1','2')	:13,
    ('1','3')	:15,
    ('1','4')	:19,
    ('1','5')	:25,
    ('1','6')	:20,
    ('1','7')	:35,
    ('1','8')	:32,
    ('1','9')	:34,
    ('1','10')	:37,
    ('1','11')	:42,
    ('1','12')	:40,
    ('2','1')	:13,
    ('2','3')	:11,
    ('2','4')	:7,
    ('2','5')	:10,
    ('2','6')	:8,
    ('2','7')	:21,
    ('2','8')	:19,
    ('2','9')	:18,
    ('2','10')	:24,
    ('2','11')	:26,
    ('2','12')	:25,
    ('3','1')	:15,
    ('3','2')	:11,
    ('3','4')	:12,
    ('3','5')	:11,
    ('3','6')	:7,
    ('3','7')	:23,
    ('3','8')	:22,
    ('3','9')	:31,
    ('3','10')	:30,
    ('3','11')	:34,
    ('3','12')	:33,
    ('4','1')	:19,
    ('4','2')	:7,
    ('4','3')	:12,
    ('4','5')	:6,
    ('4','6')	:10,
    ('4','7')	:20,
    ('4','8')	:18,
    ('4','9')	:16,
    ('4','10')	:22,
    ('4','11')	:26,
    ('4','12')	:24,
    ('5','1')	:25,
    ('5','2')	:10,
    ('5','3')	:11,
    ('5','4')	:6,
    ('5','6')	:4,
    ('5','7')	:10,
    ('5','8')	:4,
    ('5','9')	:12,
    ('5','10')	:8,
    ('5','11')	:13,
    ('5','12')	:12,
    ('6','1')	:20,
    ('6','2')	:8,
    ('6','3')	:7,
    ('6','4')	:10,
    ('6','5')	:4,
    ('6','7')	:9,
    ('6','8')	:7,
    ('6','9')	:11,
    ('6','10')	:9,
    ('6','11')	:15,
    ('6','12')	:13,
    ('7','1')	:35,
    ('7','2')	:21,
    ('7','3')	:23,
    ('7','4')	:20,
    ('7','5')	:10,
    ('7','6')	:9,
    ('7','8')	:4,
    ('7','9')	:12,
    ('7','10')	:17,
    ('7','11')	:21,
    ('7','12')	:3,
    ('8','1')	:32,
    ('8','2')	:19,
    ('8','3')	:22,
    ('8','4')	:18,
    ('8','5')	:4,
    ('8','6')	:7,
    ('8','7')	:4,
    ('8','9')	:5,
    ('8','10')	:2,
    ('8','11')	:7,
    ('8','12')	:5,
    ('9','1')	:34,
    ('9','2')	:18,
    ('9','3')	:31,
    ('9','4')	:16,
    ('9','5')	:12,
    ('9','6')	:11,
    ('9','7')	:12,
    ('9','8')	:5,
    ('9','10')	:8,
    ('9','11')	:15,
    ('9','12')	:22,
    ('10','1')	:37,
    ('10','2')	:24,
    ('10','3')	:30,
    ('10','4')	:22,
    ('10','5')	:18,
    ('10','6')	:9,
    ('10','7')	:17,
    ('10','8')	:2,
    ('10','9')	:8,
    ('10','11')	:2,
    ('10','12')	:4,
    ('11','1')	:42,
    ('11','2')	:26,
    ('11','3')	:34,
    ('11','4')	:26,
    ('11','5')	:13,
    ('11','6')	:15,
    ('11','7')	:21,
    ('11','8')	:7,
    ('11','9')	:15,
    ('11','10')	:2,
    ('11','12')	:19,
    ('12','1')	:40,
    ('12','2')	:25,
    ('12','3')	:33,
    ('12','4')	:24,
    ('12','5')	:12,
    ('12','6')	:13,
    ('12','7')	:3,
    ('12','8')	:5,
    ('12','9')	:22,
    ('12','10')	:4,
    ('12','11')	:19
}


class Floor:
    offices = []
    paths = {}
    weights = {}
    def __init__(self, numOffices):
        self.numOffices = numOffices

    def genFloorState(self, paths, weights):
        self.offices = []
        for i in range(1, self.numOffices + 1):
            randomTemp = random.randint(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT)
            randomHum = random.randint(HUM_LOWER_LIMIT, HUM_UPPER_LIMIT)
            self.offices.append(Office(i, randomTemp, randomHum))
        self.paths = paths
        self.weights = weights

    def get(self, n):
        if n < self.numOffices + 1:
            return self.offices[n - 1]
        else:
            print("office {} doesn't exist.".format(n))
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
        avgHum = statistics.mean(hums)
        tempSD = statistics.stdev(temps)
        humSD = statistics.stdev(hums)
        return (avgTemp, avgHum, tempSD, humSD)

    def getDeviantOffice(self):
        '''returns the office that needs settings modification the most. Can be
        determined through a variety of ways, but use sum of difference from
        the goal for now'''
        maxTotDev = 0
        goalOffice = None
        for office in self.offices:


            tempDiff = abs(TEMP_IDEAL - office.getTemp())
            humDiff = abs(HUM_IDEAL - office.getHumidity())
            # totDiff = math.sqrt(tempDiff**2 + humDiff**2)
            # totDiff = tempDiff + humDiff
            totDiff = max(tempDiff, humDiff)
            if  totDiff > maxTotDev:
                maxTotDev = totDiff
                goalOffice = office
        # print(goalOffice.getTemp())
        # print(goalOffice.getHumidity())
        # print('totDiff: {}'.format(totDiff))
        # print('getDeviantOffice is returning office: {}'.format(office.getNumber()))
        return goalOffice

    def getNeighbors(self, office):
        '''returns a list of neighbors that the given office has'''
        return self.paths[str(office.getNumber())]

    def printOfficeStates(self):
        '''prints the current temperature and humidity of all of the offices'''
        print('offices: {}'.format([office.getNumber() for office in self.offices]))
        print('temperatures: {}'.format([office.getTemp() for office in self.offices]))
        print('humidities: {}'.format([office.getHumidity() for office in self.offices]))


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
        self.position = random.randint(1, self.floor.numOffices)

    def moveTo(self, n):
        if n < self.floor.numOffices and n >= 0:
            self.position = n
        else:
            print("HeatMiser can't go to an office that doesn't exist")

    def incTemp(self):
        self.floor.office

    def aStarNavigate(self):
        ''' navigates to a given goal office via A* search through the office
        layout. The goal can be assumed to be given
        '''
        correctPath = None
        goal = self.floor.getDeviantOffice()
        if self.position == goal.getNumber():
            correctPath = [self.floor.get(self.position)]
            self.position = correctPath[-1].getNumber()
            self.alterOfficeSettings(correctPath[-1])
            return correctPath

        curOffice = self.floor.get(self.position)
        heuristic = self.getHeuristicWithOfficeNums(curOffice.getNumber(), goal.getNumber())
        cost = 0
        expanded = False
        paths = [ [[curOffice], heuristic, cost, expanded] ]
        while curOffice != goal:
            expandablePaths = [path for path in paths if not path[3]]
            fn = [path[1] + path[2] for path in expandablePaths]
            bestFnIdx = fn.index(min(fn))

            pathToExpand = expandablePaths[bestFnIdx][0]

            # look at end node to expand it
            nodeToExpand = pathToExpand[-1]

            self.position = nodeToExpand.getNumber()

            curOffice = nodeToExpand

            oldPath = [path for path in paths if path[0] == pathToExpand]
            oldPathIdx = paths.index(oldPath[0])
            paths[oldPathIdx][3] = True

            # expand the node, get its neighbors and add it to a
            # temporary path storage
            neighbors = self.floor.getNeighbors(nodeToExpand)
            for neighbor in neighbors:
                # branching a path
                pathcopy = copy.deepcopy(pathToExpand)
                neighborint = int(neighbor)
                pathcopy.append(self.floor.get(neighborint))

                # goal test upon node "generation"
                if (neighborint == goal.getNumber()):
                    # you've travelled to the goal! Return with the correct path
                    self.position = pathcopy[-1].getNumber()
                    self.alterOfficeSettings(pathcopy[-1])
                    return pathcopy
                neighborHeuristic = self.getHeuristicWithOfficeNums(neighborint, goal.getNumber())
                pathCost = accumulatePathValues(pathcopy)
                paths.append( [pathcopy, neighborHeuristic, pathCost, False] )


    def getHeuristicWithOfficeNums(self, initialPos, finalPos):
        if initialPos == finalPos:
            return 0
        return HEURISTIC[(str(initialPos),
                  str(finalPos))]

    def BFSNavigate(self):
        '''navigates to a given goal office via breadth-first search through
        the office layout. The goal can be assumed to be given (source from
        Sam who asked Blake)'''
        correctPath = None
        goal = self.floor.getDeviantOffice()
        if self.position == goal.getNumber():
            correctPath = [self.floor.get(self.position)]

            self.position = correctPath[-1].getNumber()

            self.alterOfficeSettings(correctPath[-1])

            return correctPath

        # this is the list of paths that we're working on now
        paths = [[self.floor.get(self.position)]]
        done = 0
        while not done:

            temps = []
            for path in paths:
                # crude infinite loop checking: no path should be longer than
                #  the number of nodes
                if len(path) > 12:
                    continue
                lastOffice = path[-1]
                neighbors = self.floor.getNeighbors(lastOffice)
                temp = []
                for neighbor in neighbors:
                    # branching a path
                    pathcopy = copy.deepcopy(path)
                    pathcopy.append(self.floor.get(int(neighbor)))
                    temp.append(pathcopy)
                temps.extend(temp)
            paths = temps
            for path in paths:
                if path[-1].getNumber() == goal.getNumber():
                    done = True
                    correctPath = path
            if paths == []:
                break

        self.position = correctPath[-1].getNumber()
        self.alterOfficeSettings(correctPath[-1])
        return correctPath


    def alterOfficeSettings(self, office):
        '''alters the office settings within bounds so that the floor metrics
        are closer to the ideal settings'''

        print('office {} initial temperature: {}'.format(office.getNumber(), office.getTemp())) # required print

        ### baseline: change to the desired settings
        office.setTemp(TEMP_IDEAL)
        office.setHumidity(HUM_IDEAL)

        print('office {} final temperature: {}'.format(office.getNumber(), office.getTemp())) # required print


def BFSTrial():
    ''' One run from start to finish where HeatMiser optimizes a floor from
    start to finish '''
    # initialize variables
    floor = Floor(12)
    floor.genFloorState(OFFICE_CONF, OFFICE_WEIGHTS)
    print('Initial state')
    floor.printOfficeStates()

    hm = HeatMiser(floor)
    hm.generateInitialState()


    avgTemp, avgHum, tempSD, humSD = hm.floor.getAllMetrics()
    done = False
    totalEdgeSums = []
    totalNumVisits = []
    i = 0
    while not done:
        # get to the worst-offender office
        print('HeatMiser starts at office {}'.format(hm.position)) # required print
        path = hm.BFSNavigate()
        print('HeatMiser goes to office {}'.format(path[-1].getNumber())) # required print
        # for analytics
        edgeSum = accumulatePathValues(path)
        numVisits = len(path)

        print('HeatMiser visited {} offices'.format(numVisits)) # required print
        print('HeatMiser\'s path cost is {}'.format(edgeSum)) # required print


        totalEdgeSums.append(edgeSum)
        totalNumVisits.append(numVisits)

        # checking for goal conditions
        avgTemp, avgHum, tempSD, humSD = hm.floor.getAllMetrics()

        # all required prints
        print('Floor average temp after change: {}'.format(avgTemp))
        print('Floor average humidity after change: {}'.format(avgHum))
        print('Floor temp standard deviation after change: {}'.format(tempSD))
        print('Floor humidity standard deviation after change: {}'.format(humSD))


        avgTempCond = TEMP_IDEAL - avgTemp < 1 and TEMP_IDEAL - avgTemp >= 0
        avgHumCond = HUM_IDEAL - avgHum < 1 and HUM_IDEAL - avgHum >= 0
        SDTempCond = tempSD <= TEMP_IDEAL_SD
        SDHumCond = humSD <= HUM_IDEAL_SD
        if avgTempCond and avgHumCond and SDTempCond and SDHumCond:
            done = True

    # These are all required too
    print()
    print('Final floor average temp: {}'.format(avgTemp))
    print('Final floor humidity: {}'.format(avgHum))
    print('Final floor temp standard deviation: {}'.format(tempSD))
    print('Final floor humidity standard deviation: {}'.format(humSD))
    print('Simulation total power consumption: {}'.format(sum(totalEdgeSums)))
    print('Simulation total office visits: {}'.format(sum(totalNumVisits)))
    return sum(totalEdgeSums),  sum(totalNumVisits)


def aStarTrial():
    ''' One run from start to finish where HeatMiser optimizes a floor from
    start to finish '''
    # initialize variables
    floor = Floor(12)
    floor.genFloorState(OFFICE_CONF, OFFICE_WEIGHTS)

    print('Initial state')
    floor.printOfficeStates()

    hm = HeatMiser(floor)
    hm.generateInitialState()

    avgTemp, avgHum, tempSD, humSD = hm.floor.getAllMetrics()
    done = False
    totalEdgeSums = []
    totalNumVisits = []
    i = 0
    while not done:
        # get to the worst-offender office
        print('HeatMiser starts at office {}'.format(hm.position)) # required print
        path = hm.aStarNavigate()
        print('HeatMiser goes to office {}'.format(path[-1].getNumber())) # required print

        edgeSum = accumulatePathValues(path)
        numVisits = len(path)


        print('HeatMiser visited {} offices'.format(numVisits)) # required print
        print('HeatMiser\'s path cost is {}'.format(edgeSum)) # required print

        totalEdgeSums.append(edgeSum)
        totalNumVisits.append(numVisits)

        # checking for goal conditions
        avgTemp, avgHum, tempSD, humSD = hm.floor.getAllMetrics()

        # all required prints
        print('Floor average temp after change: {}'.format(avgTemp))
        print('Floor average humidity after change: {}'.format(avgHum))
        print('Floor temp standard deviation after change: {}'.format(tempSD))
        print('Floor humidity standard deviation after change: {}'.format(humSD))

        avgTempCond = TEMP_IDEAL - avgTemp < 1 and TEMP_IDEAL - avgTemp >= 0
        avgHumCond = HUM_IDEAL - avgHum < 1 and HUM_IDEAL - avgHum >= 0
        SDTempCond = tempSD <= TEMP_IDEAL_SD
        SDHumCond = humSD <= HUM_IDEAL_SD
        if avgTempCond and avgHumCond and SDTempCond and SDHumCond:
            done = True
    # These are all required too

    print()
    print('Final floor average temp: {}'.format(avgTemp))
    print('Final floor humidity: {}'.format(avgHum))
    print('Final floor temp standard deviation: {}'.format(tempSD))
    print('Final floor humidity standard deviation: {}'.format(humSD))
    print('Simulation total power consumption: {}'.format(sum(totalEdgeSums)))
    print('Simulation total office visits: {}'.format(sum(totalNumVisits)))
    return sum(totalEdgeSums),  sum(totalNumVisits)


def accumulatePathValues(path):
    '''add up the edge values between offices'''
    val = 0
    for i in range(len(path) - 1):
        val += OFFICE_WEIGHTS[str(path[i].getNumber()), str(path[i+1].getNumber())]
    return val


def main():
    avgEdgeSums = []
    avgNumVisits = []
    for i in range(100):
        es, nv = BFSTrial()
        avgEdgeSums.append(es)
        avgNumVisits.append(nv)
    BFSAvgEdgeSum = statistics.mean(avgEdgeSums)
    BFSAvgNumVisits = statistics.mean(avgNumVisits)

    avgEdgeSums = []
    avgNumVisits = []
    for i in range(100):
        es, nv = aStarTrial()
        avgEdgeSums.append(es)
        avgNumVisits.append(nv)


    print("\n\nFinal results:")
    print("\nBFS Results:")
    print("BFS 100 simulations avg power consumption: {}".format(BFSAvgEdgeSum))
    print("BFS 100 simulations avg office visits: {}".format(BFSAvgNumVisits))
    print("\nA* Results:")
    print('A* 100 simulations avg power consumptions: {}'.format(statistics.mean(avgEdgeSums)))
    print('A* 100 simulations avg office visits: {}'.format(statistics.mean(avgNumVisits)), end='\n\n')


if __name__ == '__main__':
    main()
