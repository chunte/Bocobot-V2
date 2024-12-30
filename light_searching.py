import time
import board
import analogio
from motors import Robot_Movement  # Use the shared motor control

ldr = analogio.AnalogIn(board.GP27)

def run():
    """Light Searching Mode Logic"""
#    print("Running Light Searching Mode...")
    raw = ldr.value
#    print(f"Light sensor value: {raw}")
    time.sleep(0.1)

    if raw < 15000:  # Light threshold
        Robot_Movement(0.5, 0.53)  # Forward
#        print("Move Forward")
    else:
        Robot_Movement(0.1, 0.33)  # Turn Left
#        print("Turn Left")
