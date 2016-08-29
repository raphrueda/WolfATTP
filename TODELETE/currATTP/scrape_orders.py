import csv
import sys
import re

#go through the order files in ordersArray.
#Format of the file is <strategy>-ordersSTD#-#-#.csv
# # is 1 or more numbers
class ScrapeOrders:
    def __init__(self):
        self.__orders = {}
        # self.__files = []
        self.__companies = []
        self.__strategies = []
        self.__modules = []

    def iterate_orders(self, ordersArray):
        ordersDict = {}
        for orders_file in ordersArray:
            split_file_name = orders_file.replace('.csv','').split('-')
            new_file_name = split_file_name[0] + ':' + 'N=' + split_file_name[2] + ',' + 'TH=' + split_file_name[3]
            if split_file_name[0] not in self.__modules:
                self.__modules.append(split_file_name[0])
            self.__strategies.append(new_file_name)
            fileNameParam = re.split('\-', orders_file, maxsplit=1)

            #take the first part for strategy and last part for file_name
            # file_name = fileNameParam[1]
            # strategy = fileNameParam[0]

            #make a new dict for the file_name if not already in the ordersDict
            if new_file_name not in ordersDict:
                ordersDict[new_file_name] = {}

            ordersDict[new_file_name] = self.scrape_orders(orders_file)
            self.__orders = ordersDict
        return ordersDict

    #read the order file and extract the information
    def scrape_orders(self, orders_file):
        orders = open(orders_file)
        next(orders)
        CSVorders = csv.reader(orders, delimiter=',', quotechar='|')

        companies = {}
        #go through each row of the order file
        for row in CSVorders:
            #make a new dict for the company if not already in the companies
            if row[0] not in companies:
                if row[0] not in self.__companies:
                    self.__companies.append(row[0])
                companies[row[0]] = {'lines_scanned': 0, 'tot_revenue': 0, 'orders_data': {'Date': [],
                                                                                            'Price': [],
                                                                                            'Volume': [],
                                                                                            'Value': [],
                                                                                            'Signal': []}}

            #add 1 for the lines scanned
            companies[row[0]]['lines_scanned'] += 1

            #add or subtract the total revenue
            if row[5] == "Buy":
                companies[row[0]]['tot_revenue'] -= float(row[4])
            else:
                companies[row[0]]['tot_revenue'] += float(row[4])

            #append the row to the orders data
            companies[row[0]]['orders_data']['Date'].append(row[1])
            companies[row[0]]['orders_data']['Price'].append(float(row[2]))
            companies[row[0]]['orders_data']['Volume'].append(float(row[3]))
            companies[row[0]]['orders_data']['Value'].append(float(row[4]))
            companies[row[0]]['orders_data']['Signal'].append(row[5])

        #round to 2 decimal places
        for company in companies:
            companies[company]['tot_revenue'] = round(companies[company]['tot_revenue'], 2)

        return companies

    @property
    def companies(self):
        return self.__companies

    @property
    def strategies(self):
        return self.__strategies

    @property
    def orders(self):
        return self.__orders

    @property
    def modules(self):
        return self.__modules
    # def get_files(self):
    #     fileList = []
    #     for fileKey in self.orders:
    #         fileList.append(fileKey)
    #     return set(fileList)
    #
    # def get_strategies(self):
    #     strategyList = []
    #     for fileKey in self.orders:
    #         for strategyKey in self.orders[fileKey]:
    #             strategyList.append(strategyKey)
    #     return set(strategyList)
    #
    # def get_companies(self):
    #     companyList = []
    #     for fileKey in self.orders:
    #         for strategyKey in self.orders[fileKey]:
    #             for companyKey in self.orders[fileKey][strategyKey]:
    #                 companyList.append(companyKey)
    #     return set(companyList)
