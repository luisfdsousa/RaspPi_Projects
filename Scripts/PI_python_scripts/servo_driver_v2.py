#!/usr/bin/env python3
########################################################################
# Filename    : Sweep.py
# Description : Servo driver v2
# Author      : Luís Sousa
# Modification: 26/03/2020
########################################################################
import RPi.GPIO as GPIO


class ServoDriver:
    MIN_ANGLE = 0  # Standard servo´s min angle (°)
    MAX_ANGLE = 180  # Standard servo´s max angle (°)
    MIN_DC = 0.5  # Standard 0° degree pulse width (ms)
    MAX_DC = 2.5  # Standard 180° degree pulse width (ms)
    NOMINAL_FREQUENCY = 50  # Servo control frequency (Hz)

    # Constructor to initiate the Servo object
    #   => pin: PWM pin number (Raspberry PI)
    #   => min_angle: Servo´s min angle in °
    #   => max_angle: Servo´s max angle in °
    #   => min_dc: Min duty cycle corresponding to min_angle
    #   => max_dc: Max duty cycle corresponding to max_angle
    #   => nominal_frequency: Nominal servo´s PWM frequency - typically 50Hz):
    def __init__(self,
                 pin,
                 min_angle=MIN_ANGLE,
                 max_angle=MAX_ANGLE,
                 min_dc=MIN_DC,
                 max_dc=MAX_DC,
                 nominal_frequency=NOMINAL_FREQUENCY):
        self.pin_number = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.min_dc = min_dc
        self.max_dc = max_dc
        self.nominal_frequency = nominal_frequency

        # Calculate transfer function: duty_cycle (per cent) = m * desired_angle (°) + b
        try:
            y_2 = self.max_dc / self.nominal_frequency
            y_1 = self.min_dc / self.nominal_frequency
        except ZeroDivisionError:
            y_2 = 0
            y_1 = 0
        x_2 = self.max_angle
        x_1 = self.min_angle

        # Calculate m and b in the linear transfer function
        try:
            self.m = (y_2 - y_1) / (x_2 - x_1)
        except ZeroDivisionError:
            self.m = 0
        self.b = y_2 - self.m * x_2
        self.current_dc = 0
        self.previous_dc = 0
        self.gpio_control = None

    # Destructor
    def __del__(self):
        print("Deactivating Servo")
        self.stop_hardware()

    # body of destructor
    # Linear transfer function (tf): duty cycle (XXX.X % ) = m * angle (°) + b
    # Calculates new servo´s duty cycle in % (XXX.X) given a desired angle of rotation
    def tf_linear_calc_new_dc(self, desired_angle):
        self.previous_dc = self.current_dc
        self.current_dc = round((self.m * desired_angle + self.b) * 100, 1)
        return self.current_dc

    # Memory dump of all object´s variables
    def get_data(self):
        print("Servo object dump:")
        print("\tPin: #" + str(self.pin_number))
        print("\tMin angle: " + str(self.min_angle))
        print("\tMax angle: " + str(self.max_angle))
        print("\tMin pulse width: " + str(self.min_dc))
        print("\tMax pulse width: " + str(self.max_dc))
        print("\tNominal frequency: " + str(self.nominal_frequency))
        print("\tCurrent duty cycle: " + str(self.current_dc))
        print("\tPrevious duty cycle: " + str(self.previous_dc))
        print("\tTransfer function: duty_cycle (per cent) = %f * desired_angle (°) + %f" % (self.m, self.b))

    # Configure PWM pin and start PWM with self.min_dc
    def start_hardware(self):
        print("Initializing servo on pin %d:" % self.pin_number)

        # Set self.pin_number to OUTPUT
        GPIO.setup(self.pin_number, GPIO.OUT)  # Set servoPin to OUTPUT mode

        # Set self.pin_number to LOW
        GPIO.output(self.pin_number, GPIO.LOW)  # Make servoPin output LOW level

        # Set Frequency
        self.gpio_control = GPIO.PWM(self.pin_number, self.nominal_frequency)

        # Start PWM with self.min_dc
        self.gpio_control.start(self.min_dc)

    # Set / change PWM
    def set_PWM_hardware(self, angle):  # make the servo rotate to specific angle, 0-180

        # Only change if there is a GPIO object instantiated
        if self.gpio_control is not None:

            # Control is angle is within limits
            if angle < self.min_angle:
                angle = self.min_angle
            elif angle > self.max_angle:
                angle = self.max_angle

            # Set new duty cycle
            self.gpio_control.ChangeDutyCycle(self.tf_linear_calc_new_dc(angle))

    # Set / change frequency
    def set_frequency_hardware(self, frequency):  # make the servo rotate to specific angle, 0-180

        # Only change if there is a GPIO object instantiated
        if self.gpio_control is not None:

            # Control is angle is within limits
            if angle > 0:

                # Change Frequency (Hz)
                self.gpio_control.ChangeFrequency(frequency)

    # Stop / Deactivate PWM / Servo
    def stop_hardware(self):
        print("Deinitializing Servo:")
        self.gpio_control.stop()

    # Test linear transfer function
    def test_tf(self):
        print("Start the linear transfer function output:")
        for angle in range(181):
            print("° = %d, duty cycle = %f per cent" % (angle, servo.tf_linear_calc_new_dc(angle)))


if __name__ == '__main__':  # Program entrance
    print('Program is starting...')
    GPIO.setmode(GPIO.BOARD)         # use PHYSICAL GPIO Numbering
    servo = ServoDriver(17)
    servo.start_hardware()
    servo.set_PWM_hardware(90)
    servo.get_data()
    servo.test_tf()
    servo.stop_hardware()
    del servo
    GPIO.cleanup()