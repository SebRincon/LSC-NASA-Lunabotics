import depthai as dai
import numpy as np
import cv2
#    ┌──────OAK D───────────┐
# ┌──┴──────┐           ┌───┴────┐         Pipeline
# │Left Mono│◀──────────│XLinkIn │◀───┐     ┌────┐
# │ Camera  ├────┐      └───┬────┘    ├─────│Host│
# └──┬──────┘    │      ┌───┴────┐    │     └────┘
#    │           └─────▶│XLinkOut│────│───────┐
#    │                  └───┬────┘    │       │
# ┌──┴────────┐         ┌───┴────┐    │       │
# │Right Mono │◀────────│XLinkIn │◀───┘       │
# │  Camera   ├───┐     └───┬────┘            │
# └──┬────────┘   │     ┌───┴────┐            │
#    │            └────▶│XLinkOut│───────────┐│
#    │                  └───┬────┘           ││
#    └──────────────────────┘                ││
#    ┌───────────┐            ┌───────────┐  ││
# ┌──│Right Frame│◀─getFrame──│Right Queue│◀─┘│
# │  └───────────┘            └───────────┘   │
# │  ┌───────────┐            ┌───────────┐   │
# ├──│Left Frame │◀─getFrame──│Left Queue │◀──┘
# │  └───────────┘            └───────────┘
# │  ┌─────────────────────────────────────┐
# └─▶│np.uint8(leftFrame/2 + rightFrame/2) │──┐
#    └─────────────────────────────────────┘  │
#              ┌───────────────────────────┐  │
#              │cv2.imshow("Window", imOut)│◀─┘
#              └───────────────────────────┘

def getFrame(queue):
	frame = queue.get()
	return frame.getCvFrame()

def getMonoCamera(pipeline, side:str):
	# Creating mono camera node and setting the resolution
	mono = pipeline.createMonoCamera()
	mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

	# Setting the side	
	if side.lower() == 'right':
		mono.setBoardSocket(dai.CameraBoardSocket.RIGHT)	
	else:
		mono.setBoardSocket(dai.CameraBoardSocket.LEFT)

	return mono

if __name__ == "__main__":

	foo = 1
	
	# Defineing the pipeline
	pipeline = dai.Pipeline()
	
	# Defining the monoCameras
	monoLeft  = getMonoCamera(pipeline, 'left')
	monoRight = getMonoCamera(pipeline, 'right')
	
	# Creating the xoutlinks
	xoutRight = pipeline.createXLinkOut()
	xoutRight.setStreamName("right")

	xoutLeft= pipeline.createXLinkOut()
	xoutLeft.setStreamName("left")

	# Attaching the cameras to the xoutLinks
	monoLeft.out.link(xoutLeft.input)
	monoRight.out.link(xoutRight.input)

	with dai.Device(pipeline) as device:
		# Getting output Queues and setting the queue size to 1
		leftQueue = device.getOutputQueue(name='left', maxSize=1)
		rightQueue = device.getOutputQueue(name='right',maxSize=1)
		
		# Creating a Window
		cv2.namedWindow("Stereo Pair")
		
		# SideBySide variable
		SideBySide = False
		

		while True:
			# Getting the Frames
			leftFrame = getFrame(leftQueue)
			rightFrame = getFrame(rightQueue)

			if SideBySide:
				imOut = np.hstack((leftFrame, rightFrame))
			else:
				imOut = np.uint8(leftFrame/2 + rightFrame/2)

			# Displaying the frames
			cv2.imshow("Stereo Pair", imOut)

			key = cv2.waitKey(1)

			if key == ord('q'):
				break
			elif key == ord('t'):
				SideBySide = not SideBySide
			elif key==ord('s'):
				# cv2.imwrite(f'savedImage{foo}.png', imOut)
				cv2.imwrite(f'savedImage.png', imOut)
				foo += 1
		

