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
        print('totDiff: {}'.format(totDiff))
        print('getDeviantOffice is returning office: {}'.format(office.getNumber()))
        return goalOffice

    def getNeighbors(self, office):
        '''returns a list of neighbors that the given office has'''
        return self.paths[str(office.getNumber())]


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
        paths = [ ([curOffice], heuristic, cost) ]
        while curOffice != goal:
            # print('while loop in a*')
            # find the path with the best g(n) + h(n) (distance + heuristic)
            fn = [path[1] + path[2] for path in paths]
            bestFnIdx = fn.index(min(fn))
            pathToExpand = paths[bestFnIdx][0]


            # look at end node to expand it
            nodeToExpand = pathToExpand[-1]

            self.position = nodeToExpand.getNumber()
            print(goal.getNumber())
            print(self.position)
            curOffice = nodeToExpand


            # expand the node, get its neighbors and add it to a
            # temporary path storage
            neighbors = self.floor.getNeighbors(nodeToExpand)
            for neighbor in neighbors:
                # branching a path
                pathcopy = copy.deepcopy(pathToExpand)
                neighborint = int(neighbor)
                pathcopy.append(self.floor.get(neighborint))
                neighborHeuristic = self.getHeuristicWithOfficeNums(neighborint, goal.getNumber())
                pathCost = accumulatePathValues(pathcopy)
                paths.append( (pathcopy, neighborHeuristic, pathCost) )





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
            # print(type(self.position))
            # print(self.position)
            correctPath = [self.floor.get(self.position)]
            # print('{}'.format(correctPath[-1].getTemp()))

            self.position = correctPath[-1].getNumber()
            print([n.getNumber() for n in self.floor.offices])
            print([n.getNumber() for n in correctPath])
            # print('HeatMiser is in office: {}'.format(correctPath[-1].getNumber()))

            print('before: correctPath[-1] stats: {}, {}'.format(correctPath[-1].getTemp(), correctPath[-1].getHumidity()))
            self.alterOfficeSettings(correctPath[-1])
            print('after: correctPath[-1] stats: {}, {}'.format(correctPath[-1].getTemp(), correctPath[-1].getHumidity()))

            return correctPath

        # this is the list of paths that we're working on now
        paths = [[self.floor.get(self.position)]]
        done = 0
        while not done:
            # print('number of paths: {}'.format(len(paths)))
            temps = []
            for path in paths:
                # crude infinite loop checking: no path should be longer than
                #  the number of nodes
                if len(path) > 12:
                    # toRemove.append(path)
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
        # print(correctPath[-1].getNumber())

        self.position = correctPath[-1].getNumber()
        self.alterOfficeSettings(correctPath[-1])
        return correctPath

    def evalCandidateChanges(self, candidates, metric, office):
        '''returns the 'goodness' of changing the value to the candidates.
        Returns a list of 'goodnesses' for each candidate'''
        officeIdx = self.floor.offices.index(office)
        if metric == 'temp':
            curState = [office.getTemp() for office in self.floor.offices]
            goalAvg = TEMP_IDEAL
            goalSD = TEMP_IDEAL_SD
        elif metric == 'hum':
            curState = [office.getHumidity() for office in self.floor.offices]
            goalAvg = HUM_IDEAL
            goalSD = HUM_IDEAL_SD
        else:
            print('evalCandidateChanges: enter a valid metric to evaluate (temp, hum)')
        goodnesses = []
        for c in candidates:
            cState = copy.deepcopy(curState)
            curState[officeIdx] = c
            cAvg = statistics.mean(curState)
            cSD = statistics.stdev(curState)
            # currently, goodness measured by sum of percent difference bw real and ideal metrics
            goodness = max([abs(goalAvg - cAvg), abs(goalSD - cSD)])
            # if measure == 'avg':
            #     goodness = (abs(goalAvg - cAvg) / goalAvg)
            # elif measure == 'sd':
            #     goodness = (abs(goalSD - cSD) / goalSD)
            goodnesses.append(goodness)
        return goodnesses


    def alterOfficeSettings(self, office):
        '''alters the office settings within bounds so that the floor metrics
        are closer to the ideal settings'''

        ### baseline: change to the desired settings
        print('changing office setting')
        office.setTemp(TEMP_IDEAL)
        office.setHumidity(HUM_IDEAL)


        # avgTemp, avgHum, tempSD, humSD = self.floor.getAllMetrics()
        # avgTempCond = TEMP_IDEAL - avgTemp < 1 and TEMP_IDEAL - avgTemp >= 0
        # avgHumCond = HUM_IDEAL - avgHum < 1 and HUM_IDEAL - avgHum >= 0
        # SDTempCond = tempSD <= TEMP_IDEAL_SD
        # SDHumCond = humSD <= HUM_IDEAL_SD
        #
        #
        # possibleNewTemps = [temp for temp in range(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT + 1)]
        #
        # tempCandEval = self.evalCandidateChanges(possibleNewTemps, 'temp', office)
        # bestNewTemp = possibleNewTemps[tempCandEval.index(min(tempCandEval))]
        #
        # if not avgTempCond or not SDTempCond:
        #     # if the conditions aren't met, and HeatMiser doesn't want to change,
        #     #  pick the second best
        #     if bestNewTemp == office.getTemp():
        #         print('second best temp is being chosen')
        #         possibleNewTemps[tempCandEval.index(min(tempCandEval))] = 999999
        #         bestNewTemp = possibleNewTemps[tempCandEval.index(min(tempCandEval))]
        #
        #
        # office.setTemp(bestNewTemp)
        #
        #
        # possibleNewHums = [hum for hum in range(HUM_LOWER_LIMIT, HUM_UPPER_LIMIT + 1)]
        #
        # humCandEval = self.evalCandidateChanges(possibleNewHums, 'hum', office)
        # bestNewHum = possibleNewHums[humCandEval.index(min(humCandEval))]
        # office.setHumidity(bestNewHum)
        #
        # if not avgHumCond or not SDHumCond:
        #     # same deal with humidity
        #     if bestNewHum == office.getHumidity():
        #         print('second best humidity is being chosen')
        #         possibleNewHums[humCandEval.index(min(humCandEval))] = 999999
        #         bestNewHum = possibleNewHums[humCandEval.index(min(humCandEval))]

        # if not avgTempCond:
        #     tempCandEval = self.evalCandidateChanges(possibleNewTemps, 'temp', 'avg', office)
        #     bestNewTemp = possibleNewTemps[tempCandEval.index(min(tempCandEval))]
        #     office.setTemp(bestNewTemp)
        # if not SDTempCond:
        #     tempCandEval = self.evalCandidateChanges(possibleNewTemps, 'temp', 'sd', office)
        #     bestNewTemp = possibleNewTemps[tempCandEval.index(min(tempCandEval))]
        #     office.setTemp(bestNewTemp)
        #
        #
        #
        # possibleNewHums = [hum for hum in range(HUM_LOWER_LIMIT, HUM_UPPER_LIMIT + 1)]
        # if not avgHumCond:
        #     humCandEval = self.evalCandidateChanges(possibleNewHums, 'hum', 'avg', office)
        #     bestNewHum = possibleNewHums[humCandEval.index(min(humCandEval))]
        #     office.setHumidity(bestNewHum)
        # if not SDHumCond:
        #     humCandEval = self.evalCandidateChanges(possibleNewHums, 'hum', 'sd', office)
        #     bestNewHum = possibleNewHums[humCandEval.index(min(humCandEval))]
        #     office.setHumidity(bestNewHum)


        # print(bestNewTemp, bestNewHum)




def BFSTrial():
    ''' One run from start to finish where HeatMiser optimizes a floor from
    start to finish '''
    # initialize variables
    floor = Floor(12)
    floor.genFloorState(OFFICE_CONF, OFFICE_WEIGHTS)
    print('initial floor state')
    print([n.getNumber() for n in floor.offices])
    hm = HeatMiser(floor)
    hm.generateInitialState()

    avgTemp, avgHum, tempSD, humSD = hm.floor.getAllMetrics()
    done = False
    totalEdgeSums = []
    totalNumVisits = []
    i = 0
    while not done:
        print('{}'.format(hm.position))
        # get to the worst-offender office
        print('\n\nabout to call BFS Navigate')
        print([n.getNumber() for n in floor.offices])
        print('called BFS Navigate')
        path = hm.BFSNavigate()
        print('post-BFS Navigate')
        print([n.getNumber() for n in floor.offices])
        #if (i == 11):
        #    return
        #i += 1
        # for analytics
        edgeSum = accumulatePathValues(path)
        numVisits = len(path)

        totalEdgeSums.append(edgeSum)
        totalNumVisits.append(numVisits)

        print('{}/{}, {}/{}, {}/{}, {}/{}'.format(avgTemp, TEMP_IDEAL,
                                                  avgHum, HUM_IDEAL,
                                                  tempSD, TEMP_IDEAL_SD,
                                                  humSD, HUM_IDEAL_SD))

        # checking for goal conditions
        avgTemp, avgHum, tempSD, humSD = hm.floor.getAllMetrics()
        avgTempCond = TEMP_IDEAL - avgTemp < 1 and TEMP_IDEAL - avgTemp >= 0
        avgHumCond = HUM_IDEAL - avgHum < 1 and HUM_IDEAL - avgHum >= 0
        SDTempCond = tempSD <= TEMP_IDEAL_SD
        SDHumCond = humSD <= HUM_IDEAL_SD
        if avgTempCond and avgHumCond and SDTempCond and SDHumCond:
            done = True
    # print(statistics.mean(totalEdgeSums))
    # print(statistics.mean(totalNumVisits))
    # print(sum(totalEdgeSums))
    # print(sum(totalNumVisits))
    return sum(totalEdgeSums),  sum(totalNumVisits)


def aStarTrial():
    ''' One run from start to finish where HeatMiser optimizes a floor from
    start to finish '''
    # initialize variables
    floor = Floor(12)
    floor.genFloorState(OFFICE_CONF, OFFICE_WEIGHTS)
    hm = HeatMiser(floor)
    hm.generateInitialState()

    avgTemp, avgHum, tempSD, humSD = hm.floor.getAllMetrics()
    done = False
    totalEdgeSums = []
    totalNumVisits = []
    i = 0
    while not done:
        # get to the worst-offender office
        path = hm.aStarNavigate()

        edgeSum = accumulatePathValues(path)
        numVisits = len(path)

        totalEdgeSums.append(edgeSum)
        totalNumVisits.append(numVisits)

        print('{}/{}, {}/{}, {}/{}, {}/{}'.format(avgTemp, TEMP_IDEAL,
                                                  avgHum, HUM_IDEAL,
                                                  tempSD, TEMP_IDEAL_SD,
                                                  humSD, HUM_IDEAL_SD))

        # checking for goal conditions
        avgTemp, avgHum, tempSD, humSD = hm.floor.getAllMetrics()
        avgTempCond = TEMP_IDEAL - avgTemp < 1 and TEMP_IDEAL - avgTemp >= 0
        avgHumCond = HUM_IDEAL - avgHum < 1 and HUM_IDEAL - avgHum >= 0
        SDTempCond = tempSD <= TEMP_IDEAL_SD
        SDHumCond = humSD <= HUM_IDEAL_SD
        if avgTempCond and avgHumCond and SDTempCond and SDHumCond:
            done = True
    # print(statistics.mean(totalEdgeSums))
    # print(statistics.mean(totalNumVisits))
    # print(sum(totalEdgeSums))
    # print(sum(totalNumVisits))
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
        # print(i)
        # es, nv = BFSTrial()
        es, nv = aStarTrial()
        avgEdgeSums.append(es)
        avgNumVisits.append(nv)
        # print(avgEdgeSums)
        # print(avgNumVisits)
        print(statistics.mean(avgEdgeSums))
        print(statistics.mean(avgNumVisits))


    pass

if __name__ == '__main__':
    main()
