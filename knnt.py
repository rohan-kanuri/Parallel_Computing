# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 12:25:09 2014

@author: mario
"""
import timeit
import csv
import random
import math
import operator

import thread

from threading import Thread

class thread_it(Thread):
    def __init__ (self,param):
        Thread.__init__(self)
        self.param = param
  

# Split the data into training and test data
def loadDataset(filename, split, trainingSet=[] , testSet=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset)):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])
                
def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)
    
def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key = operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors
    
def getResponse(neighbors):
    # Creating a list with all the possible neighbors
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]
    
def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0
                
def main():
    threads = []
    output = []
    trainingSet=[]
    testSet=[]
    split = 0.67
    start = timeit.default_timer()
    loadDataset('iris.data', split, trainingSet, testSet)
    #print 'Train set: ' + repr(len(trainingSet))
    #print 'Test set: ' + repr(len(testSet))    
    predictions=[]
    k = 3
    j=0
    for x in range(len(testSet)):
        current = thread_it(j)
        threads.append(current)
        current.start()
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        j=j+1
    for t in threads:
      t.join()
    accuracy = getAccuracy(testSet, predictions)
    accuracy = getAccuracy(testSet, predictions)
    stop = timeit.default_timer()
    print stop - start
    print 'Accuracy: ', accuracy

main()
