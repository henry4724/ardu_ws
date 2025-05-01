import rclpy
from rclpy.node import Node
import numpy as np

from sensor_msgs.msg import LaserScan


def blind_spot_adder(scan_msg):
    left_pole_start = 140 * np.pi / 180 
    left_pole_end = 146 * np.pi / 180    
    right_pole_start = -146 * np.pi / 180 
    right_pole_end = -140 * np.pi / 180   

    filtered_scan = LaserScan()
    filtered_scan.header = scan_msg.header
    filtered_scan.angle_min = scan_msg.angle_min
    filtered_scan.angle_max = scan_msg.angle_max
    filtered_scan.angle_increment = scan_msg.angle_increment
    filtered_scan.time_increment = scan_msg.time_increment
    filtered_scan.scan_time = scan_msg.scan_time
    filtered_scan.range_min = scan_msg.range_min
    filtered_scan.range_max = scan_msg.range_max

    ranges = list(scan_msg.ranges)
    intensities = list(scan_msg.intensities) if scan_msg.intensities else []

    angles = [scan_msg.angle_min + i * scan_msg.angle_increment for i in range(len(ranges))]

    for i, angle in enumerate(angles):
            # angle = -π, π
            angle = angle % (2 * np.pi)
            if angle > np.pi:
                angle -= 2 * np.pi

            if (left_pole_start <= angle <= left_pole_end) or (right_pole_start <= angle <= right_pole_end):
                ranges[i] = float('inf')
                if intensities:
                    intensities[i] = 0.0
        
    filtered_scan.ranges = ranges
    filtered_scan.intensities = intensities if intensities else []
    return(filtered_scan)



class LidarIgnore(Node):
    def __init__(self):
        super().__init__('lidar_ignore')
        self.scan_sub = self.create_subscription(
            LaserScan,
            'raw_scan',
            self.scan_callback,
            10)
        self.scan_sub  
        self.scan_pub = self.create_publisher(
            LaserScan,
            'scan',
            10)

    def scan_callback(self, msg):
        self.scan_pub.publish(blind_spot_adder(msg))


def main(args=None):
    rclpy.init(args=args)
    lidar_ignore = LidarIgnore()
    rclpy.spin(lidar_ignore)
    lidar_ignore.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()