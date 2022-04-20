from ctypes import addressof
import dearpygui.dearpygui as dpg

import socket
import select
import time

class Control():

    def simpleSetup(self):
        self.address = dpg.get_value('serverAddress')
        self.port = int(dpg.get_value('serverPort'))
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                connectionSuccessful = True
                messageFeed = dpg.get_value('status')
                dpg.set_value('status',f"Connected to Socket\n{messageFeed}")
                dpg.set_value('connection',"Connected")

            except:
                failedConnection += 1
                messageFeed = dpg.get_value('status')
                dpg.set_value('status', f"{self.address}:{self.port}\n{messageFeed}")
                time.sleep(1)
                # pass



    def simpleStatus(self, message):

        # self.clientSocket.connect((self.address, self.port))
        # Send data to server
        self.clientSocket.send(repr(message).encode())

        # Receive data from server
        dataFromServer = self.clientSocket.recv(1024)

        # Print to the console
        print(dataFromServer.decode())
        # self.clientSocket.close()

        return dataFromServer.decode()

    def sendVelocity(self,sender, app_data, user_data):
        messageFeed = dpg.get_value('status')
        speed = dpg.get_value("speed")
        self.clientSocket.send(repr(speed).encode())
        dataFromServer = self.clientSocket.recv(1024)

        dpg.set_value('status', f"Speed Set: {dataFromServer.decode()}\n{messageFeed}")

    def sendDirections(self,sender, app_data, user_data):
        messageFeed = dpg.get_value('status')

        self.clientSocket.send(user_data.encode())
        # dataFromServer = self.clientSocket.recv(1024)

        dpg.set_value('status', f"Direction: {user_data}\n{messageFeed}")

    def getUpdate(self):
        socks = [self.sock]
        readySocks, _, _ = select.select(socks, [], [], 5)
        for sock in readySocks:
            print('received: ' + str(message))
            # get the text via the scoket
            encodedMessage = sock.recv(1024)

            # if we didn't get anything, log an error and bail
            if not encodedMessage:
                print('error: encodedMessage was received as None')
                return None
            # end if

            # decode the received text message
            message = encodedMessage.decode('utf-8')

    def getLidarUpdates(self):
        dataFromServer = self.clientSocket.recv(1024)
        messageFeed = dpg.get_value('status')
        print('***************')
        print(dataFromServer.decode('utf-8'))
        print('***************')
        self.clientSocket.send(dataFromServer)

        dpg.set_value('status', f"{dataFromServer.decode()} \n{messageFeed[0:300]}")

class ControlGui():
    
    def createControlGUI(ctr:Control, default_font):
        
        with dpg.child_window(tag='control', width=205, height=450, pos=(0,100), label='Control'):
            dpg.bind_font(default_font)

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


                with dpg.child_window(tag='Total Power', width=200, height=50,menubar=True, no_scrollbar=True):
                    with dpg.menu_bar():
                        dpg.add_menu(label="Total Power Used", enabled=False)
                    dpg.add_text(default_value="W/h 0.0")

                with dpg.group(horizontal=True):
                    dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="FL",user_data="FL")
                    dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="Forward",user_data="F")
                    dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="FR",user_data="FR")
                with dpg.group(horizontal=True):
                    dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="Left",user_data="L")
                    dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="Stop",user_data="S")
                    dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="Right",user_data="R")
                with dpg.group(horizontal=True):
                    dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="BL",user_data="BL")
                    dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="Back",user_data="B")
                    dpg.add_button(callback=ctr.sendDirections, width=60,height=40,label="BR",user_data="BR")
            dpg.add_slider_int(label="Speed", default_value=0, max_value=30,tag="speed")
