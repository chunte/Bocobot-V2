from motors import Robot_Movement  # Use the shared motor control

def handle_command(command):
    """Handle movement commands."""
    if command == "forward":
        print("Moving Forward")
        Robot_Movement(0.5, 0.53)
    elif command == "backward":
        print("Moving Backward")
        Robot_Movement(-0.5, -0.53)
    elif command == "left":
        print("Turning Left")
        Robot_Movement(0, 0.5)
    elif command == "right":
        print("Turning Right")
        Robot_Movement(0.5, 0)
    elif command == "stop":
        print("Stopping")
        Robot_Movement(0, 0)
    else:
        print("Unknown Command")

def run():
    """Run the Remote Control Mode (Optional: Periodic Tasks)."""
    # print("Running Remote Control Mode...")
    # No loop needed, just leave it for any necessary periodic tasks
