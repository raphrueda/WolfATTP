import csv
import sys
from constant import *
import datetime

class DataManipulator:

    def __init__(self, masterArray, companies, strategyEmployed, dateRangeFrom, dateRangeTo):
        #1st dimension is company, 2nd dimension is date/row, 3rd dimension is the different data for the date.
        #1st index of 3rd dimension is Company, 2nd: Date, 3rd: Price, 4th: Volume, 5th: Value (Price * Volume), 6th: Buy/Sell
        self.masterArray = masterArray
        self.companies = companies
        self.strategyEmployed = strategyEmployed
        self.dateRangeFrom = dateRangeFrom
        self.dateRangeTo = dateRangeTo

    #converts the companyName to indices
    def getCompanyIndex(self, companyName="all"):
        companyIndex = []
        if (companyName == "all"):
            companyIndex = range(len(self.masterArray))
        else:
            try:
                companyIndex = [self.companies[companyName]]
            except KeyError:
                companyIndex = []
        return companyIndex

    def refineResult(self, array, companyName="all", specialFlag=0):

        if specialFlag != 0:
            refinedArray = array[FIRST_ROW]
            refinedArray.pop(0)
            if specialFlag == 2:
                refinedArray = refinedArray[0]
        elif companyName != "all" and len(array) > 0:
            refinedArray = array[FIRST_ROW]
        else:
            refinedArray = array
        return refinedArray

    #find price of profit
    #companyIndex is a list of numbers with the index that corresponds to the company in the masterArray
    def profitFromTransactionAsPrice(self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)
        #our result, 1st dimension is the company and 2nd dimension is the price
        profitPriceArray = []

        #a dictionary of the latest price for each company
        currentPrice = dict()

        #counter for inputting to the result array
        writeIndex = 0

        #goes through each company
        for company in companyIndex:
            #add first dimension to the result array for each company
            profitPriceArray.append([])

            isEvenDayOfTrading = 0
            #goes through each row
            for price in range(len(self.masterArray[company])):

                #checks if it is a buy
                if ((isEvenDayOfTrading % 2) == 0):
                    #update the dictionary to have the current price
                    currentPrice[self.masterArray[company][price][COMPANY_FIELD]] = self.masterArray[company][price][VALUE_FIELD]

                    #add not available to the result
                    profitPriceArray[writeIndex].append("=NA()")
                else:
                    #find profit of the current price ("Selling Price") and the stored value in currentBuy dict ("Buying Price")
                    if (self.masterArray[company][price][ORDER_FIELD] == "Sell" or self.masterArray[company][price][ORDER_FIELD] == "sell"):
                        profit = float(self.masterArray[company][price][VALUE_FIELD]) - float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])
                    else:
                        #find profit of the current price ("Buying Price") and the stored value in currentBuy dict ("Selling Price"), short-selling
                        profit = - float(self.masterArray[company][price][VALUE_FIELD]) + float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])

                    #add the profit to the result
                    profitPriceArray[writeIndex].append(round((profit),2))

                isEvenDayOfTrading += 1
            writeIndex += 1
        return self.refineResult(profitPriceArray, companyName)


    def profitFromTransactionAsPercentage(self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        #our result, 1st dimension is the company and 2nd dimension is the profit percentage
        profitPercentageArray = []

        #a dictionary of the latest price for each company
        currentPrice = dict()

        #counter for inputting to the result array
        writeIndex = 0

        #goes through each company
        for company in companyIndex:

            #add first dimension to the result array for each company
            profitPercentageArray.append([])
            firstPrice = self.masterArray[company][FIRST_ROW][VALUE_FIELD]
            isEvenDayOfTrading = 0
            #goes through each row
            for price in range(len(self.masterArray[company])):

                #checks if it is a buy
                if ((isEvenDayOfTrading % 2) == 0):
                    #update the dictionary to have the current price
                    currentPrice[self.masterArray[company][price][COMPANY_FIELD]] = self.masterArray[company][price][VALUE_FIELD]

                    #add not available to the result
                    profitPercentageArray[writeIndex].append("=NA()")
                else:
                    #find profit of the current price ("Selling Price") and the stored value in currentBuy dict ("Buying Price")
                    if (self.masterArray[company][price][ORDER_FIELD] == "Sell" or self.masterArray[company][price][ORDER_FIELD] == "sell"):
                        profit = float(self.masterArray[company][price][VALUE_FIELD]) - float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])
                    else:
                        #find profit of the current price ("Buying Price") and the stored value in currentBuy dict ("Selling Price"), short-selling
                        profit = - float(self.masterArray[company][price][VALUE_FIELD]) + float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])

                    #add the profit percentage to the result
                    profitPercentageArray[writeIndex].append(round(profit*100/float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]]),4))
                isEvenDayOfTrading += 1
            writeIndex += 1

        return self.refineResult(profitPercentageArray, companyName)

    def cumulativeProfit(self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        #our result, 1st dimension is the company and 2nd dimension is the profit percentage
        cumulativeProfitArray = []

        #a dictionary of the latest price for each company
        currentPrice = dict()

        #a dictionary of the current cumulativeProfit for each company
        cumulativeProfit = dict()

        #counter for inputting to the result array
        writeIndex = 0

        #goes through each company
        for company in companyIndex:

            #add first dimension to the result array for each company
            cumulativeProfitArray.append([])

            #initialise the profit of company to be 0
            cumulativeProfit[self.masterArray[company][FIRST_ROW][COMPANY_FIELD]] = 0

            isEvenDayOfTrading = 0
            #goes through each row
            for price in range(len(self.masterArray[company])):

                #checks if it is a buy
                if ((isEvenDayOfTrading % 2) == 0):
                    #update the dictionary to have the current price
                    currentPrice[self.masterArray[company][price][COMPANY_FIELD]] = self.masterArray[company][price][VALUE_FIELD]

                    #add not available to the result
                    cumulativeProfitArray[writeIndex].append("=NA()")
                else:
                    #find profit of the current price ("Selling Price") and the stored value in currentBuy dict ("Buying Price")
                    if (self.masterArray[company][price][ORDER_FIELD] == "Sell" or self.masterArray[company][price][ORDER_FIELD] == "sell"):
                        profit = float(self.masterArray[company][price][VALUE_FIELD]) - float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])
                    else:
                        #find profit of the current price ("Buying Price") and the stored value in currentBuy dict ("Selling Price"), short-selling
                        profit = - float(self.masterArray[company][price][VALUE_FIELD]) + float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])

                    #add the profit percentage to the result
                    cumulativeProfit[self.masterArray[company][price][COMPANY_FIELD]] += round(profit,2)
                    cumulativeProfitArray[writeIndex].append(round(cumulativeProfit[self.masterArray[company][price][COMPANY_FIELD]],2))
                isEvenDayOfTrading += 1
            writeIndex += 1

        return self.refineResult(cumulativeProfitArray, companyName)

    def cumulativePercentage(self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        #our result, 1st dimension is the company and 2nd dimension is the profit percentage
        cumulativePercentageArray = []

        #a dictionary of the latest price for each company
        currentPrice = dict()

        #a dictionary of the current cumulative profit for each company
        cumulativePercentage = dict()

        #counter for inputting to the result array
        writeIndex = 0

        #goes through each company
        for company in companyIndex:

            #add first dimension to the result array for each company
            cumulativePercentageArray.append([])

            #initialise the profit of company to be 0
            cumulativePercentage[self.masterArray[company][FIRST_ROW][COMPANY_FIELD]] = 0
            firstPrice = self.masterArray[company][FIRST_ROW][VALUE_FIELD]
            isEvenDayOfTrading = 0
            #goes through each row
            for price in range(len(self.masterArray[company])):

                #checks if it is a buy
                if ((isEvenDayOfTrading % 2) == 0):
                    #update the dictionary to have the current price
                    currentPrice[self.masterArray[company][price][COMPANY_FIELD]] = self.masterArray[company][price][VALUE_FIELD]

                    #add not available to the result
                    cumulativePercentageArray[writeIndex].append("=NA()")
                else:
                    #find profit of the current price ("Selling Price") and the stored value in currentBuy dict ("Buying Price")
                    if (self.masterArray[company][price][ORDER_FIELD] == "Sell" or self.masterArray[company][price][ORDER_FIELD] == "sell"):
                        profit = float(self.masterArray[company][price][VALUE_FIELD]) - float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])
                    else:
                        #find profit of the current price ("Buying Price") and the stored value in currentBuy dict ("Selling Price"), short-selling
                        profit = - float(self.masterArray[company][price][VALUE_FIELD]) + float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])

                    #add the profit percentage to the result
                    cumulativePercentage[self.masterArray[company][price][COMPANY_FIELD]] += profit*100/float(firstPrice)
                    cumulativePercentageArray[writeIndex].append(round(cumulativePercentage[self.masterArray[company][price][COMPANY_FIELD]],4))
                isEvenDayOfTrading += 1
            writeIndex += 1

        return self.refineResult(cumulativePercentageArray, companyName)

    def maxProfit(self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        #our result, 1st dimension is the company and 2nd dimension is the company name, maximum profit, date achieved
        maximumProfitArray = []

        #a dictionary of the latest price for each company
        currentPrice = dict()

        #keeps the maximum profit price and date when it occured for each company
        maxProfit = dict()

        #counter for inputting to the result array
        writeIndex = 0

        #goes through each company
        for company in companyIndex:
            #initialise the maximum profit of company to be 1st profit calculation, need at least 2 rows
            if (len(self.masterArray[company]) > 1):
                if (self.masterArray[company][FIRST_ROW][ORDER_FIELD] == "Sell" or self.masterArray[company][FIRST_ROW][ORDER_FIELD] == "sell"):
                    maxProfit[self.masterArray[company][FIRST_ROW][COMPANY_FIELD]] = round(- float(self.masterArray[company][SECOND_ROW][VALUE_FIELD]) + float(self.masterArray[company][FIRST_ROW][VALUE_FIELD]),2)
                else:
                    maxProfit[self.masterArray[company][FIRST_ROW][COMPANY_FIELD]] = round(float(self.masterArray[company][SECOND_ROW][VALUE_FIELD]) - float(self.masterArray[company][FIRST_ROW][VALUE_FIELD]),2)

                maxProfit[self.masterArray[company][FIRST_ROW][COMPANY_FIELD] + "-date"] = self.masterArray[company][SECOND_ROW][DATE_FIELD]
            else:
                maxProfit[self.masterArray[company][FIRST_ROW][COMPANY_FIELD]] = maxProfit[self.masterArray[company][FIRST_ROW][COMPANY_FIELD] + "-date"] = "=NA()"
                continue


            isEvenDayOfTrading = 0
            #goes through each row
            for price in range(len(self.masterArray[company])):
                #checks if it is a buy
                if ((isEvenDayOfTrading % 2) == 0):
                    #update the dictionary to have the current price
                    currentPrice[self.masterArray[company][price][COMPANY_FIELD]] = self.masterArray[company][price][VALUE_FIELD]

                else:
                    #find profit of the current price ("Selling Price") and the stored value in currentBuy dict ("Buying Price")
                    if (self.masterArray[company][price][ORDER_FIELD] == "Sell" or self.masterArray[company][price][ORDER_FIELD] == "sell"):
                        profit = float(self.masterArray[company][price][VALUE_FIELD]) - float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])
                    elif (self.masterArray[company][price][ORDER_FIELD] == "Buy" or self.masterArray[company][price][ORDER_FIELD] == "buy"):
                        #find profit of the current price ("Buying Price") and the stored value in currentBuy dict ("Selling Price"), short-selling
                        profit = - float(self.masterArray[company][price][VALUE_FIELD]) + float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])

                    if profit > maxProfit[self.masterArray[company][price][COMPANY_FIELD]]:
                        maxProfit[self.masterArray[company][price][COMPANY_FIELD]] = round(profit,2)
                        maxProfit[self.masterArray[company][price][COMPANY_FIELD] + "-date"] = self.masterArray[company][price][DATE_FIELD]

                isEvenDayOfTrading += 1

        for key in maxProfit:

            #avoid making a new list with just date
            if not key.endswith("-date"):
                maximumProfitArray.append([])
                maximumProfitArray[writeIndex].append(key)
                maximumProfitArray[writeIndex].append(maxProfit[key])

                #we want date to be in the same list as the price not a new one
                maximumProfitArray[writeIndex].append(self.convert_to_excel_date( maxProfit[key + "-date"]))
                writeIndex += 1

        return self.refineResult(maximumProfitArray, companyName, 1)

    def minProfit(self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        #our result, 1st dimension is the company and 2nd dimension is the company name, minimum profit, date achieved
        minimumProfitArray = []

        #a dictionary of the latest price for each company
        currentPrice = dict()

        #keeps the minimum profit price and date when it occured for each company
        minProfit = dict()

        #counter for inputting to the result array
        writeIndex = 0

        #goes through each company
        for company in companyIndex:
            #initialise the minimum profit of company to be 1st profit calculation, need at least 2 rows
            if (len(self.masterArray[company]) > 1):
                if (self.masterArray[company][FIRST_ROW][ORDER_FIELD] == "Sell" or self.masterArray[company][FIRST_ROW][ORDER_FIELD] == "sell"):
                    minProfit[self.masterArray[company][FIRST_ROW][COMPANY_FIELD]] = - float(self.masterArray[company][SECOND_ROW][VALUE_FIELD]) + float(self.masterArray[company][FIRST_ROW][VALUE_FIELD])
                else:
                    minProfit[self.masterArray[company][FIRST_ROW][COMPANY_FIELD]] = float(self.masterArray[company][SECOND_ROW][VALUE_FIELD]) - float(self.masterArray[company][FIRST_ROW][VALUE_FIELD])

                minProfit[self.masterArray[company][FIRST_ROW][COMPANY_FIELD] + "-date"] = self.masterArray[company][SECOND_ROW][DATE_FIELD]
            else:
                minProfit[self.masterArray[company][FIRST_ROW][COMPANY_FIELD]] = minProfit[self.masterArray[company][FIRST_ROW][COMPANY_FIELD] + "-date"] = "=NA()"
                continue


            isEvenDayOfTrading = 0
            #goes through each row
            for price in range(len(self.masterArray[company])):
                #checks if it is a buy
                if ((isEvenDayOfTrading % 2) == 0):
                    #update the dictionary to have the current price
                    currentPrice[self.masterArray[company][price][COMPANY_FIELD]] = self.masterArray[company][price][VALUE_FIELD]

                else:
                    #find profit of the current price ("Selling Price") and the stored value in currentBuy dict ("Buying Price")
                    if (self.masterArray[company][price][ORDER_FIELD] == "Sell" or self.masterArray[company][price][ORDER_FIELD] == "sell"):
                        profit = float(self.masterArray[company][price][VALUE_FIELD]) - float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])
                    elif (self.masterArray[company][price][ORDER_FIELD] == "Buy" or self.masterArray[company][price][ORDER_FIELD] == "buy"):
                        #find profit of the current price ("Buying Price") and the stored value in currentBuy dict ("Selling Price"), short-selling
                        profit = - float(self.masterArray[company][price][VALUE_FIELD]) + float(currentPrice[self.masterArray[company][price][COMPANY_FIELD]])

                    if profit < minProfit[self.masterArray[company][price][COMPANY_FIELD]]:

                        minProfit[self.masterArray[company][price][COMPANY_FIELD]] = round(profit,2)
                        minProfit[self.masterArray[company][price][COMPANY_FIELD] + "-date"] = self.masterArray[company][price][DATE_FIELD]

                isEvenDayOfTrading += 1

        for key in minProfit:

            #avoid making a new list with just date
            if not key.endswith("-date"):
                minimumProfitArray.append([])
                minimumProfitArray[writeIndex].append(key)
                minimumProfitArray[writeIndex].append(minProfit[key])

                #we want date to be in the same list as the price not a new one
                minimumProfitArray[writeIndex].append(self.convert_to_excel_date(minProfit[key + "-date"]))
                writeIndex += 1

        return self.refineResult(minimumProfitArray, companyName, 1)

    def cashFlow(self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        cashFlowArray = []
        writeIndex = 0
        for company in companyIndex:
            cashFlowArray.append([])
            for price in range(len(self.masterArray[company])):
                if (self.masterArray[company][price][ORDER_FIELD] == "Buy" or self.masterArray[company][price][ORDER_FIELD] == "buy"):
                    #negative because it's buy
                    cashFlowArray[writeIndex].append(float(self.masterArray[company][price][VALUE_FIELD]) * (-1))
                else:
                    #positive because it's sell
                    cashFlowArray[writeIndex].append(float(self.masterArray[company][price][VALUE_FIELD]))
            writeIndex += 1

        return self.refineResult(cashFlowArray, companyName)

    def getNumOfLine (self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        numOfLinesArray = []
        for company in companyIndex:
            numOfLinesArray.append(len(self.masterArray[company]))

        return self.refineResult(numOfLinesArray, companyName)

    def getCompanyList (self):
        listOfCompanies = []

        #go through dictionary and append the keys
        for company in self.companies:
            listOfCompanies.append(company)

        return listOfCompanies

    def getOverallRevenue (self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        overallRevenueArray = []
        cumulativeProfitArray = self.cumulativeProfit(companyName)
        numOfLinesArray = self.getNumOfLine(companyName)
        writeIndex = 0
        for company in companyIndex:
            overallRevenueArray.append([])

            #find the company name
            overallRevenueArray[writeIndex].append(self.masterArray[company][FIRST_ROW][COMPANY_FIELD])

            #finds last index of the cumulative profit for a company
            lastIndex = numOfLinesArray - 1

            #last value of cumulative profit is in the last odd index
            if lastIndex % 2 == 0 and lastIndex > 0:
                overallRevenueArray[writeIndex].append(cumulativeProfitArray[lastIndex-1])
            elif lastIndex > 0:
                overallRevenueArray[writeIndex].append(cumulativeProfitArray[lastIndex])
            else:
                overallRevenueArray[writeIndex].append("=NA()")
            writeIndex += 1

        return self.refineResult(overallRevenueArray, companyName, 2)

    def convert_to_excel_date(self, old_date):

        date_pieces = old_date.split('-')
        if len(date_pieces[2]) == 2: # So its truncated to the last two digits
            date_pieces[2] = '20' + date_pieces[2]
        month_to_int = {
            'JAN': 1,
            'FEB': 2,
            'MAR': 3,
            'APR': 4,
            'MAY': 5,
            'JUN': 6,
            'JUL': 7,
            'AUG': 8,
            'SEP': 9,
            'OCT': 10,
            'NOV': 11,
            'DEC': 12,
        }
        return datetime.date(int(date_pieces[2]), month_to_int[date_pieces[1]], int(date_pieces[0]))

    def getCompanyDates (self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        companyDatesArray = []
        writeIndex = 0

        for company in companyIndex:
            companyDatesArray.append([])
            for rowIndex in range(len(self.masterArray[company])):
                companyDatesArray[writeIndex].append(self.convert_to_excel_date(self.masterArray[company][rowIndex][DATE_FIELD]))
            writeIndex += 1

        return self.refineResult(companyDatesArray, companyName)

    def getCompanyPrices (self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        companyPricesArray = []
        writeIndex = 0

        for company in companyIndex:
            companyPricesArray.append([])
            for rowIndex in range(len(self.masterArray[company])):
                companyPricesArray[writeIndex].append(self.masterArray[company][rowIndex][PRICE_FIELD])
            writeIndex += 1

        return self.refineResult(companyPricesArray, companyName)

    def getCompanySignals (self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        companySignalsArray = []
        writeIndex = 0

        for company in companyIndex:
            companySignalsArray.append([])
            for rowIndex in range(len(self.masterArray[company])):
                companySignalsArray[writeIndex].append(self.masterArray[company][rowIndex][ORDER_FIELD])
            writeIndex += 1

        return self.refineResult(companySignalsArray, companyName)

    def getCompanyVolumes (self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        companyVolumesArray = []
        writeIndex = 0

        for company in companyIndex:
            companyVolumesArray.append([])
            for rowIndex in range(len(self.masterArray[company])):
                companyVolumesArray[writeIndex].append(self.masterArray[company][rowIndex][VOLUME_FIELD])
            writeIndex += 1

        return self.refineResult(companyVolumesArray, companyName)

    def getStrategyEmployed (self):

        return self.strategyEmployed

    def getDateRangeFrom(self):

        return self.dateRangeFrom

    def getDateRangeTo(self):

        return self.dateRangeTo

    def getOverallPercentage (self, companyName):

        #gets the index of the company/ies
        companyIndex = self.getCompanyIndex(companyName)

        overallPercentageArray = []
        cumulativePercentageArray = self.cumulativePercentage(companyName)
        numOfLinesArray = self.getNumOfLine(companyName)
        writeIndex = 0
        for company in companyIndex:
            overallPercentageArray.append([])

            #find the company name
            overallPercentageArray[writeIndex].append(self.masterArray[company][FIRST_ROW][COMPANY_FIELD])

            #finds last index of the cumulative profit for a company
            lastIndex = numOfLinesArray - 1

            #last value of cumulative profit is in the last odd index
            if lastIndex % 2 == 0 and lastIndex > 0:
                overallPercentageArray[writeIndex].append(cumulativePercentageArray[lastIndex-1])
            elif lastIndex > 0:
                overallPercentageArray[writeIndex].append(cumulativePercentageArray[lastIndex])
            else:
                overallPercentageArray[writeIndex].append("=NA()")
            writeIndex += 1

        return self.refineResult(overallPercentageArray, companyName, 2)

    def getAnalytics(self, analytics, companyName="all"):

        result = []

        if (analytics == "profitPrice"):
            result = self.profitFromTransactionAsPrice(companyName)
        if (analytics == "profitPercentage"):
            result = self.profitFromTransactionAsPercentage(companyName)
        if (analytics == "cumulativeProfit"):
            result = self.cumulativeProfit(companyName)
        if (analytics == "cumulativePercentage"):
            result = self.cumulativePercentage(companyName)
        if (analytics == "maxProfit"):
            result = self.maxProfit(companyName)
        if (analytics == "minProfit"):
            result = self.minProfit(companyName)
        if (analytics == "cashFlow"):
            result = self.cashFlow(companyName)
        if (analytics == "numOfLines"):
            result = self.getNumOfLine(companyName)
        if (analytics == "companyList"):
            result = self.getCompanyList()
        if (analytics == "overallRevenue"):
            result = self.getOverallRevenue(companyName)
        if (analytics == "companyDates"):
            result = self.getCompanyDates(companyName)
        if (analytics == "companyPrices"):
            result = self.getCompanyPrices(companyName)
        if (analytics == "companySignals"):
            result = self.getCompanySignals(companyName)
        if (analytics == "companyVolumes"):
            result = self.getCompanyVolumes(companyName)
        if (analytics == "strategyEmployed"):
            result = self.getStrategyEmployed()
        if (analytics == "dateRangeFrom"):
            result = self.getDateRangeFrom()
        if (analytics == "dateRangeTo"):
            result = self.getDateRangeTo()
        if (analytics == "companyIndex"): #This is not used by JJ do we need it? ****
            result = self.getCompanyIndex(companyName)

        #if companyName is specified, return a 1D array from the 2D arrays, companyList returns 1D array
        # if companyName != "all" and len(result) > 0 and analytics != "companyList":
        #     #only 1 company so just show 1D array from [[list of data]]
        #     return result[FIRST_ROW]
        # else:
        return result
