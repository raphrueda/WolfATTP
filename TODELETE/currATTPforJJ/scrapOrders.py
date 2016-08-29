import csv
import sys


def scrapOrders():
    companies = dict()
    orders = open("ordersSTD.csv")
    next(orders)
    masterArray = []
    CSVorders = csv.reader(orders, delimiter=',', quotechar='|')
    index = 0
    j = 0
    for row in CSVorders:
        if (row[0] == "Company Name"):
            continue
        try:
            index = companies[row[0]]
        except:
            companies[row[0]] = len(companies)
            index = companies[row[0]]
            masterArray.append([]) #new list for each company

        masterArray[index].append([]) #new list for each date/row
        j = len(masterArray[index]) -1
        for i in range (len(row)):
            masterArray[index][j].append(row[i])
    return (masterArray, companies)


