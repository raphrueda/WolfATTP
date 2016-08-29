import csv
import sys
import re

#go through the order files in ordersArray.
#Format of the file is <strategy>-ordersSTD#-#-#.csv
# # is 1 or more numbers
class ScrapeOrders:
    def __init__(self):
        self.__orders = {}
        self.__profit = {}
        # self.__files = []
        self.__companies = []
        self.__strategies = []
        self.__modules = []

    def iterate_orders(self, ordersArray):
        orders_dict = {}
        profit_dict = {}
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
            if new_file_name not in orders_dict:
                orders_dict[new_file_name] = {}

            # ordersDict[new_file_name] = self.scrape_orders(orders_file)
            # self.__orders = ordersDict

            (orders_dict[new_file_name], profit_dict[new_file_name]) = self.scrape_orders(orders_file)

            #round the numbers
            #for date_key in orders_dict[orders_file]['profit_of_the_day']:
            #    orders_dict[orders_file]['profit_of_the_day'][date_key] = round(orders_dict[orders_file]['profit_of_the_day'][date_key], 2)
            self.__orders = orders_dict
            self.__profit = profit_dict
        return (orders_dict, profit_dict)
        # return ordersDict

    #read the order file and extract the information
    def scrape_orders(self, orders_file):
        orders = open(orders_file)
        next(orders)
        CSVorders = csv.reader(orders, delimiter=',', quotechar='|')
        profit_of_the_day = {'Dates': [], 'profit_loss': [], 'cumulative_profit_loss': []}
        saved_value = 0
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

            if (companies[row[0]]['lines_scanned'] % 2 == 0):
                #append if date does not exist
                if row[1] not in profit_of_the_day['Dates']:
                    profit_of_the_day['Dates'].append(row[1])

                    #find profit or loss and add to the end of the list
                    if row[5] == "Buy":
                        profit_of_the_day['profit_loss'].append(- float(row[4]) + saved_value)
                    else:
                        profit_of_the_day['profit_loss'].append(float(row[4]) - saved_value)
                else:
                    #find profit or loss and add to the existing index
                    if row[5] == "Buy":
                        profit_of_the_day['profit_loss'][profit_of_the_day['Dates'].index(row[1])] += (- float(row[4]) + saved_value)
                    else:
                        profit_of_the_day['profit_loss'][profit_of_the_day['Dates'].index(row[1])] += (float(row[4]) - saved_value)

            saved_value = float(row[4])
            #append the row to the orders data
            companies[row[0]]['orders_data']['Date'].append(row[1])
            companies[row[0]]['orders_data']['Price'].append(float(row[2]))
            companies[row[0]]['orders_data']['Volume'].append(float(row[3]))
            companies[row[0]]['orders_data']['Value'].append(float(row[4]))
            companies[row[0]]['orders_data']['Signal'].append(row[5])

        #revert the last value if the number of rows are odd

        # if (companies[row[0]]['lines_scanned'] % 2 == 1):
        #     if row[5] == "Buy":
        #         companies[row[0]]['tot_revenue'] += float(row[4])
        #     else:
        #         companies[row[0]]['tot_revenue'] -= float(row[4])

        #round to 2 decimal places
        for company in companies:
            companies[company]['tot_revenue'] = round(companies[company]['tot_revenue'], 2)

                #find cumulative profit
        for index in range(len(profit_of_the_day['profit_loss'])):
            profit_of_the_day['profit_loss'][index] = round(profit_of_the_day['profit_loss'][index], 2)
            if index > 0:
                profit_of_the_day['cumulative_profit_loss'].append(round(profit_of_the_day['cumulative_profit_loss'][index-1] + profit_of_the_day['profit_loss'][index], 2))
            else:
                profit_of_the_day['cumulative_profit_loss'].append(round(profit_of_the_day['profit_loss'][index], 2))

        #returns a tuple of the company and profit of the day
        return (companies, profit_of_the_day)

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

    @property
    def profit(self):
        return self.__profit
