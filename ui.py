import dearpygui.dearpygui as dpg

# from utils import marketData


class ui():
    def __init__(self):
        dpg.create_context()
        dpg.configure_app(init_file="dpg.ini")
        dpg.create_viewport(title='Trading Bot V2 Viz', width=960, height=540)
        with dpg.window(tag='main_window'):
            pass
        self.annotations = []

    def show_ui(self):
        dpg.setup_dearpygui()
        dpg.set_primary_window('main_window', True)
        # dpg.show_implot_demo()
        # dpg.show_imgui_demo()
        dpg.configure_app(docking=True)
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def update_draggable_line(self, sender):
        val = dpg.get_value(sender)
        dpg.set_value('d_line', val)
        dpg.set_value('d_line_sub', val)

    def create_main_ui(self, marketData, strategy, update_ui, update_market_data, backend):
        with dpg.window(label='main candle graph', no_close=True):
            # create main graph
            with dpg.plot(tag='candle_plot', width=-1, height=-1):
                dpg.add_plot_legend()
                dpg.add_drag_line(
                    tag='d_line', callback=self.update_draggable_line, default_value=marketData.time[5])
                xAxis = dpg.add_plot_axis(
                    dpg.mvXAxis, label='Dates', time=True)
                with dpg.plot_axis(dpg.mvYAxis, label='EUR'):
                    dpg.add_candle_series(dates=marketData.time, opens=marketData.open, highs=marketData.high,
                                          lows=marketData.low, closes=marketData.close, label='BTC')
                    dpg.fit_axis_data(dpg.top_container_stack())
                dpg.fit_axis_data(xAxis)
            # create parameter manipulators
        with dpg.window(label='parameters', no_close=True):
            with dpg.table(header_row=False):
                dpg.add_table_column()
                for key in strategy.vars:
                    with dpg.table_row():
                        dpg.add_input_text(
                            label=str(key),
                            tag=str(key), decimal=True, default_value=strategy.vars[key],
                            callback=update_ui)
        with dpg.window(label='subplots', no_close=True):
            # create subplots
            with dpg.plot(width=-1, height=-1):
                dpg.add_plot_legend()
                dpg.add_drag_line(
                    tag='d_line_sub', callback=self.update_draggable_line, default_value=marketData.time[5])
                xAxis = dpg.add_plot_axis(dpg.mvXAxis, time=True)
                with dpg.plot_axis(dpg.mvYAxis, label='balanceOverTime'):
                    for result in backend:
                        if type(backend[result]) == list:
                            dpg.add_line_series(tag=str(result), label=str(
                                result), x=marketData.time, y=backend[result])
        with dpg.window(label='stats', no_close=True):
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

        with dpg.window(label='market data settings', no_close=True):
            # create the market data to fetch
            with dpg.table(header_row=False, borders_innerH=True, borders_innerV=True):
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_text('FIAT currency')
                    dpg.add_input_text(
                        uppercase=True, no_spaces=True, default_value='EUR', tag='FIAT currency')
                with dpg.table_row():
                    dpg.add_text('CRYPTO currency')
                    dpg.add_input_text(
                        uppercase=True, no_spaces=True, hexadecimal=True, default_value='BTC', tag='CRYPTO currency')
                # test duration input
                with dpg.table_row():
                    dpg.add_text('Start')
                    dpg.add_date_picker(level=0, default_value={
                        'month_day': 1, 'month': 0, 'year': 121, 'week_day': 5}, tag='market_start')
                with dpg.table_row():
                    dpg.add_text('End')
                    with dpg.group():
                        dpg.add_checkbox(
                            label='Use Current time', tag='use_current_time', default_value=True, callback=lambda: dpg.configure_item('maket_end', show=not dpg.get_item_configuration('maket_end')['show']))
                        dpg.add_date_picker(show=False, tag='maket_end')
                with dpg.table_row():
                    dpg.add_text('Time Interval')
                    dpg.add_combo(['1m', '3m', '5m', '15m', '30m',
                                  '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'], default_value='5m', tag='time_interval')
                with dpg.table_row():
                    dpg.add_text('Update Market Data')
                    dpg.add_button(label='Update', callback=update_market_data)

        with dpg.window(label='Simulation Settings', no_close=True):
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_checkbox(label='Auto Update', enabled=False)
                    dpg.add_button(
                        label='Update', tag='simulation_update_button', callback=update_ui)
        with dpg.menu_bar(parent='main_window'):
            with dpg.menu(label="File"):
                dpg.add_menu_item(
                    label="Save layout", callback=lambda: dpg.save_init_file("dpg.ini"))
                dpg.add_menu_item(
                    label="Quit", callback=lambda: dpg.destroy_context())

    def updateTest(self, marketData, backend):
        for result in backend:
            if type(backend[result]) == int or type(backend[result]) == float:
                dpg.set_value(str(result), backend[result])
            elif type(backend[result]) == list:
                dpg.set_value(str(result), [marketData.time, backend[result]])

        print(self.annotations)
        for i in self.annotations:
            dpg.delete_item(i)
        self.annotations = []
        for candle in range(len(backend['buysNsells'])):

            # buy operation
            backend['buysNsells'][candle]
            if backend['buysNsells'][candle] > 0:
                self.annotations.append(dpg.add_plot_annotation(label="", default_value=(
                    marketData.time[candle], marketData.high[candle]), offset=(0, -20), color=[0, 255, 0, 255], parent='candle_plot'))
            # sell operation
            elif backend['buysNsells'][candle] < 0:
                self.annotations.append(dpg.add_plot_annotation(label="", default_value=(
                    marketData.time[candle], marketData.low[candle]), offset=(0, 20), color=[255, 0, 0, 255], parent='candle_plot'))
