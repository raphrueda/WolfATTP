from strategy_performance_report import strategy_performance_report_builder
from data_manipulator import DataManipulator
from scrape_orders import ScrapeOrders

# master_array = {
#     'WolfOfSeng': { 'BHP.AX': { 'lines_scanned': 100,
#                                 'tot_revenue': 9000,
#                                 'orders_data': {
#                                     'Date': ['2000/01/02','2000/01/03','2000/01/04','2000/01/05','2000/01/06','2000/01/07'],
#                                     'Price': [1,2,3,4,5,6],
#                                     'Volume': [100,100,100,100,100,100],
#                                     'Value': [100,200,300,400,500,100],
#                                     'Signal': ['Buy','Sell','Buy','Sell','Buy','Sell'],
#                                 }},
#                     'ANZ.AX': { 'lines_scanned': 200,
#                                 'tot_revenue': 100,
#                                 'orders_data': {
#                                     'Date': ['2000/01/02','2000/01/03','2000/01/04','2000/01/05','2000/01/06','2000/01/07'],
#                                     'Price': [6,5,4,3,2,1],
#                                     'Volume': [100,100,100,100,100,100],
#                                     'Value': [200,400,600,800,1000,1200],
#                                     'Signal': ['Buy','Sell','Buy','Sell','Buy','Sell'],
#                                 }},
#                     'CBA.AX': { 'lines_scanned': 300,
#                                 'tot_revenue': 2,
#                                 'orders_data': {
#                                     'Date': ['2000/01/02','2000/01/03','2000/01/04','2000/01/05','2000/01/06','2000/01/07'],
#                                     'Price': [9,8,7,6,5,4],
#                                     'Volume': [100,100,100,100,100,100],
#                                     'Value': [100,300,500,700,900,1100],
#                                     'Signal': ['Buy','Sell','Buy','Sell','Buy','Sell'],
#                                 }}},
#     'BuyHard': { 'BHP.AX': { 'lines_scanned': 100,
#                                 'tot_revenue': 9000,
#                                 'orders_data': {
#                                     'Date': ['2000/01/02','2000/01/03','2000/01/04','2000/01/05','2000/01/06','2000/01/07'],
#                                     'Price': [4,5,6,7,8,9],
#                                     'Volume': [100,100,100,100,100,100],
#                                     'Value': [150,250,350,450,550,650],
#                                     'Signal': ['Buy','Sell','Buy','Sell','Buy','Sell'],
#                                 }},
#                     'ANZ.AX': { 'lines_scanned': 200,
#                                 'tot_revenue': 100,
#                                 'orders_data': {
#                                     'Date': ['2000/01/02','2000/01/03','2000/01/04','2000/01/05','2000/01/06','2000/01/07'],
#                                     'Price': [1,3,5,7,8,9],
#                                     'Volume': [100,100,100,100,100,100],
#                                     'Value': [250,450,650,850,1500,1250],
#                                     'Signal': ['Buy','Sell','Buy','Sell','Buy','Sell'],
#                                 }},
#                     'CBA.AX': { 'lines_scanned': 300,
#                                 'tot_revenue': 2,
#                                 'orders_data': {
#                                     'Date': ['2000/01/02','2000/01/03','2000/01/04','2000/01/05','2000/01/06','2000/01/07'],
#                                     'Price': [2,4,6,8,10],
#                                     'Volume': [100,100,100,100,100,100],
#                                     'Value': [150,350,550,750,950,1150],
#                                     'Signal': ['Buy','Sell','Buy','Sell','Buy','Sell'],
#                                 }}}}
#
run_option = ['normal']
# companies = ['BHP.AX','ANZ.AX','CBA.AX']
# strategies = ['WolfOfSeng', 'BuyHard']
# # strategies = ['N=3,TH=0.001', 'N=4,TH=0.02']
date_range_from = 2000
date_range_to = 2005
SO = ScrapeOrders()
SO.iterate_orders(['WolfOfSeng-ordersSTD0-4-0.001.csv', 'WolfOfSeng-ordersSTD1-5-0.02.csv', 'WolfOfSeng-ordersSTD2-4-0.001.csv', 'WolfOfSeng-ordersSTD3-6-0.05.csv'])
print SO.companies
print SO.strategies
# DM = DataManipulator(master_array, run_option, companies, strategies, date_range_from, date_range_to)
DM = DataManipulator(SO.orders,
                    run_option,
                    SO.companies,
                    SO.strategies,
                    date_range_from,
                    date_range_to)
strategy_performance_report_builder(DM)
