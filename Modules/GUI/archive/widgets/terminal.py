import dearpygui.dearpygui as dpg
from math import sin

# creating data
sindatax = []
sindatay = []
for i in range(0, 500):
    sindatax.append(i / 1000)
    sindatay.append(0.5 + 0.5 * sin(50 * i / 1000))




class Terminal():

    def CreateTerminal(default_font):
        with dpg.child_window(tag='Bottom Window', width=-1, height=300, pos=(0,550),label='Surface Operations'):
            dpg.bind_font(default_font)
            with dpg.group(horizontal=True):
                dpg.add_listbox(items=["Start Up", "Calibration", "Pathing", "Excavation", "Deposition"], width=200, num_items=6)
                with dpg.child_window(tag='Action Responses', width=200, height=250,menubar=True):
                    with dpg.menu_bar():
                        dpg.add_menu(label="Action Responses", enabled=False)
                    dpg.add_text(default_value="Start up", tag='status')

                with dpg.child_window(tag='Manual Input', width=200, height=250,menubar=True):
                    with dpg.menu_bar():
                        dpg.add_menu(label="Manual Input", enabled=False)
                    dpg.add_input_text(hint="Enter Value")

                with dpg.subplots(1, 2, label="Bandwidth & Power", width=-1, height=-1, row_ratios=[1.0, 1.0], column_ratios=[1.0, 1.0]) as subplot_id:

                    with dpg.plot(no_title=True):
                        dpg.add_plot_axis(dpg.mvXAxis, label="Kb", no_tick_labels=True)
                        with dpg.plot_axis(dpg.mvYAxis, label="Time", no_tick_labels=True):
                            dpg.add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)")
                    with dpg.plot(no_title=True):
                        dpg.add_plot_axis(dpg.mvXAxis, label="W/h", no_tick_labels=True)
                        with dpg.plot_axis(dpg.mvYAxis, label="Time", no_tick_labels=True):
                            dpg.add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)")
