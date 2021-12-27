import dearpygui.dearpygui as dpg
from math import sin


dpg.create_context()

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
    dpg.add_button(width=100,height=50,label="Start", pos=(20,60))
    dpg.add_button(width=100,height=50,label="Stop", pos=(140,60))
    dpg.add_text("Timer: ")




with dpg.window(tag='Second Window', width=500, height=400, pos=(300,100), label='Camera Feed'):
    dpg.bind_font(default_font)
    width, height, channels, data = dpg.load_image("example.png")

    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width, height, data, tag="texture_tag")

    dpg.add_image("texture_tag",width=490, height=350)


with dpg.window(tag='Third Window', width=400, height=400, pos=(800,100),label='Telemetry'):
    dpg.bind_font(default_font)
    with dpg.plot(tag='Line Chart', height=380, width=400):
    # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

        # series belong to a y axis
        dpg.add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)", parent="y_axis")

with dpg.window(tag='Bottom Window', width=1200, height=400, pos=(0,500),label='Surface Operations'):
    dpg.bind_font(default_font)
    dpg.add_listbox(items=["Start Up", "Calibration", "Pathing", "Excavation", "Deposition"], width=200, num_items=6)








dpg.create_viewport(title='Rover Dashboard', width=1200, height=800)
dpg.setup_dearpygui()
dpg.show_font_manager()
dpg.show_viewport()


# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    # print("this will run every frame")

    dpg.render_dearpygui_frame()

dpg.destroy_context()
