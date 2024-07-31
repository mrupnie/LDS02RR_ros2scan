import rclpy
from rclpy.node import Node
from rclpy.time import Time
from sensor_msgs.msg import LaserScan
import serial
import argparse
import time
import math

class LidarReader(Node):
    def __init__(self, serial_port, baud_rate):
        super().__init__('lds02rr_to_scan')
        self.publisher_ = self.create_publisher(LaserScan, '/scan', 10)
        self.serial_port = serial.Serial(serial_port, baud_rate, timeout=1)
        self.timer = self.create_timer(0.1, self.read_lidar_data)  # 10 Hz

    def read_lidar_data(self):
        if self.serial_port.in_waiting > 0:
            try:
                line = self.serial_port.readline().decode('ascii').strip()
                scan_data = self.parse_lidar_data(line)
                if scan_data:
                    # self.get_logger().info(f"Published scan data: "
                    #                    f"angle_min={scan_data.angle_min}, "
                    #                    f"angle_max={scan_data.angle_max}, "
                    #                    f"ranges={scan_data.ranges[:5]}...")
                    self.publisher_.publish(scan_data)
                else:
                    self.get_logger().error('data received: ' + line)
            except ValueError:
                self.get_logger().error('Invalid data received')

    def parse_lidar_data(self, line):
        # Example: Parse the line into LaserScan message
        # You need to implement the actual parsing based on your LIDAR's data format
        # Below is a placeholder example
        data = line.split(' ')
        # self.get_logger().info(f"Published scan data: "
        #     f"ranges={data[:5]}...")
        # self.get_logger().info("len: " f"{len(data)}")
        if len(data) < 360:
            return None
        scan = LaserScan()
        scan.header.stamp = self.get_clock().now().to_msg()
        #scan.header.stamp = Time.now()
        step_degree = 1
        scan.header.frame_id = "laser_frame"
        scan.angle_min = math.radians(1.0 * step_degree)
        scan.angle_max = math.radians(360)
        scan.angle_increment = math.radians(1.0 * step_degree)
        # domyślny RPM to 300, czyli 5 obr / s, czyli 1800st/s
        scan.range_min = 0.0
        scan.range_max = 5.0
        scan.time_increment = (1.0 / 5.0) / 360.0 * step_degree # Assuming 5Hz and 360 degrees
        scan.scan_time = 1.0 / 5.0
        # Create a list of distances where the index corresponds to the angle
        #ranges = [float('inf')] * 360  # Update size based on your LiDAR's resolution
        #index = int(angle) % 360
        #ranges[index] = distance / 1000.0  # Assuming distance in mm
        #scan.ranges = [float(r) for r in data[5:]]
        scan.ranges = [float(r)/1000 for r in data[::step_degree]] # data in mm
        scan.intensities = [100.0 for r in data[::step_degree]]  # If you have intensity data, populate it here
        return scan

def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial_port', type=str, default='/dev/ttyUSB0', help='Serial port name')
    parser.add_argument('--baud_rate', type=int, default=230400, help='Baud rate')
    args = parser.parse_args(args)

    # Convert to a list of arguments for rclpy.init
    rclpy.init(args=[f'--serial_port={args.serial_port}', f'--baud_rate={args.baud_rate}'])
    lidar_reader = LidarReader(args.serial_port, args.baud_rate)

    rclpy.spin(lidar_reader)

    lidar_reader.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

