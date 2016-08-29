#!/usr/bin/python
import sys
import csv
import time
import os
from data_manipulator import DataManipulator
from scrape_orders import ScrapeOrders
import sys
from strategy_performance_report import strategy_performance_report_builder
ordersFiles = []


def main(paramsStrat, paramsN, paramsTH, paramsStart, paramsEnd, paramsTRTH, makeEXCEL):
    ## THIS IS THE ENTRY POINT OF THIS PROGRAM, DO NOT CALL FUNCTION DIRECTLY OR ILL KILL YOU
    if makeEXCEL == False:
        callStrategy(paramsStrat, paramsN, paramsTH, paramsStart, paramsEnd, paramsTRTH)
    run_option = ['normal']
    # companies = ['BHP.AX','ANZ.AX','CBA.AX']
    # strategies = ['WolfOfSeng', 'BuyHard']
    # # strategies = ['N=3,TH=0.001', 'N=4,TH=0.02']
    date_range_from = 2000
    date_range_to = 2005
    SO = ScrapeOrders()
    SO.iterate_orders(ordersFiles)
    print SO.companies
    print SO.strategies
    # DM = DataManipulator(master_array, run_option, companies, strategies, date_range_from, date_range_to)
    DM = DataManipulator(SO.orders,
                        SO.modules,
                        run_option,
                        SO.companies,
                        SO.strategies,
                        date_range_from,
                        date_range_to)
    strategy_performance_report_builder(DM)




def callStrategy(strat, n, th, start, end, TRTH):
    # n and the will be arrays of equal size constructed by the java to py intface
    for i in range(len(n)):
        if strat[i] == "WolfofSENG":
            callWolfOfSeng(n[i], th[i], start[i], end[i], TRTH[i])
        elif strat[i] == "BuyHard":
            callBuyHard(n[i], th[i], start[i], end[i], TRTH[i])
        elif strat[i] == "aurora":
            callAurora(n[i], th[i], start[i], end[i], TRTH[i])
        elif strat[i] == "trock":
            callTrock(n[i], th[i], start[i], end[i], TRTH[i])
        # At this point in time there is an orders file that is made in the curr
        # directory. We need to rename it and append its name to a list. File is
        # called "ordersSTD.csv"
        #print strat[i] + n[i] + th[i] + start + end + TRTH
        os.rename("ordersSTD.csv", strat[i] + "-" + "ordersSTD" + str(i) + "-" + n[i] + "-" + th[i] + ".csv")
        ordersFiles.append(strat[i] + "-" + "ordersSTD" + str(i) + "-" + n[i] + "-" + th[i] + ".csv")
        print strat[i] + "-" + "ordersSTD" + str(i) + "-" + n[i] + "-" + th[i] + ".csv"



def callWolfOfSeng(n, th, start, end, TRTH):
    if n != "" and th != "" :
        makeWolfOfSengParams(n, th, start, end)
    else:
        makeWolfOfSengParams("4", "0.001", start, end)
    parameterFile = "wolfOfSeng/sampleParams.txt"
    TRTH = TRTH
    os.system("python wolfOfSeng/momentumStrategy.py " + TRTH + " "+parameterFile)


    ##----------------------------STANDERDISTATION--------------#######


    monthToNum = {"JAN":'01',
    "FEB":'02',
    "MAR":'03',
    "APR":'04',
    "MAY":'05',
    "JUN":'06',
    "JUL":'07',
    "AUG":'08',
    "SEP":'09',
    "OCT":'10',
    "NOV":'11',
    "DEC":'12'}



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
            goodDate = [splitDate[2],monthToNum[splitDate[1]],splitDate[0]]
            joiner = "/"
            row[1] =joiner.join(goodDate)
            writer.writerow(row)
    goodOrders.close()
    badOrders.close()


def callAurora(n, th, start, end, TRTH):
    # aurora are annyoing and break if you give a start date out of range



    makeAuroraParams(n, th, start, end, TRTH)
    parameterFile = "aurora/parameters.txt"
    TRTH = TRTH
    os.system("java -jar aurora/aurora.jar "+TRTH +" "+parameterFile+ "")
    #os.rename("orders.csv", "ordersSTD.csv")



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
            goodDate = [splitDate[2],splitDate[1],splitDate[0]]
            joiner = "/"
            row[1] =joiner.join(goodDate)
            if row[5] == "B":
                row[5] = "Buy"

            if row[5] == "S":
                row[5] = "Sell"
            writer.writerow(row)
    goodOrders.close()
    badOrders.close()



def makeAuroraParams(n, th, start, end, TRTH):

    preOpen = open(TRTH)
    counter = 0
    for line in preOpen:

        if counter == 1:
            # Read first line and make sure date is good
            [x.strip() for x in line.split(',')]
            print x
        counter = counter + 1


    params = open("aurora/parameters.txt", 'w')
    if start != "":
        params.write("start_date = 31-Jan-" + start + "\n")
        params.write("end_date = 01-Jan-" + end + "\n")
    params.write("moving_average_window = " + n + "\n")
    params.write("threshold = " + th + "\n")
    params.write("output_dir = orders.csv" + "\n")
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
    if n != "" and th != "" :
        makeBuyHardParams(n, th, start, end)
        ## else use default
    parameterFile = "buyHard/parameters.txt"
    TRTH = TRTH
    os.system("java -jar buyHard/BuyHard-Momentum-1.0.0.jar "+TRTH +" "+parameterFile+ "")
    #os.system("mv orders.csv ordersSTD.csv")
    # Log file in curr directory, uncoment line above to move to buyHard Directory

    # Now we have to open the log file and standerdise the output to ours


    ##----------------------------STANDERDISTATION--------------#######


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
            goodDate = [splitDate[2],splitDate[1],splitDate[0]]
            joiner = "/"
            row[1] =joiner.join(goodDate)
            if row[5] == "B":
                row[5] = "Buy"

            if row[5] == "S":
                row[5] = "Sell"
            writer.writerow(row)
    goodOrders.close()
    badOrders.close()
def callTrock(n, th, start, end, TRTH):
    makeTrockParams(n, th, start, end, TRTH)
    os.system("./trock/trockAT params.params")


def makeTrockParams(n, th, start, end, TRTH):
    params = open("trock/params.params", 'w')
    params.write(":input_csvFile:" + TRTH + '\\' + "\n")
    params.write(":output_csvFile:ordersSTD.csv" + '\\' + "\n")
    params.write(":returnsInCalculation:" + n + '\\' + "\n")
    params.write(":threshold:" + th + '\\' + "\n")
    params.write(":startDate:01-JAN-" + start + '\\' + "\n")
    params.write(":endDate:31-DEC-" + end + '\\' + "\n")
