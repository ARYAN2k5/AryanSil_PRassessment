# AryanSil_PRassessment
Repo about robot navigation using ROS2 and OpenCV

This solution contains a ROS2 system that allows TurtleBot3 to visually track and follow a green sphere in a Gazebo simulation. 
The robot uses a Proportional (P) controller to center the object in its field of view and move towards it.

The features include - 

a) HSV colour thresholding: Detection of green objects
b) P-controller: Angular velocity commands based on the visual error
c) Search and Recovery Logic: If target is lost, the robot spins in the last known direction to find it
d) Centroid tracking: Calculates horizontal error for steering the robot
