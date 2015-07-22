# Import all of the modules we need
import RPi.GPIO as GPIO # For Raspberry Pi GPIO pins
from subprocess import Popen, PIPE # To be able to call a shell script
import time # So we can pause with sleep()

led_pin = 29 # Choose a digital i/o pin
buzzer_pin = 15 # Choose a pin with PWM
pause_length = 2 # How frequently should the script check for guests (seconds)

# Setup the board and pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT) # LED pin
GPIO.setup(buzzer_pin, GPIO.OUT) # Piezo pin
buzzer = GPIO.PWM(buzzer_pin, 100) # Setting the buzzer to use the PWM

# Some basic musical notes for play a tune when someone logs in (440 A)
c = 261.63
d = 294.66
e = 329.63
f = 349.23
g = 392.00
a = 440.00
b = 493.88
C = 523.25
r = 1 # rest (musical pause)

# Current status of whether someone is logged in over SSH
# Defaults to False
current_status = False;

# Start of the logic
try:
    # while True will run indefinitely, unless interrupted by an error or keyboard using ctrl+c
    while True:

        # Run the Linux command 'who' to display current users
        p = Popen(['who'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        # We could probably use some error checking at this point, but this is just a simple script for fun
        # and we're only using a basic command that isn't likely to issue an error.
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")

        # Checks for an open parenthesis, because remote users will have their client computer name in parenthesis
        # Real sophisticated (sarcasm), I know, but it's working so far.
        if "(" in output:

            if current_status == False:
                # If the current status was previously off, or False, we'll turn on the LED...
                GPIO.output(led_pin, True)
                # ... And start making some noise with the piezo.
                GPIO.output(buzzer_pin, True)
                buzzer.start(100)
                buzzer.ChangeDutyCycle(90)
                buzzer.ChangeFrequency(c) # playing a low C
                time.sleep(0.25) # for 1/4 second
                buzzer.ChangeFrequency(e) # playing an E
                time.sleep(0.25) # for 1/4 second
                buzzer.ChangeFrequency(g) # playing a G
                time.sleep(0.25) # for 1/4 second
                buzzer.ChangeFrequency(C) # playing a high C
                time.sleep(0.5) # for 1/2 second
                buzzer.stop() # And... done.

                # Making sure to change the new current status to True
                current_status = True
        else:
            if current_status == True:
                # Turn off the LED if it was previously on
                GPIO.output(led_pin, False)
                # And mark the new current status
                current_status = False

        # Wait a certain amount of seconds and check again
        time.sleep(pause_length)

# Gracefully exit the program if interrupted by keyboard (ctrl+c)
except KeyboardInterrupt:
    print "Interrupted :("

# Cleans up the GPIO at the end of the script (keyboard interruption in this case)
finally:
    GPIO.cleanup()
