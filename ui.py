import dearpygui.dearpygui as dpg

#from utils import marketData


class ui():
    def __init__(self):
        dpg.create_context()
        dpg.create_viewport(title='Trading Bot V2 Viz', width=960, height=540)
        with dpg.window(tag='main_window'):
            pass

    def show_ui(self):
        dpg.setup_dearpygui()
        dpg.set_primary_window('main_window', True)
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def create_main_ui(self, marketData, strategy, callback, backend):
        with dpg.table(parent='main_window', tag='table', header_row=False, resizable=True,
                       borders_outerH=True, borders_innerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column()
            dpg.add_table_column()
            with dpg.table_row():
                # create main graph
                with dpg.plot(tag='candle_plot', width=-1, height=600):
                    dpg.add_plot_legend()
                    xAxis = dpg.add_plot_axis(
                        dpg.mvXAxis, label='Dates', time=True)
                    with dpg.plot_axis(dpg.mvYAxis, label='EUR'):
                        dpg.add_candle_series(dates=marketData.time, opens=marketData.open,
                                              highs=marketData.high, lows=marketData.low, closes=marketData.close, label='BTC')
                        dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xAxis)
                # create parameter manipulators
                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    for key in strategy.vars:
                        with dpg.table_row():
                            dpg.add_input_text(
                                label=str(key),
                                tag=str(key), decimal=True, default_value=strategy.vars[key],
                                callback=callback)
            with dpg.table_row():
                # create subplot
                with dpg.plot(width=-1, height=-1):
                    dpg.add_plot_legend()
                    xAxis = dpg.add_plot_axis(dpg.mvXAxis, time=True)
                    with dpg.plot_axis(dpg.mvYAxis, label='balanceOverTime'):
                        dpg.add_line_series(
                            tag='balance_over_time', label='blance over time', x=marketData.time, y=backend['BalanceOverTime'])
                        dpg.add_line_series(
                            tag='eur_over_time', label='eur_over_time', x=marketData.time, y=backend['EurOverTime'])
                # create stats
                with dpg.table(header_row=False, borders_innerH=True, borders_innerV=True):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    with dpg.table_row():
                        dpg.add_text('Total gains')
                        dpg.add_text(
                            tag='total_gains', default_value=backend['BalanceOverTime'][-1]-backend['BalanceOverTime'][0])
                    with dpg.table_row():
                        dpg.add_text('Total fees')
                        dpg.add_text(
                            tag='total_fees', default_value=backend['fees'])
                    with dpg.table_row():
                        dpg.add_text('Transactions')
                        dpg.add_text(tag='transactions',
                                     default_value=backend['BuyOperations']+backend['SellOperations'])
                    with dpg.table_row():
                        dpg.add_text('Buys')
                        dpg.add_text(tag='buys',
                                     default_value=backend['BuyOperations'])
                    with dpg.table_row():
                        dpg.add_text('Sells')
                        dpg.add_text(tag='sells',
                                     default_value=backend['SellOperations'])

    def updateTest(self, marketData, results):
        dpg.set_value('balance_over_time', [
                      marketData.time, results['BalanceOverTime']])
        dpg.set_value('eur_over_time', [
                      marketData.time, results['EurOverTime']])
        dpg.set_value(
            'total_gains', results['BalanceOverTime'][-1]-results['BalanceOverTime'][0])
        dpg.set_value('total_fees',
                      results['fees'])
        dpg.set_value('transactions',
                      results['BuyOperations']+results['SellOperations'])
        dpg.set_value('buys',
                      results['BuyOperations'])
        dpg.set_value('sells',
                      results['SellOperations'])
