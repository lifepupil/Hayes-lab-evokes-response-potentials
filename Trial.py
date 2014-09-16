'''
Created on Jan 15, 2010

@author: Chris
'''

class Trial():
    '''
    classdocs
    '''


    def __init__(self,triggerCh):
        '''
        Constructor
        '''
        self.stimCond = triggerCh
        self.measurementBaseline = 0
        self.trialBlock = ""
        self.electrode = ""
        self.included = ""
        self.columnNames = ""
        self.ordinal = 0
        self.unconverted = [] # a list of unconverted values from an individual ERP trial
        self.converted = [] # a list of converted values from an individual ERP trial

        # these are only temporary values which change each time 
        # a new time range inside which to look is called
        self.maxAmp = 0
        self.latency = 0

        self.date = ""
        self.trialDataString = ""
        self.timeMsecs = []
        
    def getWaveSection(self,start,end):
        startIndex, endIndex = (start + 200)/2,(end + 202)/2
        waveSlice = self.converted[startIndex: endIndex]        
        MaxAmpLat = max(waveSlice)
        MinAmpLat = min(waveSlice)
        
#        print MaxAmpLat, " for ",self.columnNames #, " at ", waveSlice
        self.maxAmp = MaxAmpLat[0]
        self.latency = MaxAmpLat[1]
        
    
           
