
import dearpygui.dearpygui as dpg


class Viewport():
    def createViewport(default_font):
            with dpg.child_window(tag='lidarView', width=500, height=450, pos=(205,100), label='Camera Feed'):
                dpg.bind_font(default_font)
                dpg.add_image("texture_tag", pos=(100,100))