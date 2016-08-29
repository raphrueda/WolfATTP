import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import datetime
from time import time

"""
This the Performance Strategy Report Builder will take in a DataManipulator
object and create an Excel file that will detail and visualise the results of
the algorithmic trading strategy module.

"""

def date_convertor(date_string):
    date_components = map(int, date_string.split('/'))
    return datetime.date(date_components[0], date_components[1], date_components[2])

def strategy_namer(table_height, strategy):
    strategy_names = []
    for i in range(table_height):
        strategy_names.append(strategy)
    return strategy_names

def cash_flow_formulas(table_height, cash_flow_col, top_table_row):
    formulas = []
    for i in range(table_height):
        signal_cell = xl_rowcol_to_cell(top_table_row, cash_flow_col - 1)
        value_cell = xl_rowcol_to_cell(top_table_row, cash_flow_col - 2)
        formulas.append('=IF(' + signal_cell + '="Buy",' + value_cell + '* -1,' + value_cell +')') # Looks like =IF($E$14="Buy", $F$14*-1, $F$14)
        top_table_row += 1
    return formulas

def pl_per_bs_formulas(table_height, cash_flow_col, top_table_row):
    formulas = []
    for i in range(table_height):
        if i % 2 == 0:
            formulas.append('=NA()')
        else:
            prev_value_cell = xl_rowcol_to_cell(top_table_row - 1, cash_flow_col - 1)
            value_cell = xl_rowcol_to_cell(top_table_row, cash_flow_col - 1)
            formulas.append('=(' + prev_value_cell + '+' + value_cell + ')') # Looks like =G13+G14 where both cells could be +'ve or -'ve
        top_table_row += 1
    return formulas

def pl_per_bs_percent_formulas(table_height, cash_flow_col, top_table_row):
    formulas = []
    for i in range(table_height):
        if i % 2 == 0:
            formulas.append('=NA()')
        else:
            prev_value_cell = xl_rowcol_to_cell(top_table_row - 1, cash_flow_col - 2)
            value_cell = xl_rowcol_to_cell(top_table_row, cash_flow_col - 2)
            formulas.append('=(' + prev_value_cell + '+' + value_cell + ')/ABS(' + prev_value_cell + ')') # Looks like =ABS(G13-G14)
        top_table_row += 1
    return formulas

def pl_over_time_formulas(table_height, cash_flow_col, top_table_row):
    formulas = ['=NA()', '=' + xl_rowcol_to_cell(top_table_row + 1, cash_flow_col - 2) + '+ 0']
    top_table_row += 2
    for i in range(table_height - 2):
        if i % 2 == 0:
            formulas.append('=NA()')
        else:
            prev_cul_pl_cell = xl_rowcol_to_cell(top_table_row - 2, cash_flow_col)
            cul_pl_cell = xl_rowcol_to_cell(top_table_row, cash_flow_col - 2)
            formulas.append('=(' + prev_cul_pl_cell + '+' + cul_pl_cell + ')') # Looks like =(G13+G14)
        top_table_row += 1
    return formulas

def pl_over_time_percent_formulas(table_height, pl_over_time_col, top_table_row):
    formulas = []
    ini_invest_cell = xl_rowcol_to_cell(top_table_row, pl_over_time_col - 6, row_abs=True, col_abs=True)
    for i in range(table_height):
        if i % 2 == 0:
            formulas.append('=NA()')
        else:
            cul_pl_cell = xl_rowcol_to_cell(top_table_row, pl_over_time_col - 1)
            formulas.append('=(' + cul_pl_cell + '/' + ini_invest_cell + ')') # Looks like =(G13+G14)
        top_table_row += 1
    return formulas

def make_chart(workbook, worksheet, company, DM, chart_type, x_col,\
    y_col,  title, width, height, table_mark, x_axis_name, y_axis_name,\
    table2_height=None, table2_mark=None, x2_col=None, y2_col=None, x2_axis_name=None, y2_axis_name=None):
    chart = workbook.add_chart({'type': chart_type})
    chart.set_title({'name': title})

    # chart.set_legend({'none': True})
    chart.set_size({'width': width, 'height': height})

    for strategy in DM.strategies:
        table_height = DM.strategy_company_data_len(strategy, company)
        chart.add_series({
            'name': strategy,
            'values': '=' + company\
                    + '!'\
                    + xl_rowcol_to_cell(table_mark, y_col, row_abs=True, col_abs=True)\
                    + ':'\
                    + xl_rowcol_to_cell(table_mark + table_height - 1, y_col, row_abs=True, col_abs=True),
            'categories': '=' + company\
                        + '!'\
                        + xl_rowcol_to_cell(table_mark, x_col, row_abs=True, col_abs=True)\
                        + ':'\
                        + xl_rowcol_to_cell(table_mark + table_height - 1, x_col, row_abs=True, col_abs=True),
        })
        table_mark += table_height

    chart.set_y_axis({
        'name': y_axis_name
    })

    chart.set_x_axis({
        'date_axis': True
    })

    if x2_col and y2_col and y2_axis_name:
        chart.add_series({
            'name': strategy,
            'values': '=' + company\
                    + '!'\
                    + xl_rowcol_to_cell(table2_mark, y2_col, row_abs=True, col_abs=True)\
                    + ':'\
                    + xl_rowcol_to_cell(table2_mark + table_height - 1, y2_col, row_abs=True, col_abs=True),
            'categories': '=' + company\
                        + '!'\
                        + xl_rowcol_to_cell(table2_mark, x2_col, row_abs=True, col_abs=True)\
                        + ':'\
                        + xl_rowcol_to_cell(table2_mark + table_height - 1, x2_col, row_abs=True, col_abs=True),
            'y2_axis': True
        })

        chart.set_y2_axis({
            'name': y2_axis_name
        })

        chart.set_x2_axis({
            'date_axis': True
        })


    return chart

def create_summary_page(DM, workbook):
    money = workbook.add_format({'num_format': '$#,##0.00'})
    date = workbook.add_format({'num_format': 'yyyy/mm/dd'})
    percent = workbook.add_format({'num_format': '0.00%;-0.00%'})
    number = workbook.add_format({'num_format': '0.0#;-0.0#'})
    right_align = workbook.add_format({'align': 'right'})
    center_bold = workbook.add_format({'align': 'center', 'bold': True, 'border': 5})
    company_list = DM.companies
    inc = 1
    curr_row_lvl = 2

    # Create the summary worksheet and add the static headers
    summary_worksheet = workbook.add_worksheet('Report Summary')
    summary_worksheet.set_column('A:ZZ', 24)

    modules = ' - '.join(DM.modules)
    summary_worksheet.merge_range('A1:Z1', modules + ' Performance Report', workbook.add_format({'bold': True, 'font_size': 24}))

    summary_worksheet.write('A' + str(curr_row_lvl), 'SIMULATION DATE :', right_align)
    summary_worksheet.write('B' + str(curr_row_lvl), datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S'))
    curr_row_lvl += inc

    for strategy in DM.strategies:
        summary_worksheet.write('A' + str(curr_row_lvl) , strategy + ' TOTAL REVENUE:', right_align)
        total_rev = 0 if len(DM.combined_revenue[strategy]['cumulative_profit_loss']) == 0 else DM.combined_revenue[strategy]['cumulative_profit_loss'][-1]
        summary_worksheet.write('B' + str(curr_row_lvl) , total_rev , right_align)
        curr_row_lvl += inc

    table_row = curr_row_lvl + inc
    table_col = 0
    table_data = {
        'style': 'Table Style Light 9',
        'total_row': True,
        'columns': [{'header': 'COMPANY'},
                    {'header': 'LINES SCANNED', 'total_string': 'OVERALL REVENUE =', 'format': right_align},
                    {'header': 'TOTAL REVENUE ($)', 'total_function':'sum'}]
    }
    for i in range(len(DM.strategies)):
        data = []
        company_summary = DM.strategy_company_summary(DM.strategies[i])
        for key in company_summary.keys():
                data.append([key, company_summary[key]['lines_scanned'], DM.total_revenue(DM.strategies[i], key)])

        table_data = {
            'data': data,
            'style': 'Table Style Light 9',
            'total_row': True,
            'columns': [{'header': 'COMPANY'},
                        {'header': 'LINES SCANNED', 'total_string': 'OVERALL REVENUE =', 'format': right_align},
                        {'header': 'TOTAL REVENUE ($)', 'total_function':'sum'}]
        }
        summary_worksheet.merge_range(xl_rowcol_to_cell(table_row - 1, table_col) + ':' + xl_rowcol_to_cell (table_row - 1, table_col + 2), DM.strategies[i], center_bold)
        summary_worksheet.add_table(xl_rowcol_to_cell(table_row, table_col) + ':' + xl_rowcol_to_cell (table_row + 1 + len(DM.companies), table_col + 2), table_data)
        table_col += 3

    temp_data_row = curr_row_lvl
    temp_data_col = table_col + 8

    total_profit_chart = workbook.add_chart({'type': 'line'})
    total_profit_chart.set_title({'name': 'Total P/L vs Time'})
    total_profit_chart.set_size({'width': 1080, 'height': 720})
    total_profit_chart.set_x_axis({'date_axis': True})
    # total_profit_chart.set_x_axis({'date_axis': True, 'min': datetime.date(1990, 1, 1), 'max': datetime.date(2015, 12, 30),})
    total_profit_chart.set_y_axis({'name': 'P/L ($)'})
    for key in DM.combined_revenue.keys():
        summary_worksheet.merge_range(xl_rowcol_to_cell(temp_data_row - 1, temp_data_col) + ':' + xl_rowcol_to_cell(temp_data_row -1, temp_data_col + 1), key, workbook.add_format({'bold': True, 'font_size': 24}))
        summary_worksheet.write(xl_rowcol_to_cell(temp_data_row, temp_data_col), 'Date')
        summary_worksheet.write(xl_rowcol_to_cell(temp_data_row, temp_data_col + 1), 'Total Profit For Date')
        summary_worksheet.write_column(xl_rowcol_to_cell(temp_data_row + 1, temp_data_col), DM.combined_revenue[key]['Dates'])
        summary_worksheet.write_column(xl_rowcol_to_cell(temp_data_row + 1, temp_data_col + 1), DM.combined_revenue[key]['cumulative_profit_loss'])
        total_profit_chart.add_series({
            'name': key,
            'values': "='Report Summary'!" + xl_rowcol_to_cell(temp_data_row + 1, temp_data_col + 1, row_abs=True, col_abs=True) + ":" + xl_rowcol_to_cell(temp_data_row + len(DM.combined_revenue[key]['Dates']), temp_data_col + 1, row_abs=True, col_abs=True),
            'categories': "='Report Summary'!" + xl_rowcol_to_cell(temp_data_row + 1, temp_data_col, row_abs=True, col_abs=True) + ":" + xl_rowcol_to_cell(temp_data_row + len(DM.combined_revenue[key]['Dates']), temp_data_col, row_abs=True, col_abs=True),
        })
        temp_data_col += 2
    summary_worksheet.insert_chart(xl_rowcol_to_cell(table_row ,table_col + 1), total_profit_chart)

    return workbook

def create_company_page(DM, workbook, company):
    ##########  FORMATS ##########
    right_align = workbook.add_format({'align': 'right'})
    center_bold = workbook.add_format({'align': 'center', 'bold': True, 'border': 5})
    date = workbook.add_format({'num_format': 'yyyy/mm/dd'})
    percent = workbook.add_format({'num_format': '0.00%;-0.00%'})
    number = workbook.add_format({'num_format': '0.0#;-0.0#'})

    ##########  HEADERS ##########
    company_worksheet = workbook.add_worksheet(company)
    company_worksheet.set_column('A:ZZ', 20)
    company_worksheet.merge_range('A1:Z1', company, workbook.add_format({'bold': True, 'font_size': 24}))
    company_worksheet.write_column('A2', ['START DATE :','END DATE :'], right_align)

    ##########  SUMMARY TABLE ##########
    table_top_left = 'A5'
    table_row = 5
    table_col = 0  # The first col of the table

    data = []
    for strategy in DM.strategies:
        s_name = strategy
        if company not in DM.strategy_company_summary(strategy).keys():
            ini_invest = 0
            tot_return = 0
            tot_revenue = 0
        else:
            ini_invest = DM.strategy_company_summary(strategy)[company]['orders_data']['Value'][0]
            tot_revenue = DM.total_revenue(strategy, company)
            tot_return = '=' + xl_rowcol_to_cell(table_row, table_col + 2, row_abs=True, col_abs=True) + '/' + xl_rowcol_to_cell(table_row, table_col + 1, row_abs=True, col_abs=True)
        data.append([s_name, ini_invest, tot_revenue, tot_return])
        table_row += 1

    table_data = {
        'data': data,
        'style': 'Table Style Light 9',
        'columns': [{'header': 'STRATEGY'},
                    {'header': 'INITIAL INVESTMENT'},
                    {'header': 'TOTAL REVENUE ($)'},
                    {'header': 'TOTAL RETURN (%)', 'format': percent}]
    }

    company_worksheet.add_table(table_top_left + ':' + xl_rowcol_to_cell(table_row, table_col + 3), table_data)

    ##########  RAW DATA ##########
    raw_data_row_top = 12
    raw_data_col_left = 0

    table_height = 0
    for strategy in DM.strategies:
        table_height += DM.strategy_company_data_len(strategy,company)

    table_data = {
        'style': 'Table Style Light 9',
        'columns': [{'header': 'STRATEGY'},
                    {'header': 'DATE/TIME'},
                    {'header': 'PRICE'},
                    {'header': 'VOLUME'},
                    {'header': 'VALUE'},
                    {'header': 'BID/ASK'},
                    {'header': 'CASH FLOW'},
                    {'header': 'P/L PER B/S PAIR ($)'},
                    {'header': 'P/L PER B/S PAIR (%)'},
                    {'header': 'CUMULATIVE P/L ($)'},
                    {'header': 'CUMULATIVE P/L (%)'}]
    }

    company_worksheet.add_table('A13:K' + str(13 + table_height), table_data) # HACKY

    table_col = 0
    table_mark = 13
    for strategy in DM.strategies:
        table_height = DM.strategy_company_data_len(strategy, company)
        company_worksheet.write_column(xl_rowcol_to_cell(table_mark, table_col), strategy_namer(table_height, strategy)) # STRATEGY
        company_worksheet.write_column(xl_rowcol_to_cell(table_mark, table_col + 1), DM.strategy_company_dates(strategy, company), date) # DATE/TIME
        company_worksheet.write_column(xl_rowcol_to_cell(table_mark, table_col + 2), DM.strategy_company_prices(strategy, company)) # PRICE
        company_worksheet.write_column(xl_rowcol_to_cell(table_mark, table_col + 3), DM.strategy_company_volumes(strategy, company)) # VOLUME
        company_worksheet.write_column(xl_rowcol_to_cell(table_mark, table_col + 4), DM.strategy_company_values(strategy, company)) # VALUE
        company_worksheet.write_column(xl_rowcol_to_cell(table_mark, table_col + 5), DM.strategy_company_signals(strategy, company)) # BID/ASK
        company_worksheet.write_column(xl_rowcol_to_cell(table_mark, table_col + 6), cash_flow_formulas(table_height, table_col + 6, table_mark)) # CASH FLOW
        company_worksheet.write_column(xl_rowcol_to_cell(table_mark, table_col + 7), pl_per_bs_formulas(table_height, table_col + 7, table_mark)) # P/L PER B/S PAIR ($)
        company_worksheet.write_column(xl_rowcol_to_cell(table_mark, table_col + 8), pl_per_bs_percent_formulas(table_height, table_col + 8, table_mark), percent) # P/L PER B/S PAIR (%)
        company_worksheet.write_column(xl_rowcol_to_cell(table_mark, table_col + 9), pl_over_time_formulas(table_height, table_col + 9, table_mark)) # CUMULATIVE P/L ($)
        company_worksheet.write_column(xl_rowcol_to_cell(table_mark, table_col + 10), pl_over_time_percent_formulas(table_height, table_col + 10, table_mark), percent) # CUMULATIVE P/L (%)
        table_mark += table_height


    ########## CHART MAKING TIME    ############
    chart_row = raw_data_row_top
    chart_col = 12
    chart_inc = 43
    company_worksheet.insert_chart(xl_rowcol_to_cell(chart_row, chart_col),\
        make_chart(workbook=workbook, worksheet=company_worksheet, company=company,\
                    DM=DM, chart_type='line', x_col=table_col + 1, y_col=table_col + 9,\
                    title='Cumulative P/L vs. time', width=1080, height=720,\
                    table_mark=raw_data_row_top + 1, x_axis_name='Date',\
                    y_axis_name='Profit($)'))
    chart_row += chart_inc

    company_worksheet.insert_chart(xl_rowcol_to_cell(chart_row, chart_col),\
        make_chart(workbook=workbook, worksheet=company_worksheet, company=company,\
                    DM=DM, chart_type='column', x_col=table_col + 1, y_col=table_col + 7,\
                    title='P/L per B/S pair vs. time', width=1080, height=720,\
                    table_mark=raw_data_row_top + 1, x_axis_name='Date',\
                    y_axis_name='Profit($)'))
    chart_row += chart_inc

    # table2_height=None, table2_mark=None, x2_col=None, y2_col=None, x2_axis_name=None, y2_axis_name=None
    # company_worksheet.insert_chart(xl_rowcol_to_cell(chart_row, chart_col), make_chart(workbook, company_worksheet, company, DM, 'column', table_col + 1, table_col + 9, 'P/L per B/S pair vs. Stock Price vs. time', 1080, 720, raw_data_row_top + 1, 'Profit($)', 'Time'))

    return workbook

def strategy_performance_report_builder(DM):
    file_name = 'Strategy_Performance_Report_' + datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx'
    workbook = xlsxwriter.Workbook(file_name)
    workbook = create_summary_page(DM, workbook)

    for company in DM.companies:
        workbook = create_company_page(DM, workbook, company)

    workbook.close()
    print file_name
