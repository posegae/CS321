'''
KMeans.py
Ju Yun Kim and Emma Posega Rappleye
CS 321
Assignment 3, for extra credit
Implements K Means Clustering
'''

import numpy as np
import math
import random

class KMC:
    ''' KMC = K Means Clustering
        Contains the cluster objects'''

    def __init__(self, k, idFeature, features, allData):
        self.k = k
        self.allData = allData
        self.clusters = [Cluster(idFeature, features, allData) for i in range(k)]
        self.idFeature = idFeature

    def fit(self):
        '''fits a clustering model based on the data
            trainingData is a numpy array'''
        # each cluster gets an initial row randomly
        used = []
        for cluster in self.clusters:
            toAdd = self.allData[random.randint(0, len(self.allData) - 1)]
            while toAdd in used:
                toAdd = self.allData[random.randint(0, len(self.allData) - 1)]
            used.append(toAdd)
            cluster.add(toAdd)
            cluster.updateMean()
            # print([len(x.rows) for x in self.clusters])
            # print(cluster.rows)

        # initial pass: put each row into the closest cluster
        for row in self.allData:
            if row in used:
                # don't use the initial row more than once
                continue
            closestCluster = self.findClosestCluster(row)
            closestCluster.add(row)
            closestCluster.updateMean()
            used.append(row)
            print('{}/{}'.format(len(used), len(self.allData)))

        # check passes: check that each row is in the closest cluster
        numChanged = -1
        numRuns = 0
        while numChanged != 0:
            numChanged = 0
            numRuns += 1
            for row in self.allData:
                closestCluster = self.findClosestCluster(row)
                curCluster = self.findCurCluster(row)
                if closestCluster != curCluster:
                    closestCluster.add(row)
                    numChanged += 1
            # after moving everything, recalculate Means
            for cluster in self.clusters:
                cluster.updateMean()
            print('moved {} rows'.format(numChanged))
            if numRuns > 10:
                break




    def findClosestCluster(self, row):
        ''' return the cluster object closest to the given row '''
        distances = [c.getDistToMean(row) for c in self.clusters]
        # print(distances)
        return self.clusters[distances.index(min(distances))]

    def findCurCluster(self, row):
        ''' return the cluster that this row belongs to '''
        for cluster in self.clusters:
            if row[self.idFeature] in cluster.rows:
                return cluster




class Cluster:
    def __init__(self, idFeature, features, allData):
        '''rows is the list of rows, represented by their id, that are contained
            in this cluster.
            idFeature is a string that can be used to index into the ndarray to
            access the ID of the row
            features is a list of strings that can be used to index into the
            ndarray to access the relevant values of the rows
            allData is the whole training set. Cluster indexes into this with
            the contents of self.rows'''
        self.rows = []
        self.idFeature = idFeature
        self.mean = None
        self.allData = allData
        self.features = features
        self.dimension = len(features)

    def add(self, row):
        ''' adds the passed in row's id into the rows list '''
        # self.rows = row[self.idFeature]
        self.rows.append(row[self.idFeature])

    def remove(self, row):
        ''' removes the passed in row's id from the rows list '''
        self.rows.remove(row[self.idFeature])

    def updateMean(self):
        ''' iterate through all rows, and calculate the mean for each dimension
            of the data '''
        self.mean = [0] * self.dimension # reset the means
        # print([(x[self.idFeature] in self.rows) for x in self.allData])
        rowsAsNumpy = self.allData[[(x[self.idFeature] in self.rows) for x in self.allData]]
        # print(rowsAsNumpy)
        for row in rowsAsNumpy:
            for i in range(self.dimension):
                # print(self.mean)
                # print(self.features)
                # print(row)
                self.mean[i] += row[self.features[i]]
        self.mean = [x / len(self.rows) for x in self.mean] # take the average

    def getDistToMean(self, row):
        ''' return the distance from the given row to the mean '''
        rowValues = [row[x] for x in self.features]
        valDifferences = math.sqrt(sum(list(map(lambda x: (x[1] - x[0]) ** 2, zip(rowValues, self.mean)))))
        return valDifferences




def main():
    # 3436 safe   .859
    # 415 Compliant .10395
    # 149 NonCompliant .03725

    # data is a numpy array
    # data[1] accesses the second row
    # data[1]['HeatMiser_ID'] accesses the second row's id.
    dt = np.dtype([('HeatMiser_ID', np.unicode_, 16), ('Distance_Feature', np.float), ('Speeding_Feature', np.int_), ('Location', np.unicode_, 16), ('OSHA', np.unicode_, 16)])
    data = np.loadtxt('HW3_Data.txt', dtype=dt, delimiter='\t', skiprows=1)


    trainRatio = .7
    trainSize = math.floor(data.shape[0] * trainRatio)
    # trainSize = 500
    trainSet = data[:trainSize]
    testSet = data[trainSize:]

    c = KMC(3, 'HeatMiser_ID', ['Distance_Feature', 'Speeding_Feature'], trainSet)
    c.fit()
    for cluster in c.clusters:
        print(len(cluster.rows))
        print(cluster.mean)


if __name__ == '__main__':
    main()
