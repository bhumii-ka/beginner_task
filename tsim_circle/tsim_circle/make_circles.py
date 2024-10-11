import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
import math

class threeCircles(Node):

    def __init__(self):
        super().__init__('make_circles')
        self.c_pub_=self.create_publisher(Twist, '/turtle1/cmd_vel', 1)
        self.pose_getter=self.create_subscription(Pose,'/turtle1/pose',self.pose_callback,1)
        self.pen_col_client=self.create_client(SetPen,'/turtle1/set_pen')
        self.timer=self.create_timer(0.1,self.callback)
        self.msg=Twist()
        self.msg.linear.x=2.0
        self.msg.angular.z=2.0
        self.last_angle=0
        self.no_of_cir=0
        self.col_req=SetPen.Request()
        self.col_req.width=3
        self.flag=0

    def pose_callback(self, sub_msg: Pose):
        tur_ang=sub_msg._theta #get actual angle
        if tur_ang<0:
            tur_ang=(2*math.pi)+tur_ang #to make the angle positive and between 0 to 2pi
        del_angle=tur_ang-self.last_angle #diff between last and current angle
        if del_angle<0:
            del_angle=(2*math.pi)+del_angle
        tot_angle=del_angle+self.last_angle
        self.last_angle=tur_ang
        if tot_angle>2*math.pi:
            tot_angle=0
            self.msg.linear.x+=1
            self.no_of_cir+=1
        
        if self.no_of_cir==0:
            self.col_req.r=255
            self.col_req.g=0
            self.col_req.b=0
        elif self.no_of_cir==1:
            self.col_req.r=0
            self.col_req.g=255
            self.col_req.b=0
        elif self.no_of_cir==2:
            self.col_req.r=250
            self.col_req.g=10
            self.col_req.b=255
        else:
            self.col_req.off=1
            self.flag+=1
        if (self.flag==1):
            self.get_logger().info("Pen has been set off")
        
    def callback(self):
        self.c_pub_.publish(self.msg)
        self.pen_col_client.call_async(self.col_req)
        if self.no_of_cir>=3:
            self.msg.linear.x=0.0
            self.msg.angular.z=0.0
        
def main(args=None):
    rclpy.init(args=args)
    custum_node=threeCircles()
    rclpy.spin(custum_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()