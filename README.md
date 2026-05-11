# AryanSil_PRassessment
Repo about robot navigation using ROS2 and OpenCV

This solution contains a ROS2 system that allows TurtleBot3 to visually track and follow a green sphere in a Gazebo simulation. 
The robot uses a Proportional (P) controller to center the object in its field of view and move towards it.

The features include HSV colour thresholding for detection of green objects, P-controller to determine angular velocity based on the visual error, Search and Recovery Logic for the robot to spin in the last known direction to find the target if it is lost and Centroid tracking to calculate horizontal error for steering the robot.
