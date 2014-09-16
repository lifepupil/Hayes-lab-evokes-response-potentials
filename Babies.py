'''
Created on Jan 15, 2010

@author: Chris
'''

import string
from Trial import *
from Trials import *
from graphics import *

class Baby:
    '''
    Baby class is created with initialized instance variables for
    important experiment identification information for future use
    in analyses across multiple babies, and a list to contain all 
    individual ERP trials.
    '''
    def __init__(self,filePath,filename):
        '''
        Constructor
        '''
        self.ID = ""
        self.trials = []
        self.group = ''
        self.filePath = filePath+filename
        self.filename = filename        
        self.totalTrials = 0
        
        self.trialSets = []  # a list to hold Trials objects (collections of trials meeting user criteria 
        
        self.labels = '"BabyID","Trial ID","Sequence #","Stimulus","Included","Electrode","MaxAmp","Latency",'
        for times in range(-200,1800,2):
            self.labels = self.labels + str(times) + " ms ,"
        self.labels = self.labels + "\n"
        
   
    ''' 
    searches through structured raw data file output from ERP machine
    to get all baby and individual trial information gathered during ERP session,
    and organize these data into a collection of Trial objects contained by a
    Baby object.
    '''
    def extractData(self):
        PI = False # marker for PatientInformation text section
        SWSP = False # SiteWaveStatusPrivate
        GW = False # GatherWave
        lastTrial = 0
        trialCounter = 0
        currentCount = 0
        date = ""

        sensitivity = 50
        waveStart = 0 # default = 20; this screens out the first 20 values (0 to 19) of the 1024 values in each ERP trial 
        waveEnd = 1024 # default = 1021; this screens out the last 4 values (1021 to 1024) in each ERP trial 
        
        electrodes = {'1':'Fz','2':'Cz','3':'Pz','4':'unspecified electrode 4','5':'unspecified electrode 5','6':'unspecified electrode 6','7':'unspecified electrode 7','8':'unspecified electrode 8'}
        included = {'ON':'True','OFF':'False'}
        stimuli = {'0':'rare','1':'freq'}
        
            
        for line in open(self.filePath,'r'):
            line = line.rstrip()
            parts = line.split(',')
            marker = parts[0].strip('"') 
                                  
            if PI == True:
                if marker == "ID No.": self.ID = parts[1].strip('"')
                elif marker == "Name" and self.ID == "": self.ID = parts[1].strip('"')
                elif marker == "Date of Examination": 
                    date = parts[1].strip('"')
                    PI = False
                           
            if SWSP == True:
                if marker == "Wave Name": 
                    tempWaveName = parts[1].strip('"')
                elif marker == "Trigger Ch": # stimulus type rare=0 freq=1
                    del parts[0]                    
                    for TC in range(len(parts)): # TC is 'trigger channel'/stimulus type for each individual trial
                        trial = Trial(stimuli[parts[TC]])
                        self.totalTrials = self.totalTrials + 1 # keeps track of total number of trials for this baby
                        trial.trialBlock = tempWaveName[0] # stores which trial block this trial occurred in
                        trial.electrode = electrodes[tempWaveName[1]] # stores recording electrode for this trial
                        trial.ordinal = self.totalTrials 
                        trial.date = date                
                        self.trials.append(trial) # adds this trial to this baby's list of trials
                elif marker == "Measurement Baseline":
                    del parts[0]
                    for MB in range(len(parts)):
                        self.trials[MB + lastTrial].measurementBaseline = float(parts[MB])
                elif marker == "Add Flag":
                    del parts[0]
                    for AF in range(len(parts)):
                        parts[AF] = parts[AF].strip('"')
                        self.trials[AF + lastTrial].included = included[parts[AF]]
                    lastTrial = len(self.trials)


            if GW == True: # Start of individual trial data at "Gather Wave"     
                if len(marker) > 2 and marker[2] == "-": # used to detect column labels, e.g. "A1-1"           
                    for trialLabel in range(len(parts)):
                        self.trials[trialLabel + trialCounter].columnNames = parts[trialLabel].strip('"')
                        currentCount = currentCount + 1
                elif marker != "" and marker != "Wave End" and int(marker) > waveStart and int(marker) <= waveEnd:
                    if int(marker) > 20 and int(marker) < 1021: # to correctly mark time
                        time = ((int(marker) - 20)*2) - 200 - 2 # correct time (msec) requires waveStart = 20
                    else: 
                        time = "-"
#                    print marker+" "+str(time)
                    
                    del parts[0]
                    for v in range(len(parts)): # v is raw value for a trial at same timepoint 'time' 
                        unconvertedValue = (int(parts[v])/6553.5) * sensitivity
                        self.trials[v + trialCounter].unconverted.append((unconvertedValue,time))
#                        convert = ((unconvertedValue - self.trials[v + trialCounter].measurementBaseline)/6553.5) * sensitivity
#                        self.trials[v + trialCounter].converted.append((convert,time))
                        
                elif marker == "Wave End":
                    trialCounter = trialCounter + currentCount
                    currentCount = 0

            if marker == "*Patient Information": PI,SWSP,GW = True,False,False
            elif marker == "*Site Wave Status Private": PI,SWSP,GW = False,True,False
            elif marker == "*Gather Wave": PI,SWSP,GW = False,False,True
        
    ''' This method assumes that the trial list data are sorted by time sequence of trial and electrode '''
    def getTrialTypes(self,trialList,trialAttr,attrVal):
        
        filteredList = []
        if trialList == "": trialList = self.trials # allows use of this method with filtered lists as well as self.trials
        if attrVal == "": attrVal = getattr(trialList[0],trialAttr[0]) # gets attrVal of first trial if an empty string passed
        electrodeVal = trialList[0].electrode
#        stimTest = 'rare'
        
        for thisAttr in range(len(trialAttr)):
#            [filteredList.append(t) for t in trialList if getattr(t,trialAttr[thisAttr])==attrVal]
#            [i[0] for i in trialList[thisTrial].unconverted]
#            print trialAttr[thisAttr]
            for thisTrial in range(len(trialList)):
                criteriaTest = getattr(trialList[thisTrial],trialAttr[thisAttr])
#                print criteriaTest
                electrodeTest = trialList[thisTrial].electrode
                stimVal = trialList[thisTrial].stimCond
                 
                if criteriaTest == attrVal and electrodeTest == electrodeVal:                    
#                    filteredList.append(trialList[thisTrial].unconverted)
#                    if stimVal == stimTest: 
                    filteredList.append([i[0] for i in trialList[thisTrial].unconverted]) # takes the 0th value from the tuple (uvolt,time) for each time in trial
                    print trialList[thisTrial].stimCond,trialList[thisTrial].columnNames 
                        
                else:
#                    print filteredList[-1]
#                    print len(filteredList)

                    self.concatenateTrials(filteredList,trialAttr[thisAttr],attrVal,electrodeVal)
                    attrVal = criteriaTest # getattr(trialList[thisTrial],trialAttr[thisAttr])
                    electrodeVal = electrodeTest # resets electrode value to the one for the latest trial 
                    filteredList = []
                    filteredList.append([i[0] for i in trialList[thisTrial].unconverted])
#                    print filteredList

            self.concatenateTrials(filteredList,trialAttr[thisAttr],attrVal,electrodeVal)

  
    def getLastWaveData(self):
        LW = []
        path = "C:/Users/Chris/Desktop/LastWave_3_1.windows/LastWave_3_1/1Chris/size 1024 H 0.8/"
        fileName = "size1024 "
        H = "H_0.8"
        fileNum = 88
        
        for file in range(1,fileNum+1):
            arr = []
            f = open(path+fileName+str(file)+" "+H,"r")
            print path+fileName+str(file)+" "+H
            for line in f:
                try:
                    arr.append(float(line))
                except ValueError: 
                    pass
            LW.append(arr)
            
#        print LW[-1][-1]
        self.concatenateTrials(LW,H[:1],H[2:5],"concat")
        
  
    ''' aligns waveforms for each trial and concatenates them'''    
    def concatenateTrials(self,trialList,attr,attrVal,electrodeVal):
        try: concatList = trialList[0] # concatenation list
        except: return
        lastPrevVal = concatList[-1] # gets last value in the 0th trial to prime loop

        # removed whitespace so LastWave script won't choke on filename
        fname = self.filename[:-4]
        fname = fname.translate(None," ")

#        fileName = fname+"_"+attr+"_"+attrVal+"_"+electrodeVal # unrem for concatenating actual trial data
#        path = "C:/data/concatenated trials/"+electrodeVal # this too
        
        fileName = "size1024_"+attr+"-"+attrVal+"_"+electrodeVal # unrem for concatenating LastWave generated faux trial data
        path = "C:/Users/Chris/Desktop/LastWave_3_1.windows/LastWave_3_1/1Chris/size 1024 H 0.8/" # this too
        
        f = open(path+fileName,"w")
        
        for thisTrial in range(1,len(trialList)):
            firstNextVal = trialList[thisTrial][0]
            diff = lastPrevVal - firstNextVal
#            print lastPrevVal,firstNextVal,diff
            concatList.extend([diff + val for val in trialList[thisTrial]])
            lastPrevVal = concatList[-1]
        
        [f.write(str(val)+"\n") for val in concatList]
        print f.name
        f.close()
        
        

    ''' pulls out the maximum amplitude and latency to it for each individual trial'''
    def getLatencyMaxAmplitude(self,start,end):
        trialNum = len(self.trials)
        for t in range(trialNum):
            self.trials[t].getWaveSection(start,end)
            
        
    
    
    '''
    creates a Trials object.
    '''    
    def newTrialSet(self, userElectrode,userStimCond, userIncluded, userExcluded):
        # take search parameters for trial type
        # takes start and end times as parameters also
        # creates a Trials object and passes these arguments to it
        # methods of Trials which:
        # - look through all trials (filter) for criteria-meeting ones and add them to a list
        # - return average across trials
        # - return SEM across averaged trials
        # - can call the writeTrials() method to output selected trials into .CSV file         
        
        if userIncluded == "X": userIncluded = "True"
        if userExcluded == "X": userExcluded = "False"
        
        self.trialSets.append(Trials(userElectrode,userStimCond,userIncluded,userExcluded))
        
        for eachTrial in range(len(self.trials)):
            if self.trials[eachTrial].electrode == userElectrode and \
            self.trials[eachTrial].stimCond ==userStimCond:
                if self.trials[eachTrial].included == userIncluded or \
                self.trials[eachTrial].included == userExcluded:
                    self.trialSets[len(self.trialSets)-1].trials.append(self.trials[eachTrial])
        
        self.trialSets[len(self.trialSets)-1].createTimeLists()
        self.trialSets[len(self.trialSets)-1].calculateStatistics()        

    '''
    returns entire current list of individual trials.
    '''        
    def getTrials(self):
        return self.trials
    
    '''
    goes through every Trial object in the list of individual trials,
    creates a data string of its relevant data formatted to be useful 
    when opened in a spreadsheet, and writes to a .CSV file referencing
    the baby ID.
    
    GOALS:
    -    edit writeTrials so that it can be used to write a user-defined
        subset of individual trials to a user-defined file name.
    -    edit the time (ms) labels to match any time-sectioned trial data
    -    
    '''
    def writeAllTrials(self):        
        f = open("C:\data\\babies\\All_"+self.filename[:-4]+"_trials.CSV","w") # [:-4] removes ".txt" from string
        f.write(self.labels)
#        except:
#            msg = GraphWin("PROBLEM",200,50)
#            Text(Point(100,25),"Change filename to remove non-alphanumerics").draw(msg)

        
        for eachTrial in range(len(self.trials)):
            nextLine = ""
            nextLine = nextLine + self.ID + ","
            nextLine = nextLine + self.trials[eachTrial].columnNames + ","
            nextLine = nextLine + str(self.trials[eachTrial].ordinal) + ","
            nextLine = nextLine + self.trials[eachTrial].stimCond + ","
            nextLine = nextLine + self.trials[eachTrial].included + ","
            nextLine = nextLine + self.trials[eachTrial].electrode + ","
            nextLine = nextLine + str(self.trials[eachTrial].maxAmp) +  ","
            nextLine = nextLine + str(self.trials[eachTrial].latency) + ","
            
            for uVolts in range(len(self.trials[eachTrial].unconverted)):
                nextLine = nextLine + str(self.trials[eachTrial].unconverted[uVolts][0]) + ","
            nextLine = nextLine[:-1] + "\n" 
            f.write(nextLine)
    
    def writeTrialSet(self,trialSet,fileLabel):      
        f = open("C:\data\\babies\\"+self.filename[:-4]+"_avgs_"+fileLabel+"_trials.CSV","w")
        f.write(self.labels)
#        except:
#            msg = GraphWin("PROBLEM",200,50)
#            Text(Point(100,25),"Change filename to remove non-alphanumerics").draw(msg)

#        print len(trialSet)
                
        for eachTrial in range(len(trialSet.trials)):
            nextLine = ""
            nextLine = nextLine + self.ID + ","
            nextLine = nextLine + trialSet.trials[eachTrial].columnNames + ","
            nextLine = nextLine + str(trialSet.trials[eachTrial].ordinal) + ","
            nextLine = nextLine + trialSet.trials[eachTrial].stimCond + ","
            nextLine = nextLine + trialSet.trials[eachTrial].included + ","
            nextLine = nextLine + trialSet.trials[eachTrial].electrode + ","
            
            for uVolts in range(len(trialSet.averages)):
                nextLine = nextLine + str(trialSet.trials[eachTrial].converted[uVolts]) + ","            
            nextLine = nextLine[:-1] + "\n" 
            f.write(nextLine)
                    
        f.write("\n")
        
        nextLine = "Averages:,,,,,,"
        for uVolts in range(len(trialSet.averages)):
            nextLine = nextLine + str(trialSet.averages[uVolts]) + ","            
        nextLine = nextLine[:-1] + "\n" 
        f.write(nextLine)

            
            

    
