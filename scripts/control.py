#!/usr/bin/env python
import os
import numpy as np
from itertools import cycle
from math import pi

import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import String, Header


class JointHandler:
    """
    Class to keep joint related staff
    """
    def __init__(self, name, possible_poses):
        self.name = name
        tmp = list(possible_poses) + list(reversed(possible_poses))
        self.iter = cycle(tmp)

    def next(self):
        return next(self.iter)


def get_handlers(joint_names=['dof1_joint', 'dof2_joint', 'dof3_joint'], 
           ranges=[(0, pi, 1000), (-pi/2, pi/2, 500), (0, 0.5, 10)]):
    """
    Implementation of agreed in this code interface of JointHandlers provider
    """
    handlers = []
    for name, rp in zip(joint_names, ranges):
        (start, end, steps) = rp
        handlers.append(JointHandler(name, np.arange(start, end, (end-start) / steps)))
    return handlers


def talker(joint_handlers_provider):
    """
    spam joint states non-stop
    """
    if callable(joint_handlers_provider):
        handlers = joint_handlers_provider()
    else:
        handlers = joint_handlers_provider

    joint_names = [h.name for h in handlers]

    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('scara_joint_state_publisher')
    rate = rospy.Rate(10) # 10hz
    hello_str = JointState()
    hello_str.header = Header()
    while not rospy.is_shutdown():
        hello_str.header.stamp = rospy.Time.now()
        hello_str.name = joint_names
        hello_str.position = [next(h) for h in handlers]
        hello_str.velocity = []
        hello_str.effort = []
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        os.system("rosnode kill /joint_state_publisher_gui")
        os.system("rosnode kill /joint_state_publisher")
        talker(get_handlers)
        print("Well done!")
    except rospy.ROSInterruptException as e:
        print("error accured!")
        print(e)


    