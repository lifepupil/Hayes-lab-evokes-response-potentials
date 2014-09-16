'''
'''

#from operator import add
from math import *
from decimal import *
from string import *

class Trials:
    '''
    Trials class - this class is used to hold collections of trials meeting user-defined
    criteria for desired trial types, e.g. all trials with 'rare' stimulus condition and at
    the 'Pz' electrode
    '''

    def __init__(self,electrode,stimCond,included,excluded):
        '''
        Constructor
        '''
        self.trials = []
        self.averages = [0]*1000
        self.stDev = [0]*1000
        self.SEM = [0]*1000

        self.electrode = electrode
        self.stimCond = stimCond
        self.measurementBaseline = 0
        self.included = included
        self.excluded = excluded
        self.fileLabel = electrode+"-"+stimCond

        if self.included == "True": self.fileLabel = self.fileLabel + "-Incl"
        if self.excluded == "False": self.fileLabel = self.fileLabel + "-Excl"
                
    def createTimeLists(self):
        print self.included
        print self.fileLabel
        self.timeList =[[0]*len(self.trials) for t in range(1000)]
        
        for thisTime in range(1000):                
            for thisTrial in range(len(self.trials)):
                self.timeList[thisTime][thisTrial] = (self.trials[thisTrial].converted[thisTime])
        
    def calculateStatistics(self):
        for eachTime in range(1000):
            self.averages[eachTime] = sum(self.timeList[eachTime])/len(self.trials)
#            print self.averages[eachTime]
#            numerator = [sum(Decimal(str(uA - self.averages[eachTime]))^2.0) for uA in self.timeList[eachTime]]
#            self.stDev[eachTime] = (numerator/(len(self.timeList) - 1))^0.5 

# formula for standard deviation = ( sum ( (mean - eachTime value)^2 )/ n )^0.5        
#            for eachTrial in range(len(self.timeList[eachTime])):           

        
    def getAvg(self):
        return self.averages
    
#    def getStDev(self):
#        return self.stDev
#    
#    def getSEM(self):
#        return self.SEM
