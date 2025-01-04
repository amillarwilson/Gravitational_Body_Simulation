"""
contains the code to handle the graphical interface (TKINTER)

plan:
have multiple panels, so at the top you enter N bodies and then N boxes populate with spaces for
masses, positions, and velocities
"""

debug_switch = False

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def create_fields():
    """Generate fields for N bodies."""
    # Clear previous fields
    for widget in fields_frame.winfo_children():
        widget.destroy()

    try:
        n_bodies = int(n_bodies_var.get())
        if n_bodies <= 0:
            raise ValueError("Number of bodies must be positive.")
    except ValueError as e:
        error_label.config(text=f"Error: {e}")
        return

    error_label.config(text="")  # Clear error message

    # Create labels and entry fields for each body
    global entries
    entries = []  # Reset entries list to store new input fields
    for i in range(n_bodies):
        ttk.Label(fields_frame, text=f"Body {i+1}:").grid(row=i, column=0, sticky="w", padx=5, pady=2)

        body_entries = {}

        ttk.Label(fields_frame, text="Mass:").grid(row=i, column=1, sticky="e", padx=5)
        mass_entry = ttk.Entry(fields_frame, width=10, validate="key", validatecommand=(numeric_validate, "%P"))
        mass_entry.grid(row=i, column=2, padx=5)
        body_entries['mass'] = mass_entry

        ttk.Label(fields_frame, text="Vel X:").grid(row=i, column=3, sticky="e", padx=5)
        vel_x_entry = ttk.Entry(fields_frame, width=10, validate="key", validatecommand=(numeric_validate, "%P"))
        vel_x_entry.grid(row=i, column=4, padx=5)
        body_entries['vel_x'] = vel_x_entry

        ttk.Label(fields_frame, text="Vel Y:").grid(row=i, column=5, sticky="e", padx=5)
        vel_y_entry = ttk.Entry(fields_frame, width=10, validate="key", validatecommand=(numeric_validate, "%P"))
        vel_y_entry.grid(row=i, column=6, padx=5)
        body_entries['vel_y'] = vel_y_entry

        ttk.Label(fields_frame, text="Pos X:").grid(row=i, column=7, sticky="e", padx=5)
        pos_x_entry = ttk.Entry(fields_frame, width=10, validate="key", validatecommand=(numeric_validate, "%P"))
        pos_x_entry.grid(row=i, column=8, padx=5)
        body_entries['pos_x'] = pos_x_entry

        ttk.Label(fields_frame, text="Pos Y:").grid(row=i, column=9, sticky="e", padx=5)
        pos_y_entry = ttk.Entry(fields_frame, width=10, validate="key", validatecommand=(numeric_validate, "%P"))
        pos_y_entry.grid(row=i, column=10, padx=5)
        body_entries['pos_y'] = pos_y_entry

        entries.append(body_entries)


def collect_data():
    """Collect data from all entry fields, store it in a dictionary, and close the window."""
    global requested_gravitational_system_data
    requested_gravitational_system_data = {}

    try:
        for i, body_entries in enumerate(entries):
            mass = float(body_entries['mass'].get())
            vel_x = float(body_entries['vel_x'].get())
            vel_y = float(body_entries['vel_y'].get())
            pos_x = float(body_entries['pos_x'].get())
            pos_y = float(body_entries['pos_y'].get())

            requested_gravitational_system_data[f"Body_{i+1}"] = {
                "mass": mass,
                "velocity": {"x": vel_x, "y": vel_y},
                "position": {"x": pos_x, "y": pos_y},
            }

        if debug_switch == True:
            print("Collected Data:", requested_gravitational_system_data)  # Print collected data to console for debugging

        

        root.destroy()  # Close the window
    except ValueError:
        messagebox.showerror("Error", "Please fill in all fields with numeric values.")


def validate_numeric_input(new_value):
    """Validate that the input is a valid numeric value (including negative numbers)."""
    if new_value == "" or new_value == "-" or new_value.replace("-", "", 1).replace(".", "", 1).isdigit():
        return True
    return False


# Create main application window
root = tk.Tk()
root.title("Custom gravitational body simulation")

# Register validation function
numeric_validate = root.register(validate_numeric_input)

# Input for number of bodies
top_frame = ttk.Frame(root, padding=10)
top_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(top_frame, text="Enter required number of bodies:").grid(row=0, column=0, sticky="w", padx=5)
n_bodies_var = tk.StringVar()
n_bodies_entry = ttk.Entry(top_frame, textvariable=n_bodies_var, width=10, validate="key", validatecommand=(numeric_validate, "%P"))
n_bodies_entry.grid(row=0, column=1, padx=5)

generate_button = ttk.Button(top_frame, text="Generate bodies", command=create_fields)
generate_button.grid(row=0, column=2, padx=5)

# Error label
error_label = ttk.Label(root, text="", foreground="red")
error_label.pack(pady=5)

# Frame to hold dynamically created fields
fields_frame = ttk.Frame(root, padding=10)
fields_frame.pack(fill="both", expand=True)

# Submit button
submit_button = ttk.Button(root, text="Get going!", command=collect_data)
submit_button.pack(pady=10)

# Initialize entries list to store entry widgets
entries = []

# Run the application
root.mainloop()

print(requested_gravitational_system_data)
