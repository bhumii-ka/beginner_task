import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen

class teleopTurtle(Node):

    def __init__(self):
        super().__init__('teleop_turtle')
        self.tele_key=self.create_publisher(Twist, '/turtle1/cmd_vel', 1)
        self.timer=self.create_timer(0.1,self.callback)
        self.msg=Twist()
        self.speed=1.0
        self.pen_col_client=self.create_client(SetPen,'/turtle1/set_pen')
        self.col_req=SetPen.Request()
        self.col_req.width=3
        self.flag=0
        self.get_logger().info("Teleoperation is started \n Press 'q' to quit")

    def callback(self):
        key = input()
        while(key!='q'):
            if key.lower() in 'wasd':
                if key.lower()=='w':
                    self.msg.angular.z=0.0
                    self.msg.linear.x=self.speed
                elif key.lower()=='d':
                    self.msg.linear.x=0.0
                    self.msg.angular.z=self.speed
                elif key.lower()=='s':
                    self.msg.angular.z=0.0
                    self.msg.linear.x=-self.speed
                elif key.lower()=='a':
                    self.msg.linear.x=0.0
                    self.msg.angular.z=-self.speed
                self.tele_key.publish(self.msg)

            elif key in '0123456789':
                self.speed=float(key)
                self.get_logger().info("speed changed to %s" %key)

            elif key in 'rgbo':
                if key=='o':
                    self.flag=1-self.flag
                    self.col_req.off=self.flag
                if key =='r':
                    self.col_req.r=255
                    self.col_req.g=0
                    self.col_req.b=0                    
                    self.get_logger().info("colour changed to red")
                elif key=='g':
                    self.col_req.r=0
                    self.col_req.g=255
                    self.col_req.b=0
                    self.get_logger().info("colour changed to green")
                elif key=='b':
                    self.col_req.r=0
                    self.col_req.g=0
                    self.col_req.b=255
                    self.get_logger().info("colour changed to blue")
                self.pen_col_client.call_async(self.col_req)
                
            key=input()
    
def main(args=None):
    rclpy.init(args=args)
    teleop_node=teleopTurtle()
    rclpy.spin_once(teleop_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()