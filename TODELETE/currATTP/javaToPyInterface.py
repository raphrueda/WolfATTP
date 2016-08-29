#!/usr/bin/python

import adapters
import sys
import os





# What this does is takes the arguments given from the java gui and decides where to go
# 1 = Stratgey Name, 2 = N val , 3 = TH Val, 4 = startDate, 5 = endDate, 6 = TRTH val
allParams =[]
paramsStrat = []
paramsN = []
paramsTH = []
paramsStart = []
paramsEnd = []
paramsTRTH = []
interface = open('interfaceParams.txt', 'r')
for line in interface:
  allParams.append(line.rstrip('\n'));

 # Now all params are in allparams


for i in range(len(allParams)):
    if i % 6 == 0:
        paramsStrat.append(allParams[i])
    if i % 6 == 1:
        paramsN.append(allParams[i])
    if i % 6 == 2:
        paramsTH.append(allParams[i])
    if i % 6 == 3:
        paramsStart.append(allParams[i])
    if i % 6 == 4:
        paramsEnd.append(allParams[i])
    if i % 6 == 5:
        paramsTRTH.append(allParams[i])

# # now each file array is of the same length and hold the day for the correspoing on of the same index
# # def callStrategy:(strat, n, th, start, end, TRTH):
adapters.main(paramsStrat, paramsN, paramsTH, paramsStart, paramsEnd, paramsTRTH, False)
