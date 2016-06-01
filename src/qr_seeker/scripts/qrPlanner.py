#!/usr/bin/env python

import turtleQR
import cv2
from datetime import datetime
from collections import deque
from cv_bridge import CvBridge, CvBridgeError
import rospy
import time
import threading
from geometry_msgs.msg import Twist
import zbar
from PIL import Image


class UpdateCamera( threading.Thread ):

	def __init__(self, bot):
		threading.Thread.__init__(self)
		self.lock = threading.Lock()
		self.runFlag = True
		self.robot = bot
		self.frameAverageStallThreshold = 20

	def scanImage(self, image):
		scanner = zbar.ImageScanner()
		print(scanner)
		scanner.parse_config('enable')
		bwImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		pil_im = Image.fromarray(bwImg)
		pic2 = pil_im.convert("L")
		wid, hgt = pic2.size
		raw = pic2.tobytes()

		img = zbar.Image(wid, hgt, 'Y800', raw)
		result = scanner.scan(img)

		if result == 0:
			print "Scan failed"
		else:
			for symbol in img:
				pass
			del(img)
			data = symbol.data.decode(u'utf-8')
			print "Data found:", data

	def run(self):
		time.sleep(.5)
		runFlag = True
		cv2.namedWindow("TurtleCam", 1)
		timesImageServed = 1
		while(runFlag):

			image, timesImageServed = self.robot.getImage()

			with self.lock:
				if timesImageServed > 20:
					if self.stalled == False:
						print "Camera Stalled!"
					self.stalled = True
				else:
					self.stalled = False
			
			cv2.imshow("TurtleCam", image)
			self.scanImage(image)

			code = chr(cv2.waitKey(50) & 255)

			if code == 't':
				cv2.imwrite("/home/macalester/catkin_ws/src/speedy_nav/res/captures/cap-" 
					+ str(datetime.now()) + ".jpg", image)
				print "Image saved!"
			if code == 'q':
				break

			with self.lock:
				runFlag = self.runFlag

	def isStalled(self):
		"""Returns the status of the camera stream"""
		with self.lock:
			stalled = self.stalled
		return stalled

	def haltRun(self):
		with self.lock:
			self.runFlag = False

class Planner(object):

	def __init__(self):
		self.robot = turtleQR.TurtleBot()

		image, times = self.robot.getImage()		

		self.camera = UpdateCamera(self.robot)

	def run(self,runtime = 120):
		"""Runs the program for the duration of 'runtime'"""
		timeout = time.time()+runtime
		self.camera.start()
		timeToWaitAfterStall = 30

                print "Planner.run starting while loop"
		while time.time() < timeout and not rospy.is_shutdown():	
			pass
			#STUFF GOES IN HERE			

		self.camera.haltRun()
		self.camera.join()	

	def exit(self):
		self.camera.haltRun()
	
if __name__=="__main__":
	rospy.init_node('Planner')
	plan = Planner()
	plan.run(5000)
	rospy.on_shutdown(plan.exit)
	rospy.spin()

