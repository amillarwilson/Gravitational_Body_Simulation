"""
contains the code to handle the graphical interface (TKINTER)

plan:
have multiple panels, so at the top you enter N bodies and then N boxes populate with spaces for
masses, positions, and velocities
"""

import tkinter as tk

gravitational_system_config_window = tk.Tk()
instructions = tk.Label(text="Please enter the number of gravitational bodies you want to simulate:")
instructions.pack()
