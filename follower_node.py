import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class ColorFollower(Node):
    def __init__(self):
        super().__init__('color_follower')
        
        self.img_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.br = CvBridge()
        self.target_dist = 10.0
        self.kp = 0.0025
        self.last_error = 0
        self.min_stop_dist = 0.5
        
        self.lower_green = np.array([35, 100, 40])
        self.upper_green = np.array([85, 255, 255])

    def scan_callback(self, data):
        self.target_dist = data.ranges[0]

    def image_callback(self, msg):
        frame = self.br.imgmsg_to_cv2(msg, "bgr8")
        h, w, _ = frame.shape
        center_x = w // 2
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_green, self.upper_green)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        twist = Twist()

        if contours:
            cnt = max(contours, key=cv2.contourArea)
            M = cv2.moments(cnt)
            
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                error = center_x - cx
                self.last_error = error
                
                twist.angular.z = self.kp * error
                
                if abs(error) < 40:
                    if self.target_dist > self.min_stop_dist:
                        twist.linear.x = 0.2
                    else:
                        twist.linear.x = 0.0
                        self.get_logger().info("Target Reached. Stopping.")
        else:
            self.get_logger().info("Target lost. Searching...")
            twist.angular.z = 0.5 if self.last_error > 0 else -0.5

        self.cmd_pub.publish(twist)
        cv2.imshow("Robot Vision", frame)
        cv2.waitKey(1)

def main():
    rclpy.init()
    node = ColorFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
