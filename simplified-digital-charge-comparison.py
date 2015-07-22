#! /usr/bin/env python2.6                                                     
#
# Author: Tatsu

import sys
import os
import math
import re
import matplotlib
import pylab
import numpy
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
 
maximumVoltage = 0 # The largest value for voltage
maximumVoltageIndex = 0 # Stores the index value of the largest voltage
maximumAmplitudesArray = [] # Stores all the maximum amplitudes for each event for plotting
eventCounter = 0 # Counts the number of events
eventChecker = 0
discriminationParameter = 0
discriminationParameterArray = []
shortIntegralA = 0.1875
shortIntegralB = 0.5
shortIntegralStartIndex = 0
shortIntegralEndIndex = 0
eventIndexEnd = 0
zeroEncountered = 0
 
for line in fileInput:
    event = re.search("Event", line) # Utilizes regex to determine when an event has taken place
    if event:
        eventCounter += 1 # Increments event counter
        if eventCounter > 1:
          shortIntegralStartIndex = math.ceil(shortIntegralA * len(voltageArray))
          shortIntegralEndIndex = math.ceil(shortIntegralB * len(voltageArray))
          discriminationParameter = 0.0
          temporaryAmplitudeHolder = 0.0
          while shortIntegralStartIndex < shortIntegralEndIndex:
             temporaryAmplitudeHolder = float(voltageArray[int(shortIntegralStartIndex)]) - baselineVoltage
             discriminationParameter = discriminationParameter + temporaryAmplitudeHolder**2
             shortIntegralStartIndex += 1
          maximumVoltage = max(voltageArray) # Finds the largest value in the array and sets it as maximumVoltage
          maximumVoltageIndex = voltageArray.index(maximumVoltage) # Finds the index value of maximumVoltage
          maximumAmplitudesArray.append(float(maximumVoltage) - baselineVoltage) # Stores all the amplitudes for each event for plotting
          usefulEvent = 0
          eventChecker = maximumVoltageIndex # Sets the starting point to be the max voltage
          eventIndexEnd = (len(voltageArray) - 1) # Sets the end point to be the end of the array
          while eventChecker < eventIndexEnd:
             if voltageArray[eventChecker] <= baselineVoltage: # Checks if the event is useful
                usefulEvent = 1
                eventChecker = eventIndexEnd # Breaks the while loop
             eventChecker += 1 # Increments the index
          if discriminationParameter == 0.0 or usefulEvent == 0:
             zeroEncountered += 1
             maximumAmplitudesArray.pop()
          else:
             discriminationParameter = numpy.log(discriminationParameter)
             discriminationParameterArray.append(discriminationParameter)
        baselineCounter = 0 # Sets the baslineCounter back to 0 for a new event
        baselineArray = [] # Array to hold the first 20 points
        baselineCounter = 0 # Ensures that 20 points are taken for the baselineArray
        baselineVoltage = 0 # The average of the baselineArray
        averageTemporary = 0 # A temporary variable used for adding the values in baselineArray
        voltageArray = []
        i = 0 # Usage in loops
    else:
       dataList = line.split(",") # Splits the data in each line by the comma
       if len(dataList) == 1:
          next(fileInput)
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
shortIntegralStartIndex = math.ceil(shortIntegralA * len(voltageArray))
shortIntegralEndIndex = math.ceil(shortIntegralB * len(voltageArray))
discriminationParameter = 0.0
temporaryAmplitudeHolder = 0.0
while shortIntegralStartIndex < shortIntegralEndIndex:
   temporaryAmplitudeHolder = float(voltageArray[int(shortIntegralStartIndex)]) - baselineVoltage
   discriminationParameter = discriminationParameter + temporaryAmplitudeHolder**2
   shortIntegralStartIndex += 1
maximumVoltage = max(voltageArray) # Finds the largest value in the array and sets it as maximumVoltage
maximumVoltageIndex = voltageArray.index(maximumVoltage) # Finds the index value of maximumVoltage
maximumAmplitudesArray.append(float(maximumVoltage) - baselineVoltage) # Stores all the amplitudes for each event for plotting
eventChecker = maximumVoltageIndex # Sets the starting point to be the max voltage
eventIndexEnd = (len(voltageArray) - 1) # Sets the end point to be the end of the array
usefulEvent = 0
while eventChecker < eventIndexEnd:
   if voltageArray[eventChecker] <= baselineVoltage: # Checks if the event is useful
      usefulEvent = 1
      eventChecker = eventIndexEnd # Breaks the while loop
   eventChecker += 1 # Increments the index
if discriminationParameter == 0.0 or usefulEvent == 0:
   zeroEncountered += 1
   maximumAmplitudesArray.pop()
else:
   discriminationParameter = numpy.log(discriminationParameter)
   discriminationParameterArray.append(discriminationParameter)
 
matplotlib.pyplot.scatter(maximumAmplitudesArray, discriminationParameterArray) # Plots the maximum amplitudes on x-axis & discrimination parameters on y-axis
matplotlib.pyplot.title('Simplified Digital Charge Comparison Plot')
matplotlib.pyplot.xlabel('Peak Amplitudes')
matplotlib.pyplot.ylabel('Discrimination Parameters')
matplotlib.pyplot.show()
 
print '\n\n'
print '___Additional Information___'
print 'Number of events processed: %d' % eventCounter
print 'Number of events plotted: %d' % len(maximumAmplitudesArray)
print 'Time taken to process data: %f' % (time.time() - startTime), "seconds"
print '\n\n'
 
fileInput.close()
sys.exit(0)
