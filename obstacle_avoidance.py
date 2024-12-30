import time
import board
import adafruit_hcsr04
from motors import Robot_Movement  # Use the shared motor control

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP16, echo_pin=board.GP17)

def Read_Ultrasonic():
    time.sleep(0.1)
    return sonar.distance

def run():
    """Obstacle Avoidance Mode Logic"""
    #print("Running Obstacle Avoidance Mode...")
    
    try:
        distance = Read_Ultrasonic()
        #print(f"Distance: {distance:.2f} cm")
        if distance < 10:
            Robot_Movement(0.1, 0.5)  # Turn Left
            #print("Turn Left")
            time.sleep(1)
        else:
            Robot_Movement(0.5, 0.54)  # Forward
            #print("Move Forward")
    except RuntimeError as e:
        print(f"Error reading sensor: {e}")
        Robot_Movement(0, 0)  # Stop
