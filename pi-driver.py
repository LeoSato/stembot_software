import signal
import socket
import math
import RPi.GPIO as GPIO

# SIGINT Handler
def shutdown(signal, frame):

    print '\n   Stopping UDP...'
    sock.close()

    print '   Stopping PWM...'
    port.stop()
    stbd.stop()
    vert.stop()

    print '   Cleaning up...'
    GPIO.cleanup(PORT)
    GPIO.cleanup(STBD)
    GPIO.cleanup(VERT)

    print '   Exiting...'
    exit(0)

#-------#
# SETUP #
#-------#
signal.signal(signal.SIGINT, shutdown)

# UDP Constants

ADDR = ('192.168.1.4', 1337)

# PWM Constants
ZERO = 7.5
FREQ = 50

# Thruster Pin Numbers
#TODO: Update for 4 thrusters
PORT = 12
STBD = 18
VERT = 16

# PS3 Vector

x = 0
y = 0
z = 0

# UDP Setup

print '   Setting UDP mode...'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print '   Setting UDP bind...'
sock.bind(ADDR)

# PWM Setup
#TODO: Update for 4 thrusters
print '   Setting GPIO mode...'
GPIO.setmode(GPIO.BOARD)

print '   Setting GPIO pins...'
GPIO.setup(PORT, GPIO.OUT)
GPIO.setup(STBD, GPIO.OUT)
GPIO.setup(VERT, GPIO.OUT)

print '   Setting PWM frequency...'
port = GPIO.PWM(PORT, FREQ)
stbd = GPIO.PWM(STBD, FREQ)
vert = GPIO.PWM(VERT, FREQ)

print '   Setting PWM duty cycle...'
port.start(ZERO)
stbd.start(ZERO)
vert.start(ZERO)

#-----------#
# Main Loop #
#-----------#
print '   Running...'
while 1:

    # Look for PS3 input
    # If we have one, great. If not, don't do anything.
    try:
        data = sock.recv(2)
    except socket.error as (code, msg):
        pass

    # Update current thrust vector based on the input.
    if data[0] == 'x':
        x = ord(data[1]) - 127 # If we got an X, update the X.
    elif data[0] == 'y':
        y = ord(data[1]) - 127 # If we got a Y, update the Y.
    elif data[0] == 'z':
        z = ord(data[1]) - 127 # If we got a Z, you get the idea.
    else:                      # Otherwise, !?!?!?.
        print '!?!?!?'
        print data
        print '!?!?!?'

    #TODO: Find a new way to calculate the PWM for each of the 4 thrusters.
    # This code only works for the old STEMbot, which had 3 thrusters.

    # Calculate PWMs based on the input from the PS3 controller
    r = math.hypot(x, y)
    r = r if r < 127 else 127
    t = math.atan2(y, x)
    t -= math.pi / 4
    p = r * math.sin(t)
    s = r * math.cos(t)

    # Transform PWM value (us) to Duty Cycle
    #TODO: Update for 4 thrusters (equation should stay the same)
    p = .02 * p + ZERO
    s = .02 * s + ZERO
    v = .02 * z + ZERO

    # Write the new PWM to "Thrusters"
    #TODO: Update for 4 thrusters
    port.ChangeDutyCycle(p)
    stbd.ChangeDutyCycle(s)
    vert.ChangeDutyCycle(v)

    # Did it Crash?
    #TODO: Update for 4 thrusters
    print '   p: %5.2f  |  s: %5.2f  |  v: %5.2f' % (p, s, v)