import time
from motors import Robot_Movement  # Use the shared motor control

def run():
    """Basic Movement Mode Logic"""
    #print("Running Basic Movement Mode...")

    Robot_Movement(0, 0)  # Stop
    time.sleep(2)
    Robot_Movement(0.5, 0.54)  # Forward
    time.sleep(3)
    Robot_Movement(-0.5, -0.52)  # Backward
    time.sleep(3)
    Robot_Movement(0.1, 0.5)  # Turn Left
    time.sleep(3)
    Robot_Movement(0.5, 0.1)  # Turn Right
    time.sleep(3)
