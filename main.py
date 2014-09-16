'''
Created on Jan 20, 2010

@author: Chris

January 25,2010 - added date to Trial object, edited Baby class to take a filename parameter, 
and modified ExtractData method so that it will take raw data .TXT files instead of requiring
users to save these files as a .CSV. 
   
'''
from auxClasses import *
from graphics import *
from Babies import *
#from rpy import *
from os import listdir


def main():
    
    gui = GraphWin("",350,300)
    gui.setCoords(0, 0, 20, 20)
    filePath = "C:/data/"
    
#    Text(Point(5,2), "Input file name:").draw(gui)        
    
    Rectangle(Point(0.25,19.5),Point(19.75,15.5)).draw(gui)
    extractB = Button(gui,Point(15,19),Point(19.5,16.5))
    extractB.setLabel("EXTRACT")     
    fileText = Textbox(gui,9.5,18,20)
    fileText.setValue("") #("enter filename.txt here")
    Text(Point(2,18),filePath).draw(gui)    
    writeAll = Textbox(gui,14,16.5,1)
    writeAll.setValue("n")
    Text(Point(7,16.5),"Write all trial data to .CSV file?").draw(gui)
    
    Rectangle(Point(0.25,15.75),Point(19.75,5)).draw(gui)    
    Text(Point(10,15),"Get selected trial types:").draw(gui)    
    writeB = Button(gui,Point(15,11.5),Point(19.5,9)) # need to edit auxClasses so that button can be disabled 
    writeB.setLabel("WRITE")                    # until after extraction operation
    
    writeSelected = Textbox(gui,17,7,1)
    writeSelected.setValue("Y")
    Text(Point(8,7),"Write selected trial data to .CSV file?").draw(gui)
    
    stimulus = Textbox(gui,12,13.5,6)
    stimulus.setValue("rare")
    Text(Point(5,13.5),"Stimulus condition:").draw(gui)    
    
    electrode = Textbox(gui,12,12,6)
    electrode.setValue("Pz")
    Text(Point(7,12),"Electrode:").draw(gui)    
    
    included = Textbox(gui,12,10.5,1)
    included.setValue("X")
    Text(Point(7,10.5),"Included trials:").draw(gui)    
    
    excluded = Textbox(gui,12,9,1)
    excluded.setValue("")
    Text(Point(7,9),"Excluded trials:").draw(gui)      

    quitB = Button(gui,Point(1,1),Point(5.5,3.5))
    quitB.setLabel("QUIT")
    
    startTime = Textbox(gui,15,2,5)
    startTime.setValue("150") #("enter filename.txt here")
    endTime = Textbox(gui,18,2,5)
    endTime.setValue("450") #("enter filename.txt here")
    
    
    done = Text(Point(10,2),"DONE")
    started = Text(Point(10,2),"STARTED")    

    while True:
        click = gui.getMouse()
        
        if quitB.Clicked(click):
            gui.close()
            break
        
        if extractB.Clicked(click):
            done.undraw()
            started.draw(gui)
#            filename = fileText.getValue()         
#            b = Baby(filePath,filename)
#            b.extractData()
#            b.getLatencyMaxAmplitude(int(startTime.getValue()),int(endTime.getValue()))
#            if writeAll.getValue() == "Y" or writeAll.getValue() == "y": b.writeAllTrials()                            
            
            fileNames = listdir(filePath)
            fileNum = len(fileNames)
            i=0
            while i < fileNum:
                if fileNames[i][-4:] != ".txt":
                    del fileNames[i]
                    fileNum = len(fileNames)
                else:
                    fileNames[i] = "/"+fileNames[i]
                    i=i+1

#            for thisFile in range(len(fileNames)):
#                b = Baby(filePath,fileNames[thisFile])
#                b.extractData()
#                print fileNames[thisFile]
#                trialList = ""
#                filterCriteria = ["trialBlock"]
#                criteriaVal = ""
#                b.getTrialTypes(trialList,filterCriteria,criteriaVal) # this collects trials for later concatenation; unrem only for actual trials

            b = Baby(filePath,"fileNames[0]") # unrem only if concat LW data
            b.getLastWaveData() # unrem this only if concatenating LastWave generated data signals

            
            started.undraw()
            done.draw(gui)
            
        if writeB.Clicked(click):
            done.undraw()
            started.draw(gui)
                        
            if writeSelected.getValue() == "Y" or writeSelected.getValue() == "y":      
#                avgfile = str(fileText.getValue())

                b.newTrialSet(electrode.getValue(),stimulus.getValue(),included.getValue(),excluded.getValue())
                b.trialSets[len(b.trialSets)-1].getAvg()
#                b.trialSets[0].getStDev()  
                b.writeTrialSet(b.trialSets[len(b.trialSets)-1],b.trialSets[len(b.trialSets)-1].fileLabel)

            
            started.undraw()
            done.draw(gui)

            print "done"

## TEST BLOCK FOR extractData METHOD >
#    trialList = b.getTrials()    
#    print len(trialList)
#    num = 1163
#    print "stimcond = "+str(trialList[num].stimCond)
#    print "mb = ",trialList[num].measurementBaseline
#    print "trialblock = "+trialList[num].trialBlock
#    print "electrode = "+str(trialList[num].electrode)
#    print "included = "+trialList[num].included
#    print "col = "+trialList[num].columnNames
#    print "ordinal = "+str(trialList[num].ordinal)
#    print "date = "+(trialList[num].date)
#    print "unconv = ",trialList[num].unconverted
#    print "conv = ",trialList[num].converted
## TEST BLOCK FOR extractData METHOD />
#    print "done"

#if __name__ == '__main__':
#    pass

main()