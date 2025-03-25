"""
File: application_orchestrator.py
Author: Andrew Millar-Wilson
Date: 21/MAR/25

Description:
This file serves as the handler which imports both the GUI and system simulator functions. 
It runs the GUI, passes the output to the system simulator, and returns the graphic.
"""


#import GUI and system simulator
from graphical_interface_handler import GUI_coordinator
import system_simulator
#run GUI class

if __name__ == "__main__":
    test_system = GUI_coordinator()
    selected_type = test_system.main()
    debug_switch = True
    if debug_switch:
        print(f"Selected system type: {selected_type}")
        if selected_type == "custom" and test_system.requested_gravitational_system_data:
            print("Requested data:", test_system.requested_gravitational_system_data)


#pass GUI output to system simulator

test_system = system_simulator.System()