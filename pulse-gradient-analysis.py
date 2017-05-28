#! /usr/bin/env python3                                                     
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
   print("Usage: ", sys.argv[0], "<file>")
   sys.exit(1)
 
if not os.path.exists(sys.argv[1]):
   print("%s does not exist" % (sys.argv[1],))
   sys.exit(1)
 
if not os.path.isfile(sys.argv[1]):
   print("%s is not an ordinary file" % (sys.argv[1],))
   sys.exit(1)
 
if not os.access(sys.argv[1], os.R_OK):
   print("%s is not readable" % (sys.argv[1],))
   sys.exit(1)

class PulseGradientAnalysis:

   def __init__(self):
      
      self.startTime = time.time() # Starts timing the program
      self.sampleNumber = 24 # Number of samples
      self.sampleIndex = 0 # Sample index value
      self.maximumVoltage = 0 # The largest value for voltage
      self.maximumVoltageIndex = 0 # Stores the index value of the largest voltage
      self.maximumAmplitudesArray = [] # Stores all the maximum amplitudes for each event for plotting
      self.sampleAmplitudesArray = [] # Stores all the sample amplitudes for each event for plotting
      self.eventCounter = 0 # Counts the number of events
      self.eventChecker = 0 # Used to determine if voltage after max stays above baseline- in which case it is discarded
      self.eventIndexEnd = 0 # Used to determine if voltage after max stays above baseline- in which case it is discarded
      self.dataList = []

   def process_data(self):

      with open(sys.argv[1], "r") as fileInput:
         for line in fileInput:
             self.event = re.search("Event", line) # Utilizes regex to determine when an event has taken place
             if self.event:
                 self.eventCounter += 1 # Increments event counter
                 if self.eventCounter > 1:
                    self.event_processor()
                 self.baselineCounter = 0 # Sets the baselineCounter back to 0 for a new event
                 self.baselineArray = [] # Array to hold the first 20 points
                 self.baselineCounter = 0 # Ensures that 20 points are taken for the baselineArray
                 self.baselineVoltage = 0 # The average of the baselineArray
                 self.averageTemporary = 0 # A temporary variable used for adding the values in baselineArray
                 self.i = 0 # Usage in loops
                 self.voltageArray = [] # Stores all the voltage values in an array
             else:
                 self.dataList = line.split(",") # Splits the data in each line by the comma
                 if len(self.dataList) == 1: # Checks for empty lines stored as '\n'
                    next(fileInput) # Skips the line
                    self.dataList = line.split(",") # Splits the data in each line by the comma
                 self.voltage = abs(float(self.dataList[1])) # Takes the second data value stored in the list
                 self.voltageArray.append(self.voltage) # Adds a new voltage data value to the array
                 if self.baselineCounter != 21: # To ensure that 20 points are taken for the baselineArray
                    self.baselineArray.append(self.voltage) # Adds a new voltage data value to the array
                    self.baselineCounter += 1 # Increments the baselineCounter
                 else:
                    while self.i != 20: # Goes from i = 0 to i = 19
                       self.averageTemporary = self.averageTemporary + float(self.baselineArray[self.i]) # Converts the values in the baselineArray into integers and adds them up
                       self.i += 1 # Increments i
                    self.baselineVoltage = self.averageTemporary / 20 # Takes the average of the baselineArray
         self.event_processor()

   def event_processor(self):

      self.maximumVoltage = max(self.voltageArray) # Finds the largest value in the array and sets it as maximumVoltage
      self.maximumVoltageIndex = self.voltageArray.index(self.maximumVoltage) # Finds the index value of maximumVoltage
      self.maximumAmplitudesArray.append(float(self.maximumVoltage) - self.baselineVoltage) # Stores all the amplitudes for each event for plotting
      self.sampleIndex = self.maximumVoltageIndex + self.sampleNumber # Calculates the index value of the sample
      if self.sampleIndex > len(self.voltageArray): # Ensures that the sample index does not exceed the size of the array
         self.maximumAmplitudesArray.pop() # Removes the last value in the array
      else:
         self.sampleAmplitudesArray.append(float(self.voltageArray[self.sampleIndex]) - self.baselineVoltage) # Stores all the sample amplitudes for each event for plotting
      self.eventChecker = self.maximumVoltageIndex # Sets the starting point to be the max voltage
      self.eventIndexEnd = (len(self.voltageArray) - 1) # Sets the end point to be the end of the array
      self.usefulEvent = 0
      while self.eventChecker < self.eventIndexEnd:
         if self.voltageArray[self.eventChecker] <= self.baselineVoltage: # Checks if the event is useful
            self.usefulEvent = 1
            self.eventChecker = self.eventIndexEnd # Breaks the while loop
         self.eventChecker += 1 # Increments the index
      if self.usefulEvent == 0:
         self.maximumAmplitudesArray.pop()
         self.sampleAmplitudesArray.pop()
                      
   def display_data(self):
         
      matplotlib.pyplot.scatter(self.maximumAmplitudesArray, self.sampleAmplitudesArray) # Plots the maximum amplitudes on x-axis and sample amplitudes on y-axis
      matplotlib.pyplot.title('Pulse Gradient Analysis Plot (N = %d)' % self.sampleNumber)
      matplotlib.pyplot.xlabel('Peak Amplitudes')
      matplotlib.pyplot.ylabel('Sample Amplitudes')
      matplotlib.pyplot.show()
 
      print('\n\n')
      print('___Additional Information___')
      print('Number of events processed: %d' % self.eventCounter)
      print('Number of events plotted: %d' % len(self.maximumAmplitudesArray))
      print('Time taken to process data: %f' % (time.time() - self.startTime), "seconds")
      print('\n\n')

pulse_gradient_analysis = PulseGradientAnalysis()
pulse_gradient_analysis.process_data()
pulse_gradient_analysis.display_data()
