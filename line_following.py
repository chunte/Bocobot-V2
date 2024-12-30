import time
import board
import analogio
import pwmio
from motors import Robot_Movement  # Use the shared motor control

# Line Sensor

SA = analogio.AnalogIn(board.GP26)

def run():
    """Line Following Mode Logic"""

    #print("Running Line Following Mode...")
    sensor_value = (SA.value * 3.3) / 65536  # Normalize sensor reading
    #print(f"Sensor value: {sensor_value:.2f}")
    
    if 1.4 < sensor_value < 1.5:
        Robot_Movement(0.5, 0.53)  # Forward
        #print("Move Forward")
    elif 1.8 < sensor_value < 2.2:
        Robot_Movement(0.5, 0.3)  # Turn Right
        #print("Turn Right")
    elif 0.8 < sensor_value < 1.4:
        Robot_Movement(0.3, 0.53)  # Turn Left
        #print("Turn Left")
    elif 2.2 < sensor_value < 2.85:
        Robot_Movement(0.6, 0.2)  # Steep Right
        #print("Steep Right")
    elif 0.4 < sensor_value < 0.8:
        Robot_Movement(0.2, 0.63)  # Steep Left
        #print("Steep Left")
    elif 2.85 < sensor_value < 3.0:
        Robot_Movement(0.6, 0)  # Sharp Right
        #print("Sharp Right")
    elif 0.3 < sensor_value < 0.4:
        Robot_Movement(0, 0.64)  # Sharp Left
        #print("Sharp Left")
    else:
        Robot_Movement(0, 0)
        #print("No Movement")

