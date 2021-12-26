import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(tag="Primary Window"):
    dpg.add_text("Hello, world")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

dpg.create_viewport(title='Custom Title', width=800, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.show_metrics()
#dpg.set_primary_window("Primary Window", True)
#dpg.start_dearpygui()

# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    print("this will run every frame")
    dpg.render_dearpygui_frame()

dpg.destroy_context()
