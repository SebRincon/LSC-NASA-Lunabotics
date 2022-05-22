import dearpygui.dearpygui as dpg
from setup import Setup
from control import Control, ControlGui 
 
import socket
import select
import time
import array

# Context Boilerplate
dpg.create_context()
ctr = Control() 

# vp.pyGameDisplay()

connected = False

#Setting a Default Font & Font Size
with dpg.font_registry(show=False):
    default_font = dpg.add_font("Fonts/Roboto.ttf", 15)

#Creating the main window setting height & width to max
with dpg.window(tag="Primary Window", width=-1, height=-1):
    dpg.bind_font(default_font)

    Setup.createSetupModal(ctr=ctr,default_font=default_font)
    ControlGui.createControlGUI(ctr=ctr, default_font=default_font)
    # Terminal.CreateTerminal(default_font=default_font)


#Boilerplate GUI setup: Window size - Title
dpg.create_viewport(title='GEAR BOX CONTROL', width=300, height=500)
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window", True)
dpg.show_viewport()

# Render loop
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