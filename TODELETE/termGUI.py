#!/usr/bin/python
import adapters
import sys
import os




strategy = raw_input("Please choose a strategy (by Number): \n1. Wolf of Seng \n2. BuyHard \n")

nVal = raw_input("Please enter a N value (if blank, defaults to 4) \n")
if nVal == "":
    nVal = "4"

thVal = raw_input("Plese enter a TH value (if bank, defaults to 0.001) \n")
if thVal == "":
    thVal = "0.001"

startDate = ""
endDate = ""
startDate = raw_input("Please enter a start date for analysis (if blanks, looks at \nthe whole TRTH file ) \n")
if startDate != "":
    endDate = raw_input("Plese enter a end date for the analysis (if blank, only \nlooks at start date year ) \n")

if strategy == '1':
    adapters.callWolfOfSeng(nVal, thVal, startDate, endDate, sys.argv[1])
else:
    adapters.callBuyHard(nVal, thVal, startDate, endDate, sys.argv[1])
os.system("clear")

temp = raw_input("Made orders file, press enter to exit\n")
