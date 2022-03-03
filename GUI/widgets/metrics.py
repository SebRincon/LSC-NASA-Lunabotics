import dearpygui.dearpygui as dpg


class Metrics():
    def createMetrics(default_font):
        with dpg.child_window(tag="Top Window",width=-1, height=70, pos=(0,0)):
            dpg.bind_font(default_font)
            with dpg.group(horizontal=True):
                dpg.add_progress_bar( show=True, overlay='UTC',width=200,height=30,default_value=0.5,pos=(0,30))
                dpg.add_progress_bar( show=True, overlay='Bin Capacity',width=200,height=30,default_value=0.5,pos=(230,30))
                dpg.add_progress_bar( show=True, overlay='Battery',width=200,height=30,default_value=0.5,pos=(460,30))
                dpg.add_progress_bar( show=True, overlay='Rover Temp',width=200,height=30,default_value=0.5,pos=(690,30))

                dpg.add_button(label="Open Setup", callback=lambda: dpg.configure_item("modal_id", show=True))
                dpg.add_text('Not Connected', tag='connection')