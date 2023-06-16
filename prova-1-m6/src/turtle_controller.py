#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose 

from math import atan2

from collections import deque

class Fila(deque): # filas possuem append e popleft, sempre se retira o primeiro a entrar
    
    def append(self, __x):
        return super().append(__x)
    
    def popleft(self):
        return super().popleft()

class Pilha(deque): # pilhas possuem appendleft e popleft, sempre se retira o último a entrar
    
    def appendleft(self, __x):
        return super().appendleft(__x)
    
    def popleft(self):
        return super().popleft()

MAX_DIFF = 0.1

goals = Fila()
goals.append(Pose(x=0.0, y=0.5))
goals.append(Pose(x=0.5, y=0.0))
goals.append(Pose(x=0.0, y=0.5))
goals.append(Pose(x=0.5, y=0.0))
goals.append(Pose(x=0.0, y=1.0))
goals.append(Pose(x=1.0, y=0.0))
print(" "*8, "GOALS", " "*8)
print(goals)
# antigoals = Pilha()
# antigoals.append(Pose(x=0.0, y=1.0))
# antigoals.append(Pose(x=0.5, y=0.0))
# antigoals.append(Pose(x=0.0, y=0.5))
# antigoals.append(Pose(x=0.5, y=0.0))
# antigoals.append(Pose(x=0.0, y=0.5))
# print(" "*8, "ANTIGOALS", " "*8)
# print(antigoals)
class TurtleController(Node):
    def __init__(self, goal_queue):
        super().__init__('turtle_controller')
        self.pose = Pose(x=-40.0)
        self.setpoint = Pose(x=-40.0)
        self.goals = goal_queue # isso é uma fila
        self.antigoals = Pilha() # isso vai ser uma pilha
        self.setpoint_rel = goal_queue[0]
        self.antitrajetory = False
        
        self.publisher_ = self.create_publisher(
            msg_type=Twist,
            topic='/turtle1/cmd_vel',
            qos_profile=10)
        
        self.subscription_ = self.create_subscription(
            msg_type=Pose,
            topic='/turtle1/pose',
            callback=self.pose_callback,
            qos_profile=10
        )
        self.time = 0.02
        self.timer_ = self.create_timer(
            timer_period_sec=self.time,
            callback=self.move_turtle)
        self.counter = 0
        
    def pose_callback(self, msg):
        self.pose = Pose(x=msg.x, y=msg.y, theta=msg.theta)
        if self.setpoint.x == -40.0:
            self.setpoint.x = self.pose.x + self.setpoint_rel.x
            self.setpoint.y = self.pose.y + self.setpoint_rel.y
        
    
    def next_setpoint(self):
        if len(self.goals) == 0 and self.antitrajetory == False:
            self.goals = self.antigoals # agora goals é uma pilha, não uma fila
            self.antigoals = Pilha()
            self.antitrajetory = True
            
        print(" "*8, "GOALS", " "*8)
        print(self.goals)
        print(" "*8, "ANTIGOALS", " "*8)
        print(self.antigoals)
        
        self.antigoals.appendleft(Pose(x=-self.goals[0].x, y=-self.goals[0].y))
        
        self.setpoint.x = self.pose.x + self.goals[0].x 
        self.setpoint.y = self.pose.y + self.goals[0].y
        
        self.goals.popleft()
        
        print("Goals: ", len(self.goals))
        print("Next goal: ", self.setpoint)
        print("Antigoals: ", len(self.antigoals))
        print('\n'*2)

    def move_turtle(self):

        if self.pose.x == -40.0:
            print("Aguardando primeira posição...")
            return
                    
        inc_x = self.setpoint.x - self.pose.x
        inc_y = self.setpoint.y - self.pose.y
        angle_to_goal = atan2(inc_y,inc_x)
        
        speed = Twist()
        
        if (abs(inc_x) < MAX_DIFF and abs(inc_y) < MAX_DIFF):
            self.next_setpoint()
            
        if abs(angle_to_goal - self.pose.theta) > MAX_DIFF:
            speed.linear.x = 0.0
            speed.angular.z = 0.8 if (angle_to_goal - self.pose.theta) > 0.0 else -0.8
        else:
            speed.linear.x = 0.5
            speed.angular.z = 0.0            
          
                    
        self.publisher_.publish(speed)


def main(args=None):
    rclpy.init()
    turtle_controller = TurtleController(goals)
    
    rclpy.spin(turtle_controller)
    
    turtle_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()