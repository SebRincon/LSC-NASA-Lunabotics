import dearpygui.dearpygui as dpg

import socket
import select
import time

class Control():

    def setup(self):
        self.address = dpg.get_value('serverAddress')
        self.port = int(dpg.get_value('serverPort'))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.address)
        print(self.port)
        messageFeed = dpg.get_value('status')
        dpg.configure_item("modal_id", show=False)

        print('socket instantiated')
            # connect the socket
        connectionSuccessful = False
        failedConnection = 0
        
        while not connectionSuccessful and failedConnection < 5:
            try:
                messageFeed = dpg.get_value('status')
                dpg.set_value('status', f"{self.address}:{self.port}\n{messageFeed}")
# Note: if execution gets here before the server starts up, this line will cause an error, hence the try-except
                self.sock.connect((self.address, self.port))
                print('socket connected')
                connectionSuccessful = True
                messageFeed = dpg.get_value('status')
                time.sleep(1)
                failedConnection += 1
                dpg.set_value('status',f"Connected to Socket\n{messageFeed}")
            except:
                pass
            # end try
            
        # end while

    def setupMotors(self,sender, app_data, user_data):
        pass

    def setVelocity(self,sender, app_data, user_data):
        socks = [self.sock]
        readySocks, _, _ = select.select(socks, [], [], 5)
        for sock in readySocks:
            messageFeed = dpg.get_value('status')
            dpg.set_value('status', f"Speed: {speed}->{user_data}\n{messageFeed}")
            # now time to send the acknowledgement
            # encode the acknowledgement text
            speed = dpg.get_value("speed")
            encodedAckText = bytes("speed", 'utf-8')
            # send the encoded acknowledgement text
            sock.sendall(encodedAckText)
            messageFeed = dpg.get_value('status')
            dpg.set_value('status', f"Motors Updated\n{messageFeed}")




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