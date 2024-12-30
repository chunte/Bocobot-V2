import webserver
import line_following
import light_searching
import basic_movement
import obstacle_avoidance
import remote_control
from motors import Robot_Movement  # Use the shared motor control

# Current mode (default is None, waiting for user selection)
current_mode = None

def main():
    global current_mode
    print("Starting Main Program")

    # Initialize the webserver
    webserver.init()

    while True:
        try:
            #  poll the server for incoming/outgoing requests  
            webserver.poll()
        
            # Check the selected mode from the webserver
            selected_mode = webserver.get_selected_mode()

            # If a new mode is selected, switch to it
            if selected_mode != current_mode:
                current_mode = selected_mode
                if current_mode == None:
                    print(f"Select mode")
                else:
                    print(f"Switching to {current_mode} mode")

            # Run the selected mode's loop if applicable
            if current_mode == "basic_movement":
                basic_movement.run()
            elif current_mode == "obstacle_avoidance":
                obstacle_avoidance.run()
            elif current_mode == "line_following":
                line_following.run()
            elif current_mode == "light_searching":
                light_searching.run()
            elif current_mode == "remote_control":
                remote_control.run()
            else:
                Robot_Movement(0, 0)  # Stop
                
        except Exception as e:
            print(e)
            continue

# Ensure the main function is called
if __name__ == "__main__":
    main()
