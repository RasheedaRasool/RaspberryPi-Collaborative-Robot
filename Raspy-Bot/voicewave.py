
# Import standard python modules.
import sys                                                                                                                                                                                             

# Import blinka python modules.
import board
import digitalio

import Servo_control as sc

import time
import Adafruit_PCA9685



# relay = digitalio.DigitalInOut(board.D5)
# relay.direction = digitalio.Direction.OUTPUT

def homestate(pwm):

    # if dist ==1:
    print("home")
    sc.move_servo(pwm, 4, 170)
    sc.move_servo(pwm, 5, 185) #find the values here
    sc.move_servo(pwm, 6, 230)
    
    sc.move_servo(pwm, 7, 120)
    sc.move_servo(pwm, 8, 70)
    sc.move_servo(pwm, 9, 0)  


pwm = Adafruit_PCA9685.PCA9685()

print('Set frequency')
pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)


homestate(pwm)
