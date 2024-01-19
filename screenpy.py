#!/usr/bin/env python3 

import subprocess
import sys

# Check if there are any screen sessions
if not subprocess.run('ps aux | grep -iE "[s]creen -a" | grep -v color', shell=True, check=False, stdout=subprocess.PIPE).stdout:
    sys.exit("No screen sessions available - exiting script")

try:
    # List all screen sessions with pts in the name
    screen_list = subprocess.run(["screen", "-ls"], check=False, stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")

    # Print the list of screen sessions
    for i, line in enumerate(screen_list):
        if "pts" in line:
            print(f"{i + 1}: {line}")

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
                sys.exit(0)

    # If the selected screen is not found
    print("Invalid screen number selected.")

except subprocess.CalledProcessError as e:
    print(f"Error executing 'screen -ls': {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)
