import cv2
import numpy as np
import RPi.GPIO as GPIO
import sonic_arm as sa
import Adafruit_PCA9685
import Servo_control as sc

cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)
# in1 = 4
in1=20
# in2 = 17
in2 = 16

in3 = 27
in4 = 22
en1 = 19
en2 = 26
# en2 = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(en1, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
p1 = GPIO.PWM(en1, 100)
p2 = GPIO.PWM(en2, 100)
p1.start(40)
p2.start(40)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)



pwm = Adafruit_PCA9685.PCA9685()

print('Set frequency')
pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)


def stopcar():
#     if (cv2.waitKey(1) & 0xff == ord('q')) or stop==1:   # 1 is the time in ms
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

while True:
    ret, frame = cap.read()
    crop_img = frame[60:120, 0:160]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)


    dist = sa.check_dist()
    print(dist)
    if len(contours) > 0:
        if dist>26:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

            if cx >= 120:
                print("Turn Left!")
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.HIGH)

            if cx < 120 and cx > 50:
                print("On Track!")
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)

            if cx <= 50:
                print("Turn Right")
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)

        else:
            stopcar()
            print('Stopping car!!!!!!')
            sa.pickup(pwm,dist)
            sa.dropoff(pwm)
            sa.home(pwm)
            continue

    else:
            print ("I don't see the line")
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)

    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




