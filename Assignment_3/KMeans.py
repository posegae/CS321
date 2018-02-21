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

    def __init__(self, k, idFeature, features, allData, labelFeature):
        self.k = k
        self.allData = allData
        self.clusters = [Cluster(idFeature, features, allData) for i in range(k)]
        self.idFeature = idFeature
        self.labelFeature = labelFeature

    def fit(self, labelCandidates):
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
#             print('{}/{}'.format(len(used), len(self.allData)))

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
#                     np.delete(curCluster, row)
                    curCluster.remove(row)
                    numChanged += 1
            # after moving everything, recalculate Means
            for cluster in self.clusters:
                cluster.updateMean()
            print('moved {} rows'.format(numChanged))
            if numRuns > 10:
                break

        print('now assigning clusters their labels')
        # Now that we have all our data points in a cluster, assign a label to
        #  each of them
        #  e. g. one cluster is compliant, another safe, and another NonCompliant
        for labelCandidate in labelCandidates:
            self.assignClusterLabel(labelCandidate)


    def assignClusterLabel(self, candidate):
        '''
        candidate: a string that matches with a class in the feature that you
                    want to predict on (Safe, NonCompliant, Compliant)
        checks percentage membership of the given candidate in each of the
            clusters. Assign the one with the largest proportion the candidate
        '''
        unlabeledClusters = [c for c in self.clusters if c.label == '']

        clusterRows = []
        for cluster in unlabeledClusters:
            clusterRows.append(cluster.getRowsAsNumpy())
        clusterCandidateCounts = []
        for cr in clusterRows:
            clusterCandidateCounts.append(sum([1 if x[self.labelFeature] == candidate else 0 for x in cr  ]))
        candidatePercentages = []
        for i in range(len(clusterCandidateCounts)):
            candidatePercentage = clusterCandidateCounts[i] / len(unlabeledClusters[i].rows)
            candidatePercentages.append(candidatePercentage)
        bestClusterIdx = candidatePercentages.index(max(candidatePercentages))
        unlabeledClusters[bestClusterIdx].label = candidate





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

    def test(self, testSet):
        safeTruePositive = 0
        safeFalsePositive = 0
        safeTrueNegative = 0
        safeFalseNegative = 0
        compliantTruePositive = 0
        compliantFalsePositive = 0
        compliantTrueNegative = 0
        compliantFalseNegative = 0
        noncompliantTruePositive = 0
        noncompliantFalsePositive = 0
        noncompliantTrueNegative = 0
        noncompliantFalseNegative = 0

        for row in testSet:
            predictedCluster = self.findClosestCluster(row)
            if predictedCluster.label == row[self.labelFeature]:
                # these are true positives and true negatives
                if predictedCluster.label == 'Safe':
                    safeTruePositive += 1
                    compliantTrueNegative += 1
                    noncompliantTrueNegative += 1
                elif predictedCluster.label == 'Compliant':
                    safeTrueNegative += 1
                    compliantTruePositive += 1
                    noncompliantTrueNegative += 1
                elif predictedCluster.label == 'NonCompliant':
                    safeTrueNegative += 1
                    compliantTrueNegative += 1
                    noncompliantTruePositive += 1
                else:
                    # this shouldn't happen
                    print('unexpected label in test')
                    exit(0)
            else:
                # these are false positives and false negatives
                p = predictedCluster.label # predicted
                a = row[self.labelFeature] # actual
                if p == 'Safe' and a == 'Compliant':
                    safeFalsePositive += 1
                    compliantFalseNegative += 1
                elif p == 'Safe' and a == 'NonCompliant':
                    safeFalsePositive += 1
                    noncompliantFalseNegative += 1
                elif p == 'Compliant' and a == 'Safe':
                    compliantFalsePositive += 1
                    safeFalseNegative += 1
                elif p == 'Compliant' and a == 'NonCompliant':
                    compliantFalsePositive += 1
                    noncompliantFalseNegative += 1
                elif p == 'NonCompliant' and a == 'Safe':
                    noncompliantFalsePositive += 1
                    safeFalseNegative += 1
                elif p == 'NonCompliant' and a == 'Compliant':
                    noncompliantFalsePositive += 1
                    compliantFalseNegative += 1
                else:
                    print('unexpected label combinations in test')
                    print(p)
                    print(a)

                          
        safePrecision = safeTruePositive / (safeTruePositive + safeFalsePositive)
        safeRecall = safeTruePositive / (safeTruePositive + safeFalseNegative)
        safeF1 = 2 * ((safePrecision * safeRecall) / (safePrecision + safeRecall))
        compliantPrecision = compliantTruePositive / (compliantTruePositive + compliantFalsePositive)
        compliantRecall = compliantTruePositive / (compliantTruePositive + compliantFalseNegative)
        compliantF1 = 2 * ((compliantPrecision * compliantRecall) / (compliantPrecision + compliantRecall))
        noncompliantPrecision = noncompliantTruePositive / (noncompliantTruePositive + noncompliantFalsePositive)
        noncompliantRecall = noncompliantTruePositive / (noncompliantTruePositive + noncompliantFalseNegative)
        noncompliantF1 = 2 * ((noncompliantPrecision * noncompliantRecall) / (noncompliantPrecision + noncompliantRecall))
        
        print('metrics are (precision, recall, f1)')
        print('Safe: {}, {}, {}'.format(safePrecision, safeRecall, safeF1))
        print('Compliant: {}, {}, {}'.format(compliantPrecision, compliantRecall, compliantF1))
        print('NonCompliant: {}, {}, {}'.format(noncompliantPrecision, noncompliantRecall, noncompliantF1))
        
                

        



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
        self.label = ''

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

    def getRowsAsNumpy(self):
        ''' returns the filtered training data set that corresponds to the rows
            that this cluster contains '''
        return self.allData[[(x[self.idFeature] in self.rows) for x in self.allData]]




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

    c = KMC(3, 'HeatMiser_ID', ['Distance_Feature', 'Speeding_Feature'], trainSet, 'OSHA')
    c.fit(['Compliant', 'NonCompliant', 'Safe'])
    c.test(testSet)
    for cluster in c.clusters:
        print(len(cluster.rows))
        print(cluster.mean)
        print(cluster.label)


if __name__ == '__main__':
    main()
