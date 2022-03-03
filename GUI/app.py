

import dearpygui.dearpygui as dpg
import controlCallbacks 
import socket
import select
import time

# Context Boilerplate
dpg.create_context()
ctr = controlCallbacks.Control() 
connected = False
texture_data = []



for i in range(0, 76800):
    texture_data.append(100 / 255)
    texture_data.append(100 / 255)
    texture_data.append(100 / 255)
    texture_data.append(255 / 255)


#Setting a Default Font & Font Size
with dpg.font_registry(show=False):
    # first argument ids the path to the .ttf or .otf file
    # default_font = dpg.add_font("Fonts/Noto.otf", 20)
    default_font = dpg.add_font("Fonts/Roboto.ttf", 15)



with dpg.texture_registry(show=False):
    dpg.add_dynamic_texture(320, 240, texture_data, tag="texture_tag")


with dpg.window(tag="Primary Window", width=-1, height=-1):
    dpg.bind_font(default_font)


    with dpg.window(label="Connection Setup", modal=True, show=True, id="modal_id", no_title_bar=True, pos=(500,200)):
        dpg.add_text("Enter HOST & PORT")
        dpg.add_separator()
        # dpg.add_checkbox(label="Don't ask me next time")
        dpg.add_text("Address")
        with dpg.group(horizontal=True):
            dpg.add_input_text(default_value="10.3.141.1", uppercase=True, width=-1, tag='serverAddress')

        dpg.add_text("Port")
        with dpg.group(horizontal=True):
            dpg.add_input_text(default_value="10001", uppercase=True, width=-1, tag='serverPort')

        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75, callback=ctr.simpleSetup)
            dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item("modal_id", show=False))

    with dpg.child_window(tag="Top Window",width=-1, height=70, pos=(0,0)):
        dpg.bind_font(default_font)
        with dpg.group(horizontal=True):
            dpg.add_progress_bar( show=True, overlay='UTC',width=200,height=30,default_value=0.5,pos=(0,30))
            dpg.add_progress_bar( show=True, overlay='Bin Capacity',width=200,height=30,default_value=0.5,pos=(230,30))
            dpg.add_progress_bar( show=True, overlay='Battery',width=200,height=30,default_value=0.5,pos=(460,30))
            dpg.add_progress_bar( show=True, overlay='Rover Temp',width=200,height=30,default_value=0.5,pos=(690,30))

            dpg.add_button(label="Open Setup", callback=lambda: dpg.configure_item("modal_id", show=True))
            dpg.add_text('Not Connected', tag='connection')


    with dpg.child_window(tag='control', width=205, height=450, pos=(0,100), label='Control'):
        with dpg.group(horizontal=False):
            with dpg.group(horizontal=True):
                dpg.add_button(width=90,height=40,label="Start")
                dpg.add_button(width=90,height=40,label="Start")
            
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

            with dpg.group(horizontal=True):
                dpg.add_button(callback=ctr.sendVelocity, width=60,height=40,label="FL",user_data="FL")
                dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="Forward",user_data="forward")
                dpg.add_button(callback=ctr.sendVelocity, width=60,height=40,label="FR",user_data="FR")
            with dpg.group(horizontal=True):
                dpg.add_button(callback=ctr.sendVelocity, width=60,height=40,label="Left",user_data="L")
                dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="Stop",user_data="stop")
                dpg.add_button(callback=ctr.sendVelocity, width=60,height=40,label="Right",user_data="R")
            with dpg.group(horizontal=True):
                dpg.add_button(callback=ctr.sendVelocity, width=60,height=40,label="BL",user_data="BL")
                dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="Back",user_data="backward")
                dpg.add_button(callback=ctr.sendVelocity, width=60,height=40,label="BR",user_data="BR")
        dpg.add_slider_int(label="Speed", default_value=0, max_value=30,tag="speed")

    with dpg.child_window(tag='lidarView', width=500, height=450, pos=(205,100), label='Camera Feed'):
        dpg.bind_font(default_font)
        dpg.add_image("texture_tag", pos=(100,100))



        # dpg.add_image("texture_tag",width=490, height=350)
    with dpg.child_window(tag='Bottom Window', width=-1, height=300, pos=(0,600),label='Surface Operations'):
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



            # with dpg.subplots(1, 2, label="Bandwidth & Power", width=-1, height=-1, row_ratios=[1.0, 1.0], column_ratios=[1.0, 1.0]) as subplot_id:

            #     with dpg.plot(no_title=True):
            #         dpg.add_plot_axis(dpg.mvXAxis, label="Kb", no_tick_labels=True)
            #         with dpg.plot_axis(dpg.mvYAxis, label="Time", no_tick_labels=True):
            #             dpg.add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)")
            #     with dpg.plot(no_title=True):
            #         dpg.add_plot_axis(dpg.mvXAxis, label="W/h", no_tick_labels=True)
            #         with dpg.plot_axis(dpg.mvYAxis, label="Time", no_tick_labels=True):
            #             dpg.add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)")






dpg.create_viewport(title='RIMOR', width=1200, height=900)
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window", True)

dpg.show_viewport()
# dpg.start_dearpygui()
while dpg.is_dearpygui_running():
    conState  = dpg.get_value('connection')
    # if conState == 'Connected':
        # ctr.getLidarUpdates()
    #     update = ctr.simpleStatus(dpg.get_value('speed'))
    #     statusFeed = dpg.get_value('status')
    #     dpg.set_value('status', f'{update}\n{statusFeed}')
    #     time.sleep(2)
    dpg.render_dearpygui_frame()

dpg.destroy_context()