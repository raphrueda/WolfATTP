#!/usr/bin/python
#1/4 1 pm
import sys
import csv
import unittest
import time

globalErrorList = []

def preTesting():
    if (len(sys.argv) < 3):
        globalErrorList.append("Please Specify a TRTH and a Parameter file")
        print "Please Specify a TRTH and a Parameter file"

def decomposeCSV():
    # Unpacking of the param file
    params = open(sys.argv[2])
    next(params)
    paramN = ''
    paramTH = ''
    paramDateRange = ''
    currentCompany = ''
    numOfCompanys = 0
    masterArray = []
    CSVparams = csv.reader(params, delimiter=',', quotechar='|')
    for row in CSVparams:
        # 0 - N
        # 1 - TH
        paramN = int(row[0])
        paramTH = float(row[1])
        # Create array to hold date variable
        arrDateRange = []
        if (len(row) == 3):
            # If statments detects of there is a third param
            paramDateRange = str(row[2])
            arrDateRange = paramDateRange.split("-", 2);




    # Make Array that will hold the end of day values
    dataArray = []
    # Open file and skip the first line as it is the heading and not actully
    # data
    file = open(sys.argv[1])

    next(file)

    # Register as CSV
    with file as inputData:
        thisreader = csv.reader(inputData, delimiter=',', quotechar='|')
        for row in thisreader:
    # Right now, row is an array of each line in the csv
    # Index as follows
    # 0 - Share name
    # 1 - Date
    # 2 - Time
    # 3 - Type
    # 4 - Qualifiers
    # 5 - Open
    # 6 - High
    # 7 - Low
    # 8 - Last
    # 9 - Volume
    # 10 - Open Intel
    # 11 - Settle
    # Add the last value for each entry to the array
            if (currentCompany == ''):
                currentCompany = row[0]
                numOfCompanys = numOfCompanys +1
            if (currentCompany != row[0]):
                masterArray.append(dataArray)
                dataArray = []
                currentCompany = row[0]
                numOfCompanys = numOfCompanys +1
            # Date detection
            shareDate = row[1].split("-", 3)


            if (len(arrDateRange)  == 1):
                #Means it not a range, but just a value
                if (shareDate[2] != arrDateRange[0] ):

                    continue
            if (len(arrDateRange)  == 2):
                # Means its an Actully range of dates
                if(arrDateRange[0] > arrDateRange[1]):
                    # Invalide date range eg 2025-2015
                    globalErrorList.append("Invalid date ranage, function aborted")
                    return 0,0,0,[]

                if ((shareDate[2] > arrDateRange[1]) or (shareDate[2] < arrDateRange[0])):
                    # Date out of range, skip

                    continue

            if row[8] == '':
     			# dataArray.append('NA')
                 continue
            temp = []
            temp.append(row[8])
            temp.append(row[0])
            temp.append(row[1])
            temp.append('1000')
            dataArray.append(temp)
    # Now endOfDay has the end of day prices
    # Return from functiuon
    masterArray.append(dataArray)
    if (masterArray == [[]]):
        #This means that the date range did not match anthything in the CSV
        globalErrorList.append("No date for given date Range")
    return  paramN, paramTH, numOfCompanys, masterArray

def generateReturns(dataArray, numOfCompanys):

    for company in range(numOfCompanys):
        for i in range(len(dataArray[company])):
            if i > 0:
                if dataArray[company][i] != 'NA':
                    subcounter = 1
                    while dataArray[company][i - subcounter] == 'NA':
                        # Keep going back to find a valid value
                        subcounter = subcounter + 1
                    # now dataArray[counter - subcoutner] is a valid value
                    if i - subcounter < 0:
                        # this is for the rare case there is a no trading day in the
                        # first entry of the CSV and the sub counter takes us out of
                        # range of the endOfDay value. We then just lodge a 'NA' r
                        # result
                        dataArray[company].append('NA')
                        continue
                    dataArray[company][i].append((
                    float(dataArray[company][i][0]) -
                    float(dataArray[company][i - subcounter][0]))/
                    float(dataArray[company][i - subcounter][0]))
                else:
                    dataArray[company][i].append('NA')
            else:
                dataArray[company][i].append('')
    return dataArray

def SMA(n, dataArray, numOfCompanys):

    for company in range(numOfCompanys):
        length = len(dataArray[company])
        for i in range(n):
            # smAvg.append(0)
            dataArray[company][i].append(0)


        for i in range(n, length):
            windowSum = 0
            for j in range(n):
                if dataArray[company][i-j][4] == '':
                    continue
                else:
                    windowSum += float((dataArray[company][i-j][4]))
            # smAvg.append(sum/n)
            dataArray[company][i].append(windowSum/n)
    return dataArray

def gen_trade_signal_values(dataArray, thresh, numOfCompanys):
    for company in range(numOfCompanys):
        for i in range (len(dataArray[company])):
            if(i == 0):
                prev = dataArray[company][i][5]
                dataArray[company][i].append('');
            else:
                sig = (dataArray[company][i][5]) - prev
                prev = dataArray[company][i][5]
                dataArray[company][i].append(sig);
    return dataArray

def gen_trading_signals(dataArray, thresh, numOfCompanys):
    for company in range(numOfCompanys):
        buyCount = 1
        sellCount = 1

        for m in range(len(dataArray[company])):
            i = dataArray[company][m][6]
            if i == '':
                dataArray[company][m].append("Undefined")
                dataArray[company][m].append("noCount")
            elif (i < (-1*thresh)):
                dataArray[company][m].append("Sell")
                dataArray[company][m].append(sellCount)
                sellCount = sellCount + 1
            elif (i > thresh):
                dataArray[company][m].append("Buy")
                dataArray[company][m].append(buyCount)
                buyCount = buyCount + 1
            else:
                dataArray[company][m].append("Undefined")
                dataArray[company][m].append("noCount")
    return dataArray

def gen_orders(dataArray, numOfCompanys):
    for company in range(numOfCompanys):
        count = 0
        orders = []

        for index in range(len(dataArray[company])):
            if(index == 0 and dataArray[company][index][7] != "Undefined"):
                #case: buy...
                orders.append(dataArray[company][index][7])
                dataArray[company][index].append(dataArray[company][index][7])
                prev = dataArray[company][index][7]
                continue
            elif(len(orders) == 0 and dataArray[company][index][7] != "Undefined"):
                #case: ud,ud,ud,buy...
                orders.append(dataArray[company][index][7])
                dataArray[company][index].append(dataArray[company][index][7])
                prev = dataArray[company][index][7]
            elif(len(orders)>0 and dataArray[company][index][7] != "Undefined"):
                if(prev != dataArray[company][index][7]):
                    orders.append(dataArray[company][index][7])
                    dataArray[company][index].append(dataArray[company][index][7])
                    prev = dataArray[company][index][7]
                else:
                    dataArray[company][index].append('doNothing')
                    continue
            else:
                dataArray[company][index].append('doNothing')
                continue
    return dataArray

def makeOrderFile(dataArray , numOfCompanys):

    with open('orders.csv','w') as f1:
        writer = csv.writer(f1, delimiter=',',lineterminator='\n',)
        #header = 'CompanyName,Date/Time,Price,Volume,Value,Bid/Ask'
        #writer.writerow(header)
        writer.writerow(["Company Name","Date/Time","Price","Volume","Value","Bid/ask"])
        for company in range(numOfCompanys):
            for i in range(len(dataArray[company])):
                if (dataArray[company][i][9] == 'doNothing'):
                    continue
                else:
                    tempRow = []
                    tempRow.append(dataArray[company][i][1]) #Company Name
                    tempRow.append(dataArray[company][i][2]) #Date Time
                    tempRow.append(dataArray[company][i][0]) #Price
                    tempRow.append(100) #Volume fixed at 100 as specified in spec
                    value = float(dataArray[company][i][0]) * 100
                    tempRow.append(round(value, 2))           #Value
                    tempRow.append(dataArray[company][i][9]) #Bid/Ask
                    writer.writerow(tempRow)

def makeLogFile(startTime, endTime, executionTime, dataArray, paramN, paramTH):
    linesLoaded = 0
    log = open('log.txt', 'w')
    log.write('Team Name: The Wolf Of Seng \n')
    log.write('Version 1.03 \n')
    if (globalErrorList == []):
        log.write('Output Files: orders.csv, log.txt \n')
    else:
            log.write('Output Files: log.txt \n')
    log.write('Input File Name: ')
    log.write(sys.argv[1])
    log.write('\n')
    for i in range(len(globalErrorList)):
        if (i == 0):
            log.write('START ERROR LOG \n')
        log.write(globalErrorList[i])
        log.write('\n')
        if (i == len(globalErrorList) -1):
            log.write('END ERROR LOG \n\n')

    for i in range(len(dataArray)):
        linesLoaded = linesLoaded + len(dataArray[i])
    log.write('Lines successfully loaded from CSV (values in Last column): ')
    log.write(str(linesLoaded))
    log.write('\n')
    log.write('N Value ')
    log.write(str(paramN))
    log.write(' \n')
    log.write('TH Value ')
    log.write(str(paramTH))
    log.write(' \n')
    log.write('Start Time ')
    log.write(str(startTime))
    log.write(' \n')
    log.write('End Time ')
    log.write(str(endTime))
    log.write(' \n')
    log.write('Execution Time ')
    log.write(str(executionTime))
    log.write(' \n')

def main():
    # All these if statments do is abort the program nicely is we have an error
    startTime = time.time()
    dataArray = []
    preTesting()
    if (globalErrorList == []):
        paramN, paramTH, numOfCompanys, dataArray = decomposeCSV()
    if (globalErrorList == []):
        dataArray = generateReturns(dataArray, numOfCompanys)
    if (globalErrorList == []):
        dataArray = SMA(paramN, dataArray, numOfCompanys)
    if (globalErrorList == []):
        dataArray = gen_trade_signal_values(dataArray,paramTH, numOfCompanys)
    if (globalErrorList == []):
        dataArray = gen_trading_signals(dataArray,paramTH, numOfCompanys)
    if (globalErrorList == []):
        dataArray = gen_orders(dataArray, numOfCompanys)
    endTime = time.time()
    executionTime = (endTime - startTime)
    makeLogFile(startTime, endTime, executionTime, dataArray, paramN, paramTH)
    if (globalErrorList == []):
        makeOrderFile(dataArray, numOfCompanys)


if __name__ == "__main__":
    main()
