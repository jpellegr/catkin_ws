# catkin_ws

###M and Rae's Notes on the code:


####Turtlebot Code (catkin_ws\src\speedy_nav\scripts)

__TurtleBot.py__ Four classes: one for the _TurtleBot_ object, and then three thread classes - _MovementControlThread_, _ImageSensorThread_, and _SensorThread_. (s2 in terms of units means seconds squared, we think -- in terms of seconds of an arc or whatever)
__TurtleBot__ just initialises all the threads and provides movement/utility methods - turning, bumper status, find angle to wall, and so on. Uses __Utils__. Uses CvBridge to be able to use images from kinect with OpenCV/ROS

__Utils__ All utils has in it is _getMedianAngle()_. Other utils are in __FixedActions__, which contains methods align, to move a fixed distance away from an object; _findAdjustedTargetArea_, which adjusts the expected size of the target given information about what angle it’s at; as well as _turnToNextTarget_ and _turnByAngle_, which are self-explanatory.

__CameraOnly__ is the same as __TurtleBot.py__ but without using the turtlebot so only uses Image and Depth sensors. Accesses a camera only (hence, the name). Has _ImageSensor_, _DepthSensor_, and _TurtleBot_ classes. Has _getMedianAngle()_. _TurtleBot_ initializes other 2 classes. Then, only handles finding angle to wall. 

__Planner__ has a _Planner_ class and an assisting _UpdateCamera_ class. The latter does pretty much what you would expect it to - refreshes images, saves them if the ‘t’ key is pressed, notices if the camera is stalled. 
Planner starts up the camera, requests a destination until it gets a valid one, tand then sets up a potential field brain with various behaviors from __FieldBehaviors__.

__FieldBehaviors__ includes a bunch of methods for use by a potential field brain: _RandomWander_, _KeepMoving_, _ObstacleForce_ (represents the repulsive force from an obstacle or barrier), and _ColorInvestigate_ (which is attracted to colors that the __MultiCamShift__ is interested in).

__MultiCamShift__ is interested in colors that are placed horizontally in a pattern (_getHorzPatterns_). Uses _getPotentialMatches_ to find the expected location of an interesting object given a couple instances of the same color horizontally but not vertically displaced.


#####Some useful tutorials:
TurtleBot - http://wiki.ros.org/Robots/TurtleBot

ROS explanation- http://robohub.org/ros-101-intro-to-the-robot-operating-system/

rospy - http://wiki.ros.org/rospy_tutorials

CvBridge - http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython 



Connecting to the TurtleBot using the workstation Enterprise:

First run though the necessary things to make sure the TurtleBot is started up correctly and the laptop is on. 

Ensure the laptop is connected to the `Macalester` network, not `macalester-student`. The latter is outside the firewall and you won't be able to ssh in.

Open up a terminal on the laptop. Begin by getting the laptop's IP address with 
```
ifconfig
```
Then switch over to Enterprise and open a terminal. Run `ifconfig` again to get Enterprises's IP address and then run
```
python hostTurtlebotSetup.py
```
and enter both IPs when prompted. 

Next run 
```
source turtleros.bash
```
which should complete immediately with no output. Then you're ready to SSH into the laptop, by running
```
ssh -X macalester@<ip-address>
```
where `<ip-address>` is the address of the laptop. You will need to enter the password of the laptop, which is posted on the main board in the robot lab underneath the Robot Navigation poster. (The ssh should not take long, if it does check and make sure the laptop isn't conencted to `macalester-guest`. If it fails it'll time out after a minute or so.)

Then open a new terminal. In it, run 
```
roslaunch turtlebot_bringup minimal.launch
```
after which switch back to the first terminal and run 
```
roslaunch turtlebot_dashboard turtle_dashboard.launch
```

You should now have the create dashboard up. 
