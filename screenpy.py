#!/usr/bin/env python3 

import subprocess

try:
    # List all screen sessions with pts in the name
    screen_list = subprocess.check_output(["screen", "-ls"]).decode("utf-8").split("\n")

    # Check if there are any screen sessions
    if not any("pts" in line for line in screen_list):
        print("No available screen sessions.")
        exit(0)

    # Print the list of screen sessions
    for i, line in enumerate(screen_list):
        if "pts" in line:
            print(f"{i+1}: {line}")

    # Get user input
    select = int(input("Choose a number for the screen session you need to view: ")) - 1

    # Iterate over screen sessions again
    for i, line in enumerate(screen_list):
        if "pts" in line:
            if i == select:
                session_id = line.split(".")[0].strip()
                print(f"Attempting to attach to {session_id}")

                # Use subprocess.run to run the screen command in script mode
                subprocess.run(["script", "-q", "-c", f"screen -d -r {session_id}", "/dev/null"])

                # Keep the script running until the user decides to exit
                input("Press Enter to exit")
                exit(0)

    # If the selected screen is not found
    print("Invalid screen number selected.")

except subprocess.CalledProcessError as e:
    print(f"Error executing 'screen -ls': {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)
