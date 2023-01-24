import easygopigo3 as easy
import socket
from math import *
import math

import time

from di_sensors.easy_inertial_measurement_unit import EasyIMUSensor


imu = EasyIMUSensor()

my_gopigo = easy.EasyGoPiGo3()
"""
imu.safe_calibrate()
print("calibré")

print("balise 1")
while follow == 'n' :
    print ("balise 2")
    print(safe_calibration_status())
    follow = input('pass ? y/n')
"""

angle = imu.safe_north_point()
print(angle)
euler = imu.safe_read_euler()
string_to_print = "Euler Heading: {:.1f}  Roll: {:.1f}  Pitch: {:.1f} ".format(euler[0], euler[1], euler[2])
print(string_to_print)
"""
my_gopigo.turn_degrees(angle)
my_gopigo.drive_cm(5)
"""
