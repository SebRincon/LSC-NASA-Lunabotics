## Start Up

#
**This code is working with keyboard input as default, refer to line 104 in `dsRunner.py` for changing this.**
#

1. Connect PI to RoboRIO
2. Make sure PI & Driver station computer are on the routers WIFI
3. SSH into PI & Ping `169.254.69.69` - this is a ping to the RoboRIO
4. run **`piRunner.py`** on the RPI4 - This will handle socket bridge and pass data to networktables
5. run **`dsRunner.py`** on the Driverstation computer - This will connect to the PI's socket server and pass data 
6. **Optionally** run **`ntReader.py`** on the PI to view the networktables change live
7. ###### **`Profit`**
