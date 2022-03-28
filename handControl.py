import mediapipe as mp 
import cv2
import handsModule as hm 
import pyautogui as pg
import webbrowser as wb 
import screen_brightness_control as brc

# Width and height of window
wCam, hCam = 640, 480

# For Control values
ges = True

a = [8, 12, 16, 20]

# Starting Video capture
cap = cv2.VideoCapture(0)

# Setting width and height of camera feed
cap.set(3, wCam)
cap.set(4, hCam)

# Hand detector
detector = hm.handDetector()

# To Find Hand gestures and perfrom specific Action
def findGesture(lm):
	global ges 
	x = []
	if lm:
		if lm[0][1] > lm[1][1]:
			if lm[4][1] < lm[3][1]:
				x.append(1)
			else:
				x.append(0)
		else:
			if lm[4][1] > lm[3][1]:
				x.append(1)
			else:
				x.append(0)
		for i in a:
			if lm[i][2] < lm[i-2][2]:
				x.append(1)
			else:
				x.append(0)
		if sum(x) == 5 and lm[0][2] > lm[17][2]:
			if ges:
				print("Play")
				pg.press("playpause")
				ges = not ges
		# elif sum(x) == 0 and lm[0][2] > lm[17][2]:
		# 	if ges:
		# 		print("Mute")
		# 		pg.press("volumemute")
		# 		ges = not ges
		elif x == [0, 1, 0, 0, 0] and lm[0][2] > lm[17][2]:
			print("Volume Up")
			pg.press("volumeup",presses=2)
			ges = False
		elif x == [1, 1, 0, 0, 0] and lm[0][2] > lm[17][2]:
			print("Volume Down")
			pg.press("volumedown",presses=2)
			ges = False
		elif x == [0, 1, 1, 0, 0] and lm[0][2] > lm[17][2]:
			print("Scroll up")
			pg.press("up",presses=2)
			ges = False
		elif x == [1, 1, 1, 0, 0] and lm[0][2] > lm[17][2]:
			print("Scroll Down")
			pg.press("down",presses=2)
			ges = False
		elif x == [1, 0, 0, 0, 0] and lm[4][1] < lm[2][1]:
			print("Right")
			pg.press("right")
			ges = False
		elif x == [1, 0, 0, 0, 1] and lm[4][1] < lm[2][1]:
			if ges:
				print("Browser Forward")
				pg.press("browserforward")
				ges = not ges
		elif x == [1, 0, 0, 0, 1] and lm[4][1] > lm[2][1]:
			if ges:
				print("Browser Back")
				pg.press("browserback")
				ges = not ges
		elif x == [1, 0, 0, 0, 0] and lm[4][1] > lm[2][1]:
			print("Left")
			pg.press("left")
			ges = False
		elif x == [0, 1, 0, 0, 1] and lm[0][2] > lm[17][2]:
			if ges:
				print("Youtube")
				wb.open("https://www.youtube.com")
				ges = not ges
		elif x == [1, 1, 0, 0, 1] and lm[0][2] > lm[17][2]:
			if ges:
				print("Google")
				wb.open("https://www.google.com")
				ges = not ges
		elif x == [0, 1, 1, 1, 0] and lm[0][2] > lm[17][2]:
			print("Increase Brightness")
			brc.set_brightness(brc.get_brightness()[0]+5)
			ges = False
		elif x == [1, 1, 1, 1, 0] and lm[0][2] > lm[17][2]:
			print("Decrease Brightness")
			brc.set_brightness(brc.get_brightness()[0]-5)
			ges = False

	else:
		ges = True

while True:
	# Reading each frame from feed
	success, img = cap.read()

	# Finding Hands in Image
	img = detector.findHands(img)

	# Getting Hand positions frome image
	lm, bbox = detector.findPosition(img)

	# Calling findGesture()
	findGesture(lm)

	# Displaying each frame
	cv2.imshow("Hand Control", img)
	cv2.waitKey(1)