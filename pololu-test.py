import maestro
from time import sleep
servo = maestro.Controller()
servo.setAccel(0,4)      #set servo 0 acceleration to 4
servo.setTarget(0,6000)  #set servo to move to center position
while True:
	sleep(5)	
servo.close
