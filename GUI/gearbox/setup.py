import dearpygui.dearpygui as dpg
from control import Control


class Setup():
    def createSetupModal(default_font,ctr:Control):
        with dpg.window(label="Connection Setup", modal=True, show=True, id="modal_id", no_title_bar=True, pos=(50,100)):
            dpg.bind_font(default_font)
            dpg.add_text("Enter HOST & PORT")
            dpg.add_separator()
            # dpg.add_checkbox(label="Don't ask me next time")
            dpg.add_text("Address")
            with dpg.group(horizontal=True):
                dpg.add_input_text(default_value="192.168.1.100", uppercase=True, width=-1, tag='serverAddress')

            dpg.add_text("Port")
            with dpg.group(horizontal=True):
                dpg.add_input_text(default_value="10001", uppercase=True, width=-1, tag='serverPort')

            with dpg.group(horizontal=True):
                dpg.add_button(label="OK", width=75, callback=ctr.setup)
                dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item("modal_id", show=False))