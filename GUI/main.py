import dearpygui.dearpygui as dpg
from math import sin


dpg.create_context()

image = "savedImage.png"
width, height, channels, data = dpg.load_image(image)


# creating data
sindatax = []
sindatay = []
for i in range(0, 500):
    sindatax.append(i / 1000)
    sindatay.append(0.5 + 0.5 * sin(50 * i / 1000))

with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    # default_font = dpg.add_font("Fonts/Noto.otf", 20)
    default_font = dpg.add_font("Fonts/Roboto.ttf", 15)


with dpg.window(tag="Top Window",width=1200, height=30, pos=(0,0)):
    dpg.bind_font(default_font)
    dpg.add_progress_bar( show=True, overlay='UTC',width=200,height=30,default_value=0.5,pos=(0,30))
    dpg.add_progress_bar( show=True, overlay='Bin Capacity',width=200,height=30,default_value=0.5,pos=(230,30))
    dpg.add_progress_bar( show=True, overlay='Battery',width=200,height=30,default_value=0.5,pos=(460,30))
    dpg.add_progress_bar( show=True, overlay='Rover Temp',width=200,height=30,default_value=0.5,pos=(690,30))

with dpg.window(tag="First Window",width=300, height=400, pos=(0,100), label='Control'):
    dpg.bind_font(default_font)
    with dpg.group(horizontal=True):
        dpg.add_button(width=90,height=50,label="Start" )
        dpg.add_button(width=90,height=50,label="Stop")

    with dpg.child_window(tag='Velocity', width=200, height=50,menubar=True, no_scrollbar=True):
        with dpg.menu_bar():
            dpg.add_menu(label="Velocity", enabled=False)
        dpg.add_text(default_value="m/s 0.0")

    with dpg.child_window(tag='Timer', width=200, height=50,menubar=True, no_scrollbar=True):
        with dpg.menu_bar():
            dpg.add_menu(label="Timer", enabled=False)
        dpg.add_text(default_value="Min 0:0")

    with dpg.child_window(tag='Bandwidth', width=200, height=50,menubar=True, no_scrollbar=True):
        with dpg.menu_bar():
            dpg.add_menu(label="Bandwith Used", enabled=False)
        dpg.add_text(default_value="k/b 0.0")

    with dpg.child_window(tag='Totol Power', width=200, height=50,menubar=True, no_scrollbar=True):
        with dpg.menu_bar():
            dpg.add_menu(label="Total Power Used", enabled=False)
        dpg.add_text(default_value="W/h 0.0")






with dpg.window(tag='Third Window', width=400, height=400, pos=(800,100),label='Telemetry'):
    dpg.bind_font(default_font)
    dpg.add_3d_slider(label="3D Slider", )
    # with dpg.plot(tag='Line Chart', height=380, width=400):
    # # optionally create legend
    #     dpg.add_plot_legend()

    #     # REQUIRED: create x and y axes
    #     dpg.add_plot_axis(dpg.mvXAxis, label="x")
    #     dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

    #     # series belong to a y axis
    #     dpg.add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)", parent="y_axis")

with dpg.window(tag='Bottom Window', width=1200, height=300, pos=(0,500),label='Surface Operations'):
    dpg.bind_font(default_font)
    with dpg.group(horizontal=True):
        dpg.add_listbox(items=["Start Up", "Calibration", "Pathing", "Excavation", "Deposition"], width=200, num_items=6)
        with dpg.child_window(tag='Action Responses', width=200, height=250,menubar=True):
            with dpg.menu_bar():
                dpg.add_menu(label="Action Responses", enabled=False)
            dpg.add_text(default_value="Start up")

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

            
with dpg.window(tag='Second Window', width=500, height=400, pos=(300,100), label='Camera Feed'):
        dpg.bind_font(default_font)

        with dpg.texture_registry(show=False):
            dpg.add_dynamic_texture(width, height, data, tag="texture_tag")

        dpg.add_image("texture_tag",width=490, height=350)

            

dpg.create_viewport(title='Rover Dashboard', width=1200, height=800)
dpg.setup_dearpygui()
dpg.show_font_manager()
dpg.show_item_registry()
dpg.show_viewport()
# dpg.start_dearpygui()


# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    # print("this will run every frame")
    image = "savedImage.png"
    width, height, channels, data = dpg.load_image(image)
    
    dpg.set_value("texture_tag", data)

    dpg.render_dearpygui_frame()

dpg.destroy_context()
