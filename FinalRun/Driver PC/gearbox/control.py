from cProfile import label
from ctypes import addressof
import socket
from urllib import response
import dearpygui.dearpygui as dpg
 
import socket
import select
import time

class Control():

    def setup(self):
        import socket

        self.ClientSocket = socket.socket()
        address = dpg.get_value('serverAddress')
        port = int(dpg.get_value('serverPort'))
        messageFeed = dpg.get_value('status')
        connectionSuccessful = False


        print('Waiting for connection')
        try:
            self.ClientSocket.connect((address, port))
            dpg.configure_item("modal_id", show=False)
        except socket.error as e:
            print(str(e))

        Response = self.ClientSocket.recv(1024)
        while  not connectionSuccessful:
            # Input = input('Say Something: ')
            self.ClientSocket.send(str.encode('GUI'))
            Response = self.ClientSocket.recv(1024)
            print(Response)
            if Response.decode('utf-8') == 'GUI':
                print('Connected')
                connectionSuccessful = True
                
            

    def simpleSetup(self):
        self.address = dpg.get_value('serverAddress')
        self.port = int(dpg.get_value('serverPort'))
        self.ClientSocket = socket.socket()
        # self.ClientSocket.connect((self.address, self.port))
        print(self.address)
        print(self.port)
        connectionSuccessful = False
        failedConnection = 0
        messageFeed = dpg.get_value('status')
        dpg.configure_item("modal_id", show=False)
        while not connectionSuccessful and failedConnection < 5:
            try:
                # Create a client socket
                # Connect to the server
                self.clientSocket.connect((self.address, self.port))
                Response = self.clientSocket.recv(1024)
                print(response)
                connectionSuccessful = True
                # _initMessage = self.clientSocket.recv(1024)
                self.clientSocket.send("GUI")
                messageFeed = dpg.get_value('status')
                dpg.set_value('status',f"Connected to Socket\n{messageFeed}")
                dpg.set_value('connection',"Connected")

            except:

                messageFeed = dpg.get_value('status')
                dpg.set_value('status', f"{self.address}:{self.port}\n{messageFeed}")
                time.sleep(1)
                failedConnection += 1
 
    def sendMessage(self,sender, app_data, user_data):
        messageFeed = dpg.get_value('status')
        dpg.set_value('status',f"{messageFeed}\n{user_data}")

        self.ClientSocket.send(str.encode(user_data))

class ControlGui():
    
    def createControlGUI(ctr:Control, default_font):
        
        with dpg.child_window(tag='control', width=-1 , height=-1, pos=(0,0), label='Control'):
            dpg.bind_font(default_font)

            with dpg.group(horizontal=True):
                with dpg.group(horizontal=False):
                    dpg.add_text(default_value='Front')
                    dpg.add_button(callback=ctr.sendMessage, width=60,height=40,label="Forward",user_data="fr_fw")
                    dpg.add_button(callback=ctr.sendMessage, width=60,height=40,label="Stop",user_data="fr_st")
                    dpg.add_button(callback=ctr.sendMessage, width=60,height=40,label="Back",user_data="fr_bk")

                with dpg.group(horizontal=False):
                    dpg.add_text(default_value='Back')
                    dpg.add_button(callback=ctr.sendMessage, width=60,height=40,label="Forward",user_data="bk_fw")
                    dpg.add_button(callback=ctr.sendMessage, width=60,height=40,label="Stop",user_data="bk_st")
                    dpg.add_button(callback=ctr.sendMessage, width=60,height=40,label="Back",user_data="bk_bk")

                with dpg.group(horizontal=False):
                    dpg.add_text(default_value='Aux Motor')
                    dpg.add_button(callback=ctr.sendMessage, width=60,height=40,label="forward",user_data="mt_on_fw")
                    dpg.add_button(callback=ctr.sendMessage, width=60,height=40,label="backward",user_data="mt_on_bk")
                    dpg.add_button(callback=ctr.sendMessage, width=60,height=40,label="Stop",user_data="mt_off")

            with dpg.child_window(tag='Action Responses', width=-1, height=-1,menubar=True):
                with dpg.menu_bar():
                    dpg.add_menu(label="Terminal", enabled=False)
                dpg.add_text(default_value="Start up", tag='status')
