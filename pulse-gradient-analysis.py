#! /usr/bin/env python2.6                                                     
#
# Author: Tatsu

import sys
import os
import math
import re
import matplotlib
import pylab
import time
 
if len(sys.argv) < 2:
   print "Usage: ", sys.argv[0], "<file>"
   sys.exit(1)
 
if not os.path.exists(sys.argv[1]):
   print "%s does not exist" % (sys.argv[1],)
   sys.exit(1)
 
if not os.path.isfile(sys.argv[1]):
   print "%s is not an ordinary file" % (sys.argv[1],)
   sys.exit(1)
 
if not os.access(sys.argv[1], os.R_OK):
   print "%s is not readable" % (sys.argv[1],)
   sys.exit(1)
 
startTime = time.time() # Starts timing the program
fileInput = open(sys.argv[1], "r") # Opens whatever file you have as the argument
 
sampleNumber = 24 # Number of samples
sampleIndex = 0 # Sample index value
maximumVoltage = 0 # The largest value for voltage
maximumVoltageIndex = 0 # Stores the index value of the largest voltage
maximumAmplitudesArray = [] # Stores all the maximum amplitudes for each event for plotting
sampleAmplitudesArray = [] # Stores all the sample amplitudes for each event for plotting
eventCounter = 0 # Counts the number of events
eventChecker = 0 # Used to determine if voltage after max stays above baseline- in which case it is discarded
eventIndexEnd = 0 # Used to determine if voltage after max stays above baseline- in which case it is discarded
 
for line in fileInput:
    event = re.search("Event", line) # Utilizes regex to determine when an event has taken place
    if event:
        eventCounter += 1 # Increments event counter
        if eventCounter > 1:
          maximumVoltage = max(voltageArray) # Finds the largest value in the array and sets it as maximumVoltage
          maximumVoltageIndex = voltageArray.index(maximumVoltage) # Finds the index value of maximumVoltage
          maximumAmplitudesArray.append(float(maximumVoltage) - baselineVoltage) # Stores all the amplitudes for each event for plotting
          sampleIndex = maximumVoltageIndex + sampleNumber # Calculates the index value of the sample
          if sampleIndex > len(voltageArray): # Ensures that the sample index does not exceed the size of the array
             maximumAmplitudesArray.pop() # Removes the last value in the array
          else:
             sampleAmplitudesArray.append(float(voltageArray[sampleIndex]) - baselineVoltage) # Stores all the sample amplitudes for each event for plotting
          eventChecker = maximumVoltageIndex # Sets the starting point to be the max voltage
          eventIndexEnd = (len(voltageArray) - 1) # Sets the end point to be the end of the array
          usefulEvent = 0
          while eventChecker < eventIndexEnd:
             if voltageArray[eventChecker] <= baselineVoltage: # Checks if the event is useful
                usefulEvent = 1
                eventChecker = eventIndexEnd # Breaks the while loop
             eventChecker += 1 # Increments the index
          if usefulEvent == 0:
             maximumAmplitudesArray.pop()
             sampleAmplitudesArray.pop()
        baselineCounter = 0 # Sets the baselineCounter back to 0 for a new event
        baselineArray = [] # Array to hold the first 20 points
        baselineCounter = 0 # Ensures that 20 points are taken for the baselineArray
        baselineVoltage = 0 # The average of the baselineArray
        averageTemporary = 0 # A temporary variable used for adding the values in baselineArray
        i = 0 # Usage in loops
        voltageArray = [] # Stores all the voltage values in an array
    else:
       dataList = line.split(",") # Splits the data in each line by the comma
       if len(dataList) == 1: # Checks for empty lines stored as '\n'
          next(fileInput) # Skips the line
          dataList = line.split(",") # Splits the data in each line by the comma
       voltage = abs(float(dataList[1])) # Takes the second data value stored in the list
       voltageArray.append(voltage) # Adds a new voltage data value to the array
       if baselineCounter != 21: # To ensure that 20 points are taken for the baselineArray
          baselineArray.append(voltage) # Adds a new voltage data value to the array
          baselineCounter += 1 # Increments the baselineCounter
       else:
          while i != 20: # Goes from i = 0 to i = 19
            averageTemporary = averageTemporary + float(baselineArray[i]) # Converts the values in the baselineArray into integers and adds them up
            i += 1 # Increments i
          baselineVoltage = averageTemporary / 20 # Takes the average of the baselineArray
           
### This final part is to catch the last event ###
maximumVoltage = max(voltageArray) # Finds the largest value in the array and sets it as maximumVoltage
maximumVoltageIndex = voltageArray.index(maximumVoltage) # Finds the index value of maximumVoltage
maximumAmplitudesArray.append(float(maximumVoltage) - baselineVoltage) # Stores all the amplitudes for each event for plotting
sampleIndex = maximumVoltageIndex + sampleNumber # Calculates the index value of the sample
sampleAmplitudesArray.append(float(voltageArray[sampleIndex]) - baselineVoltage) # Stores all the sample amplitudes for each event for plotting
usefulEvent = 0
while eventChecker < eventIndexEnd:
   if voltageArray[eventChecker] <= baselineVoltage: # Checks if the event is useful
      usefulEvent = 1
      eventChecker = eventIndexEnd # Breaks the while loop
   eventChecker += 1 # Increments the index
if usefulEvent == 0:
   maximumAmplitudesArray.pop()
   sampleAmplitudesArray.pop()
 
matplotlib.pyplot.scatter(maximumAmplitudesArray, sampleAmplitudesArray) # Plots the maximum amplitudes on x-axis and sample amplitudes on y-axis
matplotlib.pyplot.title('Pulse Gradient Analysis Plot (N = %d)' % sampleNumber)
matplotlib.pyplot.xlabel('Peak Amplitudes')
matplotlib.pyplot.ylabel('Sample Amplitudes')
matplotlib.pyplot.show()
 
print '\n\n'
print '___Additional Information___'
print 'Number of events processed: %d' % eventCounter
print 'Number of events plotted: %d' % len(maximumAmplitudesArray)
print 'Time taken to process data: %f' % (time.time() - startTime), "seconds"
print '\n\n'
 
fileInput.close()
sys.exit(0)
