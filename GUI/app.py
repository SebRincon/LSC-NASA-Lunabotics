import dearpygui.dearpygui as dpg
from widgets.setup import Setup
from widgets.viewport import Viewport, ViewportGUI
from widgets.metrics import Metrics
from widgets.terminal import Terminal
from widgets.control import Control, ControlGui 
import socket
import select
import time
import array

# Context Boilerplate
dpg.create_context()
ctr = Control() 
vp = Viewport()

connected = False


#Setting a Default Font & Font Size
with dpg.font_registry(show=False):
    default_font = dpg.add_font("Fonts/Roboto.ttf", 15)


#Createing blank texture for lidar
texture_data = []
for i in range(76800):
    texture_data.append(50 / 255)
    texture_data.append(50 / 255)
    texture_data.append(50 / 255)
    texture_data.append(255 / 255)

raw_data = array.array('f', texture_data)

#Setting texture into texture_registry for widget access
with dpg.texture_registry(show=False):
    dpg.add_raw_texture(320, 240, raw_data, format=dpg.mvFormat_Float_rgba, tag="texture_tag")

#Creating the main window setting height & width to max
with dpg.window(tag="Primary Window", width=-1, height=-1):
    dpg.bind_font(default_font)

    #Running setup for all the widgets 
    Setup.createSetupModal(ctr=ctr,default_font=default_font)
    Metrics.createMetrics(default_font=default_font)
    ControlGui.createControlGUI(ctr=ctr, default_font=default_font)
    ViewportGUI.createViewport(default_font=default_font, VP=vp)
    Terminal.CreateTerminal(default_font=default_font)

#Boilerplate GUI setup: Window size - Title
dpg.create_viewport(title='RIMOR', width=1200, height=900)
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