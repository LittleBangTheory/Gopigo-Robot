import easygopigo3 as easy
import socket
import time
from math import *
import math
import numpy as np
from di_sensors.easy_distance_sensor import EasyDistanceSensor



def client_request(request_type):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.10', 12345))
    if request_type == 'r':
        s.sendall(b'GBP')           #Envoie une requête pour connaitre les coordonnées du robot dans la map
        answer = s.recv(1024).decode("utf-8").split(",")
    elif request_type == 't' :
        s.sendall(b'GTP')           #Envoie une requête pour connaitre les coordonnées de la cible dans la map
        answer = s.recv(1024).decode("utf-8").split(",")
    else :
        s.sendall(b'GBS')           #Envoie une requête pour avoir l'autorisation de bouger
        answer = int.from_bytes(s.recv(1024), "big")
    if request_type == 'r' or request_type == 't':
        answer[0] = int(float(answer[0])/8.5)
        answer[1] = int(float(answer[1]))/8
    s.close()
    return answer


def orientation(my_gopigo, x_r, y_r):
    coord_t = client_request('t')
    x_t = coord_t[0]
    y_t = coord_t[1]

    coord_next = client_request('r')
    x_next = coord_next[0]
    y_next = coord_next[1]
    print(x_next)
    print(y_next)
    global angle_origin
    distance = sqrt((x_next - x_t)**2 + (y_next - y_t)**2)
    adjacent = abs(x_next - x_t)
    angle_cible = acos(adjacent/distance)*180/(math.pi)
    if((x_next-x_r)!=0):
        calcul_angle_origin = atan((abs(y_next-y_r))/(abs(x_next-x_r)))*180/(math.pi)

    if(x_next>x_r):
        if(y_next>y_r):
            angle_origin = calcul_angle_origin
        elif(y_next<y_r):
            angle_origin = -calcul_angle_origin
        else:
            angle_origin = 0
    elif(x_next<x_r):
        if(y_next>y_r):
            angle_origin = 180 - calcul_angle_origin
        elif(y_next<y_r):
            angle_origin = calcul_angle_origin - 180
        else:
            angle_origin = 180
    else:
        if(y_next>y_r):
            angle_origin = 90
        elif(y_next<y_r):
            angle_origin = -90
        else:
            print("C'est la faute de Julien\n")

    if (x_t>x_next):
        if(y_t>y_next):
            angle_mouv = angle_cible - angle_origin
        elif(y_t<y_next):
            angle_mouv = -angle_origin - angle_cible
        else:
            angle_mouv = - angle_origin
    elif(x_t==x_next):
        if(y_t>y_next):
            angle_mouv = -angle_origin + 90
        else:
            angle_mouv = -angle_origin - 90
    else:
        if(y_t>y_next):
            angle_mouv = -angle_cible-angle_origin + 180
        elif(y_t<y_next):
            angle_mouv = angle_cible - angle_origin + 180
        else:
            angle_mouv = 180 - angle_origin
    if(angle_mouv>180):
        angle_mouv = -(360 - angle_mouv)
    elif(angle_mouv<(-180)):
        angle_mouv = -(-360-(angle_mouv))
    return [angle_mouv,distance]


def main():
    my_gopigo = easy.EasyGoPiGo3()
    sensor = EasyDistanceSensor()
    my_gopigo.set_eye_color((0,0,255))
    my_gopigo.open_eyes()
    my_gopigo.set_speed(1000)
    coord_r = client_request('r')
    x_r = coord_r[0]
    y_r = coord_r[1]
    while (client_request('m') != 49):
        time.sleep(0.1)
    my_gopigo.drive_cm(20)
    compteur = 0
    while(client_request('m') != 48):
        coord_t_init = client_request('t')
        while(np.array_equal(coord_t_init, client_request('t'), equal_nan=True )):
            param = orientation(my_gopigo, x_r, y_r)
            angle_mouv =  param[0]
            distance=param[1]
            coord_r = client_request('r')
            x_r = coord_r[0]
            y_r = coord_r[1]
            my_gopigo.turn_degrees(angle_mouv)
            my_gopigo.forward()
            dist_p = 0
            while(distance - dist_p) >10:
                coord_new = client_request('r')
                x_new = coord_new[0]
                y_new = coord_new[1]
                dist_p = sqrt((x_new - x_r)**2 + (y_new - y_r)**2)
                if (sensor.read() < 50):
                    my_gopigo.stop()
                    dist_p = distance
                while(sensor.read() < 10):
                    compteur+=1
                    time.sleep(0.1)
                    if compteur == 10:
                        compteur = 0
                        my_gopigo.turn_degrees(90)
                        coord_r = client_request('r')
                        x_r = coord_r[0]
                        y_r = coord_r[1]
                        my_gopigo.drive_cm(20)
            my_gopigo.stop()
    my_gopigo.close_eyes()
main()
