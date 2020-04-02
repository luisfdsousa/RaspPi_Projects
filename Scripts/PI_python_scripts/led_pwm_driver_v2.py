#!/usr/bin/env python3
########################################################################
# Filename    : led_driver.py
# Description : LED Control
# Version     : 2.0
# Author      : Luis Sousa
# Modification: 2020/03/24
########################################################################
import RPi.GPIO as GPIO
from enum import Enum
import time, threading, sys


# state machine states for the LED control
class LEDStateMachineStates(Enum):
    Init = 1
    OnOff = 2
    Dimming = 3
    Exit = 4


class LEDDriver:
    NOMINAL_FREQUENCY = 50  # Servo control frequency (Hz)
    DEFAULT_SLEEP_TIME = 0.005  # sleep time between duty_cycle changes in ms

    # Constructor to initiate the LED object
    #   => pin: PWM pin number (Raspberry PI)
    #   => sleep_time: Sleep time in between duty cycle changes (for dimming function)
    #   => nominal_frequency: Nominal servo´s PWM frequency - typically 50Hz):
    def __init__(self,
                 pin,
                 sleep_time=DEFAULT_SLEEP_TIME,
                 nominal_frequency=NOMINAL_FREQUENCY):
        self.pin_number = pin
        self.sleep_time = sleep_time
        self.nominal_frequency = nominal_frequency
        self.state = LEDStateMachineStates.Init
        self.previous_state = LEDStateMachineStates.Init
        self.current_dc = 0
        self.previous_dc = 0
        self.thread = None
        self.gpio_control = None

    # Destructor
    def __del__(self):
        print("Deactivating LED")
        self.start_dimming()
        self.turn_off_LED()
        self.__stop_hardware()

    def __check_state(self, desired_state):
        # Initialize HW in state Init and deinit it in all other states
        if self.state == LEDStateMachineStates.Init or self.state == LEDStateMachineStates.Exit:
            self.__start_hardware()
        else:
            self.__stop_hardware()

        # save states
        self.previous_state = self.state
        self.state = desired_state

    def turn_on_LED(self):
        print("Turn on LED: #" + str(self.pin_number))
        self.__check_state(self, LEDStateMachineStates.OnOff)
        GPIO.output(self.pin_number, GPIO.HIGH)

    def turn_off_LED(self):
        print("Turn off LED: #" + str(self.pin_number))
        GPIO.output(self.pin_number, GPIO.LOW)
        self.__check_state(self, LEDStateMachineStates.Exit)

    # Start dimming
    def start_dimming(self):
        print("Start dimming LED on pin: #" + str(self.pin_number))
        self.__check_state(self, LEDStateMachineStates.Dimming)

        # Set Frequency
        self.gpio_control = GPIO.PWM(self.pin_number, self.nominal_frequency)

        # Start PWM with self.min_dc
        self.gpio_control.start(0)

        # Set new duty cycle
        self.gpio_control.ChangeDutyCycle(0)

        # Launch thread to dim LED
        self.thread = threading.Thread(target=self.__thread_run)
        self.thread.start()

    # Stop dimming
    def stop_dimming(self):
        print("Stop dimming LED on pin: #" + str(self.pin_number))

        if self.gpio_control is not None:
            # Stop PWM
            self.gpio_control.stop()

        if self.thread is not None:
            # Signal termination
            self.thread.terminate()

            # Wait for actual termination (if needed)
            self.thread.join()

        self.__check_state(self, LEDStateMachineStates.Exit)

    # Thread run function (private.. starts with __)
    def __thread_run(self):
        print("Dimming LED #" + str(self.pin_number))
        self.current_dc = 0.0
        step = 1.0
        self.gpio_control = GPIO.PWM(self.pin_number, self.nominal_frequency)
        # self.gpio_control.ChangeFrequency(self.nominal_frequency)
        self.gpio_control.start(self.current_dc)  # Start with 0% duty-cycle
        while True:
            self.current_dc += step

            if self.current_dc > 100.0:
                step = -step
                self.current_dc = 100.0
                print('>>> Changed dimming direction: lighting down')
            elif self.current_dc < 0.0:
                step = -step
                self.current_dc = 0.0
                print('>>> Changed dimming direction: lighting up')

            # debug code
            #if 0.0 == self.current_dc % 10:
            #    print('>>> duty_cycle = %f, direction: %f' % (self.current_dc, step))

            self.gpio_control.ChangeDutyCycle(self.current_dc)  # change the duty cycle to 90%
            time.sleep(self.sleep_time)  # Wait for sleep_time

    # Configure PWM pin and start PWM with self.min_dc
    def __start_hardware(self):
        print("Initializing LED on pin %d:" % self.pin_number)

        # Set self.pin_number to OUTPUT
        GPIO.setup(self.pin_number, GPIO.OUT)  # Set servoPin to OUTPUT mode

        # Set self.pin_number to LOW
        GPIO.output(self.pin_number, GPIO.LOW)  # Make servoPin output LOW level

    # Stop / Deactivate PWM / LED
    def __stop_hardware(self):
        print("Deinitializing LED:")

        if self.gpio_control is not None:
            self.gpio_control.stop()

    # Memory dump of all object´s variables
    def get_data(self):
        print("LED object dump:")
        print("\tPin: #" + str(self.pin_number))
        print("\tSleep time: #" + str(self.sleep_time))
        print('\tNominal frequency: ' + str(self.nominal_frequency))
        print("\tLED state: " + str(self.state) + ", previous LED state: " +
              str(self.previous_state))
        print('\tCurrent duty cycle: ' + str(self.current_dc))
        print('\tPrevious duty cycle: ' + str(self.previous_dc))


# Example on how to use script arguments
def evaluate_script_arguments():
    # Print total number of arguments
    num_args = len(sys.argv)
    if num_args > 1:
        print('Number of arguments: %d, args list:' %num_args)
        print(sys.argv[1:])

        if num_args > 4:
            print('Error - too many arguments: pinNumber(int) pwmFrequency(int) sleepInterval(float)')
        else:

            if num_args == 4:
                try:
                    default_sleep = float(sys.argv[3])
                    print('Sleep interval set to %f seconds' % default_sleep)
                except ValueError:
                    print('Error setting the sleep interval: argument is not a float')

            if num_args >= 3:
                if str(sys.argv[2]).isnumeric():
                    init_frequency = int(sys.argv[2])
                    print('PWM frequency set to %dHz' % init_frequency)
                else:
                    print('Error setting the PWM frequency: argument is not an int')

            if num_args >= 2:
                if sys.argv[1].isnumeric():
                    led_pin = int(sys.argv[1])
                    print('Pin number #%d selected' % led_pin)
                else:
                    print('Error setting the pin number: argument is not an integer')


if __name__ == '__main__':  # Program entrance
    print('Program is starting...')

    try:
        GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
        led = LEDDriver(17)
        led.turn_on_LED()
        time.sleep(2.0)
        led.turn_off_LED()
        time.sleep(2.0)
        led.start_dimming()
        time.sleep(10.0)
        led.stop_dimming()
        led.get_data()
        del led
        GPIO.cleanup()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        del led
        GPIO.cleanup()