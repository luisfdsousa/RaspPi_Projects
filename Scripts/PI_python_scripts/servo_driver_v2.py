#!/usr/bin/env python3
########################################################################
# Filename    : Sweep.py
# Description : Servo driver v2
# Author      : Luís Sousa
# Modification: 26/03/2020
########################################################################
import RPi.GPIO as GPIO
import time

MIN_ANGLE           = 0     # Standard servo´s min angle        (°)
MAX_ANGLE           = 180   # Standard servo´s max angle        (°)
MIN_PULSEWIDTH      = 0.5   # Standard 0° degree pulse width    (ms)
MAX_PULSEWIDTH      = 2.5   # Standard 180° degree pulse width  (ms)
NOMINAL_FREQUENCY   = 50    # Servo control frequency           (Hz)

class ServoDriver:
    def __init__(self,
                 pin,
                 min_angle = MIN_ANGLE,
                 max_angle = MAX_ANGLE,
                 min_pulsewidth = MIN_PULSEWIDTH,
                 max_pulsewidth = MAX_PULSEWIDTH,
                 nominal_frequency =NOMINAL_FREQUENCY,
                 ):
        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.min_pulsewidth = min_pulsewidth
        self.max_pulsewidth = max_pulsewidth
        self.nominal_frequency = nominal_frequency
        self.m = (1 / self.max_pulsewidth - 1 / self.min_pulsewidth) / (self.max_angle - self.min_angle)
        self.b = (1 / self.max_pulsewidth) - m * self.max_angle

    def getData(self):
        print("{0}+{1}j".format(self.real,self.imag))

def calc_linear_duty_cycle(desired_angle, min, max, m, b):
    # calculate new duty cycle based on the desired angle
    dc = m * desired_angle + b

    # If the new duty cycle is greater than its max, set it to max
    if dc > max:
        dc = max

    # If the new duty cycle is lower than its min, set it to low
    if dc < min:
        dc = min
    return dc

def setup():
    global p
    GPIO.setmode(GPIO.BOARD)         # use PHYSICAL GPIO Numbering
    GPIO.setup(servoPin, GPIO.OUT)   # Set servoPin to OUTPUT mode
    GPIO.output(servoPin, GPIO.LOW)  # Make servoPin output LOW level

    p = GPIO.PWM(servoPin, 50)     # set Frequece to 50Hz
    p.start(0)                     # Set initial Duty Cycle to 0
    
def servoWrite(angle):      # make the servo rotate to specific angle, 0-180

    m = (1/MAX_PULSEWIDTH-1/MIN_PULSEWIDTH) / (MAX_ANGLE-MIN_ANGLE)
    b = (1/MAX_PULSEWIDTH) - m * MAX_ANGLE

    
def loop():
    while True:
        time.sleep(0.5)

def destroy():
    p.stop()
    GPIO.cleanup()

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
