# from strategy_performance_report import strategy_performance_report_builder
import datetime

month_convertor = {
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
    'DEC': 12
}

class DataManipulator:

    def __init__(self, master_array, modules, run_option, companies, strategies, date_range_from, date_range_to):
        #1st dimension is company, 2nd dimension is date/row, 3rd dimension is the different data for the date.
        #1st index of 3rd dimension is Company, 2nd: Date, 3rd: Price, 4th: Volume, 5th: Value (Price * Volume), 6th: Buy/Sell
        self.__master_array = master_array
        self.__modules = modules
        self.__run_option = run_option
        self.__companies = companies
        self.__strategies = strategies
        self.__date_range_from = date_range_from
        self.__date_range_to = date_range_to


        # self.__file_names = file_names
        self.__combined_revenue = { # Obviously need to calculate some values here
            'WolfOfSeng': {
                'pl_over_time': [100,200,0,-50,-60],
                'dates': ['2000/01/01','2000/01/03','2000/01/05','2000/01/07','2000/01/09']
            },
            'BuyHard': {
                'pl_over_time': [-60,5,-10,-20,-30],
                'dates': ['2000/01/02','2000/01/04','2000/01/06','2000/01/08','2000/01/10']
            }
        }

    # @property
    # def master_array(self):
    #     return self.__master_array

    @property
    def combined_revenue(self):
        return self.__combined_revenue

    @property
    def modules(self):
        return self.__modules

    @property
    def run_option(self):
        return self.__run_option

    @property
    def companies(self):
        return self.__companies

    @property
    def strategies(self):
        return self.__strategies

    @property
    def date_range_from(self):
        return self.__date_range_from

    @property
    def date_range_to(self):
        return self.__date_range_to

    def strategy_company_summary(self, strategy):
        return self.__master_array[strategy]

    def total_revenue(self, strategy, company):
        values = self.__master_array[strategy][company]['orders_data']['Value']
        signals = self.__master_array[strategy][company]['orders_data']['Signal']
        total_revenue = 0
        if len(signals) % 2 != 0:
            length = len(signals) - 1
        else:
            length = len(signals)
        for i in range(length):
            total_revenue += (values[i] if signals[i] == 'Sell' else (values[i]*-1))
        return total_revenue
        # return self.__master_array[strategy][company]['tot_revenue']

    def strategy_company_data_len(self, strategy, company):
        return len(self.__master_array[strategy][company]['orders_data']['Date'])

    def strategy_company_dates(self, strategy, company):

        # def convertor(date_string):
        #     date_components = date_string.split('-')
        #     return datetime.date(int(date_components[2]), month_convertor[date_components[1]], int(date_components[0]))

        return self.__master_array[strategy][company]['orders_data']['Date']

    def strategy_company_prices(self, strategy, company):
        return self.__master_array[strategy][company]['orders_data']['Price']

    def strategy_company_volumes(self, strategy, company):
        return self.__master_array[strategy][company]['orders_data']['Volume']

    def strategy_company_values(self, strategy, company):
        return self.__master_array[strategy][company]['orders_data']['Value']

    def strategy_company_signals(self, strategy, company):
        return self.__master_array[strategy][company]['orders_data']['Signal']
