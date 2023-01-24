import easygopigo3 as easy
import socket
import math
import time
from di_sensors.easy_distance_sensor import EasyDistanceSensor

distance = EasyDistanceSensor()
my_gopigo = easy.EasyGoPiGo3()

dist=100

# the number of degrees each wheel needs to turn
WheelTurnDegrees = (((dist * 10) / my_gopigo.WHEEL_CIRCUMFERENCE) * 360)
# get the starting position of each motor
StartPositionLeft = my_gopigo.get_motor_encoder(my_gopigo.MOTOR_LEFT)
StartPositionRight = my_gopigo.get_motor_encoder(my_gopigo.MOTOR_RIGHT)

my_gopigo.set_motor_position(my_gopigo.MOTOR_LEFT, (StartPositionLeft + WheelTurnDegrees))
my_gopigo.set_motor_position(my_gopigo.MOTOR_RIGHT, (StartPositionRight + WheelTurnDegrees))

while my_gopigo.target_reached(StartPositionLeft + WheelTurnDegrees, StartPositionRight + WheelTurnDegrees) == False :
    print (distance.read())
    while distance.read() < 10:
        if my_gopigo.get_speed() != 0 :
            my_gopigo.set_speed(0)
        elif distance.read() >= 10 :
            my_gopigo.set_speed(400)
        #time.sleep(0.1)
drive_cm(dist)
while my_gopigo.get_speed() > 1 :
    while distance.read() < 10 :
        dist = 
        my_gopigo.stop()

#while True :
#    if distance.read() > 5 :
#        my_gopigo.forward()
#    else :
#        my_gopigo.stop()"""
