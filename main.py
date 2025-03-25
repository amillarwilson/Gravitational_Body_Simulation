"""
File: application_orchestrator.py
Author: Andrew Millar-Wilson
Date: 21/MAR/25

Description:
This file serves as the handler which imports both the GUI and system simulator functions. 
It runs the GUI, passes the output to the system simulator, and returns the graphic.
"""


#import GUI and system simulator
import graphical_interface_handler
import system_simulator
#run GUI class

if __name__ == "__main__":
    system_configuration = graphical_interface_handler.GUI_coordinator()
    selected_type = system_configuration.main()

    debug_switch = True

    if debug_switch:
        import numpy as np
        print(f"Selected system type: {selected_type}")
        if selected_type == "custom" and system_configuration.requested_gravitational_system_data:
            print("Requested data:", system_configuration.requested_gravitational_system_data)
            print(len(system_configuration.requested_gravitational_system_data))
            for body in system_configuration.requested_gravitational_system_data:
                print("Body:", body)
                print("mass:", system_configuration.requested_gravitational_system_data[body]["mass"])
                print("postition:",np.array(system_configuration.requested_gravitational_system_data[body]["position"]))
                print("velocity:",np.array(system_configuration.requested_gravitational_system_data[body]["velocity"]))
        else:
            pass

    #pass GUI output to system simulator

    if selected_type == "binary":
        simulated_system = system_simulator.System()

    elif selected_type == "random":
        simulated_system = system_simulator.System(system_type = selected_type)

    elif selected_type == "custom":
        simulated_system = system_simulator.System(system_type = selected_type, custom_system_info_dict = system_configuration.requested_gravitational_system_data)

simulated_system.plot_system()