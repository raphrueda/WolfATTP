import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import datetime
from dataManipulator import DataManipulator
from scrapOrders import scrapOrders

"""
This the Performance Strategy Report Builder will take in a DataManipulator
object and create an Excel file that will detail and visualise the results of
the algorithmic trading strategy module.

"""

def create_summary_page(DM, workbook):
    #####################################################
    ####                GLOBAL FORMATS              #####
    #####################################################
    money = workbook.add_format({'num_format': '$#,##0.00'})
    date = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    percent = workbook.add_format({'num_format': '0.00\%;-0.00\%'})
    number = workbook.add_format({'num_format': '0.0#;-0.0#'})
    company_list = DM.getCompanyList()
    table_row = 5

    # Create the summary worksheet and add the static headers
    summary_worksheet = workbook.add_worksheet('Strategy Summary')
    summary_worksheet.set_column('B:C', 14)
    summary_worksheet.set_column('D:E', 18)
    summary_worksheet.merge_range('A1:B1', 'Strategy : ', workbook.add_format({'bold': True, 'font_size': 23}))
    summary_worksheet.merge_range('C1:F1', DM.getStrategyEmployed(), workbook.add_format({'bold': True, 'font_size': 23}))
    summary_worksheet.write('A' + str(table_row - 2) + ':E' + str(table_row-2), 'Performance Overview', workbook.add_format({'bold': True, 'font_size': 20}))

    # Make a table that will briefly compare any companies
    summary_worksheet.write_row('A' + str(table_row), ['Company', 'Lines Scanned', 'Overall Profit ($)', 'Highest Gain/Loss ($)', 'Lowest Gain/Loss ($)'], workbook.add_format({'bold': True}))
    table_row = table_row + 1
    for company in company_list:
        summary_worksheet.write('A' + str(table_row), company)
        summary_worksheet.write('B' + str(table_row), DM.getNumOfLine(company))
        summary_worksheet.write('C' + str(table_row), DM.getOverallRevenue(company))
        summary_worksheet.write('D' + str(table_row), DM.maxProfit(company)[0])
        summary_worksheet.write('E' + str(table_row), DM.minProfit(company)[0])
        table_row = table_row + 1

    # Graph No.1 : Compares the return percentages of each company
    profit_per_bs_pair_chart = workbook.add_chart({'type': 'line'})
    profit_per_bs_pair_chart.set_title({'name': 'Returns per B/S pair per Company'})
    profit_per_bs_pair_chart.set_size({'width': 1080, 'height': 720})
    profit_per_bs_pair_chart.set_x_axis({
        'date_axis': True
    })
    profit_per_bs_pair_chart.set_y_axis({
        'name': 'Return (%)'
    })

    for company in company_list:
        company_profit_per_bs = DM.profitFromTransactionAsPercentage(company)
        profit_per_bs_pair_chart.add_series({
            'name': company,
            'values': '=' + company + "!$G$8:$G$" + str(7 + len(company_profit_per_bs)),
            'categories': '=' + company + "!$A$8:$A$" + str(7 + len(company_profit_per_bs)),
        })

    summary_worksheet.insert_chart('H4', profit_per_bs_pair_chart)

    # Graph No.2 : Compares the cumulative return percentages of each company
    cumulative_returns_chart = workbook.add_chart({'type': 'line'})
    cumulative_returns_chart.set_title({'name': 'Cumulative Return per Company'})
    cumulative_returns_chart.set_size({'width': 1080, 'height': 720})
    cumulative_returns_chart.set_x_axis({
        'date_axis': True
    })
    cumulative_returns_chart.set_y_axis({
        'name': 'Return (%)'
    })

    for company in company_list:
        cumulative_returns = DM.cumulativePercentage(company)
        cumulative_returns_chart.add_series({
            'name': company,
            'values': '=' + company + "!$I$8:$I$" + str(7 + len(cumulative_returns)),
            'categories': '=' + company + "!$A$8:$A$" + str(7 + len(cumulative_returns)),
        })

    summary_worksheet.insert_chart('H48', cumulative_returns_chart)
    return workbook

def create_company_page(DM, workbook, company):
    #####################################################
    ####                GLOBAL FORMATS              #####
    #####################################################
    money = workbook.add_format({'num_format': '$#,##0.00'})
    date = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    percent = workbook.add_format({'num_format': '0.00\%;-0.00\%'})
    number = workbook.add_format({'num_format': '0.0#;-0.0#'})
    worksheet = workbook.add_worksheet(company)

    # Setting the width of the first few columns for formatting purposes
    for i in range(0,5):
        worksheet.set_column(i,i,11)

    # Static header stuff at the beginning of the sheet
    company_row = 0
    company_col = 0
    company_header = 'Company : '
    company_header_format = workbook.add_format({'bold': True, 'font_size': 18})

    worksheet.merge_range("" + xl_rowcol_to_cell(company_row, company_col) + ':' + xl_rowcol_to_cell(company_row, company_col + 4) + "", company_header + company, company_header_format)

    time_frame_row = company_row + 1
    time_frame_col = 0
    time_frame_header = 'Time Frame : '
    time_frame_from = DM.getDateRangeTo()
    time_frame_to = DM.getDateRangeFrom()
    time_frame_header_format = workbook.add_format({'bold': True})
    return_header_format = workbook.add_format({'bold': True, 'align': 'center'})

    worksheet.merge_range(xl_rowcol_to_cell(time_frame_row, time_frame_col) + ':' + xl_rowcol_to_cell(time_frame_row, time_frame_col + 1), time_frame_header, time_frame_header_format)

    worksheet.write(time_frame_row, time_frame_col + 2, time_frame_from)
    worksheet.write(time_frame_row, time_frame_col + 3, 'to', workbook.add_format({'align': 'center'}))
    worksheet.write(time_frame_row, time_frame_col + 4, time_frame_to)

    revenue_row = time_frame_row + 1
    revenue_col = 0
    revenue_header = 'Total Revenue : '
    revenue_amount = DM.getOverallRevenue(company)
    revenue_header_format = workbook.add_format({'bold': True})

    worksheet.merge_range(xl_rowcol_to_cell(revenue_row, revenue_col) + ':' + xl_rowcol_to_cell(revenue_row, revenue_col + 1), revenue_header, revenue_header_format)
    worksheet.write(revenue_row, revenue_col + 2, revenue_amount, money)

    return_row = revenue_row + 1
    return_col = 0
    return_header = 'Total Return : '
    return_amount = DM.getOverallPercentage(company)
    worksheet.merge_range(xl_rowcol_to_cell(return_row, return_col) + ':' + xl_rowcol_to_cell(return_row, return_col + 1), return_header, revenue_header_format)
    worksheet.write(return_row, return_col + 2, return_amount, percent)
    worksheet.merge_range(xl_rowcol_to_cell(return_row, return_col + 3) + ':' + xl_rowcol_to_cell(return_row, return_col + 4), 'over initial investment', return_header_format)
    # worksheet.write(return_row, return_col + 3, 'over initial investment')
    worksheet.write(return_row, return_col + 5, '=ABS(E8)', money)



    # Putting in the numerical market data for the company
    dates = DM.getCompanyDates(company)
    prices = DM.getCompanyPrices(company)
    volumes = DM.getCompanyVolumes(company)
    signals = DM.getCompanySignals(company)
    cash_flows = DM.cashFlow(company)
    profits = DM.profitFromTransactionAsPrice(company)
    returns = DM.profitFromTransactionAsPercentage(company)
    cumulative_profits = DM.cumulativeProfit(company)
    cumulative_returns = DM.cumulativePercentage(company)

    table_header = workbook.add_format({'bold': True})
    worksheet.set_column('F:I', 18)
    worksheet.write('A7', 'Date', table_header)
    worksheet.write_column('A8', dates, date)

    worksheet.write('B7', 'Price ($)', table_header)
    worksheet.write_column('B8', prices, money)

    worksheet.write('C7', 'Volume', table_header)
    worksheet.write_column('C8', volumes)

    worksheet.write('D7', 'Signal', table_header)
    worksheet.write_column('D8', signals)

    worksheet.write('E7', 'Cash Flow ($)', table_header)
    worksheet.write_column('E8', cash_flows)

    worksheet.write('F7', 'Profit per B/S pair ($)', table_header)
    worksheet.write_column('F8', profits, number)

    worksheet.write('G7', 'Profit per B/S pair (%)', table_header)
    worksheet.write_column('G8', returns, percent)

    worksheet.write('H7', 'Culminative Profit ($)', table_header)
    worksheet.write_column('H8', cumulative_profits, number)

    worksheet.write('I7', 'Culminative Profit (%)', table_header)
    worksheet.write_column('I8', cumulative_returns, percent)


    #####################################################
    ####                    CHART                   #####
    #####################################################
    chart_pos_counter = 7
    chart_pos_offset = 43

    # Chart No. 1 : Scatter chart which shows the what the cashflow values were
    cash_flow_chart = workbook.add_chart({'type': 'scatter'})
    cash_flow_chart.set_title({'name': 'Cash Flow'})

    cash_flow_chart.add_series({
        'name': 'Buy / Sell Amount',
        'values': '=' + company + "!$E$8:$E$" + str(7 + len(cash_flows)),
        'categories': '=' + company + "!$A$8:$A$" + str(7 + len(cash_flows)),
        'marker': {'type': 'circle', 'size': 2},
    })

    cash_flow_chart.set_y_axis({
        'name': 'Cashflow Amount ($)'
    })

    cash_flow_chart.set_x_axis({
        'date_axis': True,
    })

    cash_flow_chart.set_legend({'none': True})
    cash_flow_chart.set_size({'width': 1080, 'height': 720})

    worksheet.insert_chart('L'+str(chart_pos_counter), cash_flow_chart)
    chart_pos_counter = chart_pos_counter + chart_pos_offset


    # Chart No.2: A chart that shows the cumulative return from the initial investment at a given point in time
    culminative_profit_percent_chart = workbook.add_chart({'type': 'line'})
    culminative_profit_percent_chart.set_title({'name': 'Culminative Return on Initial Investment'})

    culminative_profit_percent_chart.set_legend({'none': True})
    culminative_profit_percent_chart.set_size({'width': 1080, 'height': 720})

    culminative_profit_percent_chart.add_series({
        'name': 'Culminative Profit Percent',
        'values': '=' + company + "!$I$8:$I$" + str(7 + len(cumulative_returns)),
        'categories': '=' + company + "!$A$8:$A$" + str(7 + len(cumulative_returns)),
    })

    culminative_profit_percent_chart.set_y_axis({
        'name': 'Return (%)'
    })

    culminative_profit_percent_chart.set_x_axis({
        'date_axis': True,
        'min': dates[0],
        'max': dates[len(dates)-1],
    })

    worksheet.insert_chart('L'+str(chart_pos_counter), culminative_profit_percent_chart)
    chart_pos_counter = chart_pos_counter + chart_pos_offset


    # Chart No.3 : A chart that shows the return received on each buy sell pair
    profit_per_bs_pair_percent_chart = workbook.add_chart({'type': 'line'})
    profit_per_bs_pair_percent_chart.set_title({'name': 'Return per B/S pair'})
    profit_per_bs_pair_percent_chart.set_legend({'none': True})
    profit_per_bs_pair_percent_chart.set_size({'width': 1080, 'height': 720})

    profit_per_bs_pair_percent_chart.add_series({
        'name': 'Profit per B/S pair',
        'values': '=' + company + "!$G$8:$G$" + str(7 + len(returns)),
        'categories': '=' + company + "!$A$8:$A$" + str(7 + len(returns)),
        'line':   {'width': 0.75},
    })

    profit_per_bs_pair_percent_chart.set_y_axis({
        'name': 'Return (%)'
    })

    profit_per_bs_pair_percent_chart.set_x_axis({
        'date_axis': True,
        'min': dates[0],
        'max': dates[len(dates)-1]
    })

    worksheet.insert_chart('L'+str(chart_pos_counter), profit_per_bs_pair_percent_chart)
    chart_pos_counter = chart_pos_counter + chart_pos_offset

    return workbook

def performance_strategy_report_builder(DM):
    strategy_name = DM.getStrategyEmployed()
    strategy_name = strategy_name.replace (" ", "")
    workbook = xlsxwriter.Workbook(strategy_name + '_Performance_Report.xlsx')
    workbook = create_summary_page(DM, workbook)
    company_list = DM.getCompanyList()

    for company in company_list:
        workbook = create_company_page(DM, workbook, company)

    workbook.close()
