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
                messageFeed = dpg.get_value('status')
                dpg.set_value('status', f"{self.address}:{self.port}\n{messageFeed}")
                failedConnection += 1
                time.sleep(1)
                pass



    def simpleStatus(self, message):

        # self.clientSocket.connect((self.address, self.port))
        # Send data to server
        data = "Hello Server!"
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

