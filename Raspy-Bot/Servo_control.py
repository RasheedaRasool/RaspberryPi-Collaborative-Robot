# ----------------------------
# LIBRARIES

# External libraries
import time
# Import the PCA9685 module.
import Adafruit_PCA9685

SERVO_MOTOR_FREQUENCY = 50 #In Hz
SERVO_MOTOR_DUTY_CYCLE_MIN = 2.5  # Min duty cycle, in %
SERVO_MOTOR_DUTY_CYCLE_MAX = 12.5  # Max duty cycle, in %
SERVO_MOTOR_ANGLE_MIN = 0  # Min angle, in degrees
SERVO_MOTOR_ANGLE_MAX = 270  # Max angle, in degrees
PWM_BOARD_RESOLUTION = 4096 # PWM control board resolution

# ----------------------------
# CODE

def convert_angle_to_pwm_board_step(angle):
    # Check that the angle is within the limits
    if (angle < SERVO_MOTOR_ANGLE_MIN) | (angle > SERVO_MOTOR_ANGLE_MAX):
        raise ValueError('The given angle ({}) is outside the limits!'.format(angle))

    # We make sure angle is treated as a float
    servo_duty_cycle = float(angle)/(SERVO_MOTOR_ANGLE_MAX-SERVO_MOTOR_ANGLE_MIN)*(SERVO_MOTOR_DUTY_CYCLE_MAX-SERVO_MOTOR_DUTY_CYCLE_MIN) + SERVO_MOTOR_DUTY_CYCLE_MIN

    # Check that the duty cycle is within the limits
    # This check is just to be sure that also the angle parameters are set correctly
    if (servo_duty_cycle < SERVO_MOTOR_DUTY_CYCLE_MIN) | (servo_duty_cycle > SERVO_MOTOR_DUTY_CYCLE_MAX):
        raise ValueError('The given servo duty cycle ({}) is outside the limits!'.format(servo_duty_cycle))

    # The step must be an integer, as the board does not accept floats
    pwm_step = int(PWM_BOARD_RESOLUTION*servo_duty_cycle/100)

    print('angle: {}'.format(angle))
    print('servo_duty_cycle: {}'.format(servo_duty_cycle))  
    print('pwm_step: {}'.format(pwm_step))

    return pwm_step

def move_servo(pwm, servo_channel, angle):
    '''
    We move the specified servo to the given angle.
    '''

    pwm_step = convert_angle_to_pwm_board_step(angle)
    # for i in range(0,pwm_step,5):
    pwm.set_pwm(servo_channel, 0, pwm_step)
    time.sleep(3)

def automatic_control(pwm, servo_channel):
    print('Move the servo with a test pattern.')
    move_servo(pwm, servo_channel, 0)
    time.sleep(3)


# if __name__ == "__main__":
    
#     print('Initialize PWM board controller')
#     # Initialise the PCA9685 using the default address (0x40).
#     pwm = Adafruit_PCA9685.PCA9685()

#     print('Set frequency')
#     # Set the frequency
#     pwm.set_pwm_freq(SERVO_MOTOR_FREQUENCY)

    # while True:
        
    #     input_data = input("What do you want to do?\n[1] Manual test\n[2] Automatic test\n[x] Exit\nAnswer: ")


    #     if input_data == '2':
    #         automatic_control(pwm, servo_channel)
    #     elif input_data.lower() == 'x':
    #         break
    #     else:
    #         print('Unrecognized input.')
    #         continue

    #     print('Done.')