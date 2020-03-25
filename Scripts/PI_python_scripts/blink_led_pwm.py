#!/usr/bin/env python3
########################################################################
# Filename    : blink_led_pwm.py
# Description : PWM usage of GPIO. Dimming the LED.
# Author      : Luis Sousa
# Modification: 2020/03/24
########################################################################
import RPi.GPIO as GPIO
import time
import sys

def setup(led_pin):
    GPIO.setmode(GPIO.BOARD)                # use PHYSICAL GPIO Numbering
    GPIO.setup(led_pin, GPIO.OUT)            # set the ledPin to OUTPUT mode
    GPIO.output(led_pin, GPIO.LOW)           # make ledPin output LOW level
    print ('Activated pin #%d : Output mode' % led_pin)

def loop_linear_dimming(led_pin, init_frequency, default_sleep):
    print('Start dimming the LED attached to pin #%d' % led_pin)
    duty_cycle = 0.0
    step = 0.2
    led = GPIO.PWM(led_pin, init_frequency)
    led.start(duty_cycle)                            # Start with 0% duty-cycle
    while True:
        duty_cycle += step

        if duty_cycle > 100.0:
            step = -step
            duty_cycle = 100.0
            print('>>> Changed dimming direction: lighting down')
        elif duty_cycle < 0.0:
            step = -step
            duty_cycle = 0.0
            print('>>> Changed dimming direction: lighting up')

        if 0.0 == duty_cycle % 10:
            print('>>> duty_cycle = %f, direction: %f' % (duty_cycle, step))

        led.ChangeDutyCycle(duty_cycle)   # change the duty cycle to 90%
        time.sleep(default_sleep)           # Wait for sleep_time
    #led.ChangeFrequency(100)       # change the frequency to 100 Hz (floats also work)
    #led.stop()  # Stop PWM


def loop_exp_dimming(led_pin, init_frequency, default_sleep):
    print('Start dimming the LED attached to pin #%d' % led_pin)
    duty_cycle = 0.0
    step = 1.2
    led = GPIO.PWM(led_pin, init_frequency)
    led.start(duty_cycle)  # Start with 0% duty-cycle
    index = 0
    direction = -1
    while True:
        duty_cycle = pow(step, index)

        if duty_cycle > 100.0:
            direction = -direction
            duty_cycle = 100.0
            print('>>> Changed dimming direction: lighting down')
        elif duty_cycle == 1.0:
            direction = -direction
            # duty_cycle = 0.0
            print('>>> Changed dimming direction: lighting up')

        index += direction

        # if 0.0 == index % (2):
        print('>>> duty_cycle = %f, direction: %f' % (duty_cycle, direction))

        led.ChangeDutyCycle(duty_cycle)  # change the duty cycle to 90%
        time.sleep(default_sleep)  # Wait for sleep_time
    # led.ChangeFrequency(100)       # change the frequency to 100 Hz (floats also work)
    # led.stop()  # Stop PWM

def destroy():
    GPIO.cleanup()                      # Release all GPIO

if __name__ == '__main__':    # Program entrance
    led_pin = 11             # define ledPin
    init_frequency = 1000     # 1000Hz
    default_sleep = 0.01     # sleep time between duty_cycle changes in ms

    # Print total number of arguments
    num_args = len(sys.argv)
    if num_args > 0:
        print('Number of arguments: %d, args list:' %num_args)
        print(sys.argv[1:])

        if num_args > 4:
            print('Error - too many arguments: pinNumber(int) pwmFrequency(int) sleepInterval(float)')
        else:

            if num_args == 4:
                #print('Setting up the sleep interval: arg = ' + sys.argv[3])
                try:
                    default_sleep = float(sys.argv[3])
                    print('Sleep interval set to %f seconds' % default_sleep)
                except ValueError:
                    print('Error setting the sleep interval: argument is not a float')

            if num_args >= 3:
                #print('Setting up the PWM frequency: arg = ' + sys.argv[2])
                if str(sys.argv[2]).isnumeric():
                    init_frequency = int(sys.argv[2])
                    print('PWM frequency set to %dHz' % init_frequency)
                else:
                    print('Error setting the PWM frequency: argument is not an int')

            if num_args >= 2:
                #print('Setting up the pin: arg = ' + sys.argv[1])
                if sys.argv[1].isnumeric():
                    led_pin = int(sys.argv[1])
                    print('Pin number #%d selected' % led_pin)
                else:
                    print('Error setting the pin number: argument is not an integer')

    setup(led_pin)
    try:
        loop_linear_dimming(led_pin, init_frequency, default_sleep)
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()