import dearpygui.dearpygui as dpg

#from utils import marketData


class ui():
    def __init__(self):
        dpg.create_context()
        dpg.configure_app(init_file="dpg.ini")
        dpg.create_viewport(title='Trading Bot V2 Viz', width=960, height=540)
        with dpg.window(tag='main_window'):
            pass

    def show_ui(self):
        dpg.setup_dearpygui()
        dpg.set_primary_window('main_window', True)
        # dpg.show_implot_demo()
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
                with dpg.plot(tag='candle_plot', width=-1, height=400):
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
                # create subplots
                with dpg.plot(width=-1, height=-1):
                    dpg.add_plot_legend()
                    xAxis = dpg.add_plot_axis(dpg.mvXAxis, time=True)
                    with dpg.plot_axis(dpg.mvYAxis, label='balanceOverTime'):
                        for result in backend:
                            if type(backend[result]) == list:
                                dpg.add_line_series(tag=str(result), label=str(
                                    result), x=marketData.time, y=backend[result])

                # create stats
                with dpg.table(header_row=False, borders_innerH=True, borders_innerV=True):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    for result in backend:
                        if type(backend[result]) == int or type(backend[result]) == float:
                            with dpg.table_row():
                                dpg.add_text(str(result))
                                dpg.add_text(tag=str(result),
                                             default_value=backend[result])

        with dpg.menu_bar(parent='main_window'):
            with dpg.menu(label="File"):
                dpg.add_menu_item(
                    label="Save layout", callback=lambda: dpg.save_init_file("dpg.ini"))
                dpg.add_menu_item(
                    label="Quit", callback=lambda: dpg.destroy_context())

    def updateTest(self, marketData, backend):
        # update the graphs
        #
        # dpg.set_value('balance_over_time', [
        #              marketData.time, backend['BalanceOverTime']])
        # dpg.set_value('eur_over_time', [
        #              marketData.time, backend['EurOverTime']])
        # dpg.set_value('compared_performance', [
        #              marketData.time, backend['ComparedPerformance']])
        # update the value table
        for result in backend:
            if type(backend[result]) == int or type(backend[result]) == float:
                dpg.set_value(str(result), backend[result])
            elif type(backend[result]) == list:
                dpg.set_value(str(result), [marketData.time, backend[result]])
