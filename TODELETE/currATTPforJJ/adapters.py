#!/usr/bin/python
import sys
import csv
import time
import os
from dataManipulator import DataManipulator
from scrapOrders import scrapOrders
import sys
from performance_strategy_report_builder import performance_strategy_report_builder
ordersFiles = []

def callStrategy(strat, n, th, start, end, TRTH):
    # n and the will be arrays of equal size constructed by the java to py intface
    for i in range(len(n)):
        if strat[i] == "WolfOfSeng":
            callWolfOfSeng(n[i], th[i], start[i], end[i], TRTH[i])
        if strat[i] == "BuyHard":
            callBuyHard(n[i], th[i], start[i], end[i], TRTH[i])
        if strat[i] == "aurora":
            callAurora(n[i], th[i], start, end, TRTH)
        # At this point in time there is an orders file that is made in the curr
        # directory. We need to rename it and append its name to a list. File is
        # called "ordersSTD.csv"
        #print strat[i] + n[i] + th[i] + start + end + TRTH
        os.rename("ordersSTD.csv", strat[i] + "-" + "ordersSTD" + str(i) + "-" + n[i] + "-" + th[i] + ".csv")
        ordersFiles.append(strat[i] + "-" + "ordersSTD" + str(i) + "-" + n[i] + "-" + th[i] + ".csv")



def callWolfOfSeng(n, th, start, end, TRTH):
    print "made it here"
    print n + " "+ th + start + end + TRTH
    if n != "" and th != "" :
        makeWolfOfSengParams(n, th, start, end)
    else:
        makeWolfOfSengParams("4", "0.001", start, end)
    parameterFile = "wolfOfSeng/sampleParams.txt"
    TRTH = TRTH
    os.system("./wolfOfSeng/momentumStrategy " + TRTH + " "+parameterFile)
    os.system("mv orders.csv ordersSTD.csv")

def callAurora(n, th, start, end, TRTH):
    # aurora are annyoing and break if you give a start date out of range
    preOpen = open(TRTH)
    firstLine = preOpen.readline()
    firstLine = preOpen.readline()
    print firstLine

    makeAuroraParams(n, th, start, end)
    parameterFile = "aurora/parameters.txt"
    TRTH = TRTH
    os.system("java -jar aurora/aurora.jar "+TRTH +" "+parameterFile+ "")

    numToMonth = {'01':"JAN",
    '02':"FEB",
    '03':"MAR",
    '04':"APR",
    '05':"MAY",
    '06':"JUN",
    '07':"JUL",
    '08':"AUG",
    '09':"SEP",
    '10':"OCT",
    '11':"NOV",
    '12':"DEC"}


    # badOrders = open("orders.csv")
    badOrders = open("orders.csv")
    # uncoment if the file is in the buyHard dir and Comment line prev line
    next(badOrders)
    # Skips over titles

    # Print headers for new file
    goodOrders = open('ordersSTD.csv','w')
    writer = csv.writer(goodOrders, delimiter=',',lineterminator='\n',)
    writer.writerow(["Company Name","Date/Time","Price","Volume","Value","Bid/ask"])

    with badOrders as inputData:
        thisreader = csv.reader(inputData, delimiter=',', quotechar='|')
        for row in thisreader:
            splitDate = row[1].split("-", 2)
            newDate = [splitDate[1], numToMonth[splitDate[2]], splitDate[0]]
            joiner = "-"
            row[1] =joiner.join(newDate)
            if row[5] == "B":
                row[5] = "Buy"

            if row[5] == "S":
                row[5] = "Sell"
            writer.writerow(row)
    goodOrders.close()
    badOrders.close()




def makeAuroraParams(n, th, start, end):
    params = open("aurora/parameters.txt", 'w')
    if start != "":
        params.write("start_date = 31-Jan-" + start + "\n")
        params.write("end_date = 01-Jan-" + end + "\n")
    params.write("moving_average_window = " + n + "\n")
    params.write("threshold = " + th + "\n")
    params.write("output_dir = output.csv" + "\n")
    params.close()

def wolfOfSengCleanUp():
    os.remove("log.txt")
    os.remove("ordersSTD.csv")

def buyHardCleanUp():
    os.remove("logfile.log")
    os.remove("ordersSTD.csv")


def makeBuyHardParams(n, th, start, end):
    params = open("buyHard/parameters.txt", 'w')
    params.write("movingAvgTimeWindow=" + n + "\n")
    params.write("threshold=" + th + "\n")
    if start != "":
        params.write("startDate=01-01-" + start + "\n")
        params.write("endDate=01-01-" + end + "\n")


def makeWolfOfSengParams(n, th, start, end):
    params = open("wolfOfSeng/sampleParams.txt", 'w')
    params.write("N,TH,DateRange\n")
    if start!="NA" and end!="NA":
        params.write(n + "," + th + "," + start + "-" + end + "," + "\n")
    if start != "NA" and end == "NA":
        params.write(n + "," + th + "," + start + "\n")
    else:
        params.write(n + "," + th + "\n")




def callBuyHard(n, th, start, end, TRTH):
    #     # This functions calls the buyHard MSM
    numToMonth = {'01':"JAN",
    '02':"FEB",
    '03':"MAR",
    '04':"APR",
    '05':"MAY",
    '06':"JUN",
    '07':"JUL",
    '08':"AUG",
    '09':"SEP",
    '10':"OCT",
    '11':"NOV",
    '12':"DEC"}
    if n != "" and th != "" :
        makeBuyHardParams(n, th, start, end)
        ## else use default
    parameterFile = "buyHard/parameters.txt"
    TRTH = TRTH
    os.system("java -jar buyHard/BuyHard-Momentum-1.0.0.jar "+TRTH +" "+parameterFile+ "")
    #os.system("mv orders.csv ordersSTD.csv")
    # Log file in curr directory, uncoment line above to move to buyHard Directory

    # Now we have to open the log file and standerdise the output to ours

    # badOrders = open("orders.csv")
    badOrders = open("orders.csv")
    # uncoment if the file is in the buyHard dir and Comment line prev line
    next(badOrders)
    # Skips over titles

    # Print headers for new file
    goodOrders = open('ordersSTD.csv','w')
    writer = csv.writer(goodOrders, delimiter=',',lineterminator='\n',)
    writer.writerow(["Company Name","Date/Time","Price","Volume","Value","Bid/ask"])

    with badOrders as inputData:
        thisreader = csv.reader(inputData, delimiter=',', quotechar='|')
        for row in thisreader:
            splitDate = row[1].split("-", 2)
            splitDate[1] = numToMonth[splitDate[1]]
            joiner = "-"
            row[1] =joiner.join(splitDate)
            if row[5] == "B":
                row[5] = "Buy"

            if row[5] == "S":
                row[5] = "Sell"
            writer.writerow(row)
    goodOrders.close()
    badOrders.close()
