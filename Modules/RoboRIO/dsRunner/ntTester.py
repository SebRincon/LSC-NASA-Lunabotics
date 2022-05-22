from networktables import NetworkTables
import time
NetworkTables.initialize(server='169.254.55.186')


sd = NetworkTables.getTable('SmartDashboard')
_otherNumber = sd.getNumberArray('velocity', [-1,-1])
print(_otherNumber)
time.sleep(2)
sd.putNumberArray('velocity', [1,1])
otherNumber = sd.getNumberArray('velocity', [-1,-1])

print(otherNumber)