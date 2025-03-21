"""
File: graphical_interface_handler.py
Author: Andrew Millar-Wilson

Description:
This file contains the GUI handler class, which takes in user input on system type to simulate.
"""

#TODO: convert global vars to local ones

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



#convert below to a class

class GUI_coordinator:
    def __init__(self):
        self.selected_system_type = None
        self.requested_gravitational_system_data = None
        self.entries = []


    ##input validation functions##

    #validate input is numeric
    def validate_numeric_input(self, P):
        """Validate if input is numeric"""
        if P == "" or P == "-":
            return True
        try:
            float(P)
            return True
        except ValueError:
            return False
    #TODO: add the below functions one at a time to ensure it still works

    #check if all fields are filled
    def check_form_complete(self):
        """Check if all fields are filled"""
        try:
            for body_entries in self.entries:
                for entry in body_entries.values():
                    if entry.get() == "":
                        return False
            return True
        except Exception:
            return False
    
    #create fields based on number of bodies
    def create_fields(self):
        """Create input fields based on number of bodies"""
        try:
            n = int(n_bodies_var.get())
            if n <= 0:
                raise ValueError
            
            # Clear existing fields
            for widget in fields_frame.winfo_children():
                widget.destroy()
            self.entries.clear()
            
            # Create new fields
            for i in range(n):
                body_frame = ttk.LabelFrame(fields_frame, text=f"Body {i+1}", padding=5)
                body_frame.pack(fill="x", padx=5, pady=5)
                
                body_entries = {}
                
                # Mass field
                ttk.Label(body_frame, text="Mass:").grid(row=0, column=0, padx=5)
                mass_entry = ttk.Entry(body_frame, validate="key", 
                                    validatecommand=(numeric_validate, "%P"))
                mass_entry.grid(row=0, column=1, padx=5)
                body_entries['mass'] = mass_entry
                
                # Position fields
                pos_frame = ttk.Frame(body_frame)
                pos_frame.grid(row=1, column=0, columnspan=2, pady=5)
                
                ttk.Label(pos_frame, text="Position (X, Y):").grid(row=0, column=0, padx=5)
                pos_x_entry = ttk.Entry(pos_frame, validate="key",
                                    validatecommand=(numeric_validate, "%P"))
                pos_x_entry.grid(row=0, column=1, padx=5)
                body_entries['pos_x'] = pos_x_entry
                
                pos_y_entry = ttk.Entry(pos_frame, validate="key",
                                    validatecommand=(numeric_validate, "%P"))
                pos_y_entry.grid(row=0, column=2, padx=5)
                body_entries['pos_y'] = pos_y_entry
                
                # Velocity fields
                vel_frame = ttk.Frame(body_frame)
                vel_frame.grid(row=2, column=0, columnspan=2, pady=5)
                
                ttk.Label(vel_frame, text="Velocity (X, Y):").grid(row=0, column=0, padx=5)
                vel_x_entry = ttk.Entry(vel_frame, validate="key",
                                    validatecommand=(numeric_validate, "%P"))
                vel_x_entry.grid(row=0, column=1, padx=5)
                body_entries['vel_x'] = vel_x_entry
                
                vel_y_entry = ttk.Entry(vel_frame, validate="key",
                                    validatecommand=(numeric_validate, "%P"))
                vel_y_entry.grid(row=0, column=2, padx=5)
                body_entries['vel_y'] = vel_y_entry
                
                self.entries.append(body_entries)
            
            submit_button.pack(pady=10)
            root.bind('<KeyRelease>', lambda e: self.check_entry_completion())
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number")

    #check if all entries are completed and disable submit button if not
    def check_entry_completion(self, *args):
        """Check if all entries are completed and enable/disable submit button"""
        try:
            if self.check_form_complete():
                submit_button.config(state="normal")
            else:
                submit_button.config(state="disabled")
        except Exception:
            submit_button.config(state="disabled")

    def collect_data(self):
        """Collect data from all entry fields"""
        self.requested_gravitational_system_data = {}

        try:
            for i, body_entries in enumerate(self.entries):
                mass = float(body_entries['mass'].get())
                vel_x = float(body_entries['vel_x'].get())
                vel_y = float(body_entries['vel_y'].get())
                pos_x = float(body_entries['pos_x'].get())
                pos_y = float(body_entries['pos_y'].get())
                
                self.requested_gravitational_system_data[f"body_{i+1}"] = {
                    "mass": mass,
                    "velocity": [vel_x, vel_y],
                    "position": [pos_x, pos_y]
                }
            root.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please ensure all fields contain valid numbers")

    def initialize_system_selection(self):
        """Create initial window for system type selection"""
        selection_window = tk.Tk()
        selection_window.title("System Type Selection")
        
        def on_system_select():
            self.selected_system_type = system_type_var.get()
            selection_window.destroy()
            if self.selected_system_type == "custom":
                self.create_custom_system_window()
        
        system_type_frame = ttk.Frame(selection_window, padding=10)
        system_type_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(system_type_frame, text="Select system type:").pack(pady=5)
        system_type_var = tk.StringVar(value="custom")
        for system_type in ["binary", "random", "custom"]:
            ttk.Radiobutton(system_type_frame, 
                            text=system_type.capitalize(),
                            variable=system_type_var,
                            value=system_type).pack(pady=2)
        
        ttk.Button(system_type_frame, 
                text="Continue",
                command=on_system_select).pack(pady=10)
        
        selection_window.mainloop()
        return self.selected_system_type

    def create_custom_system_window(self):
        """Create the main window for custom system design"""
        global root, fields_frame, n_bodies_var, numeric_validate, submit_button
        
        root = tk.Tk()
        root.title("Custom System Designer")
        
        # Register validation functions
        numeric_validate = root.register(self.validate_numeric_input)
        check_form_complete_validate = root.register(self.check_form_complete)
        
        # Create frames
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(top_frame, text="Enter required number of bodies:").grid(row=0, column=0, sticky="w", padx=5)
        n_bodies_var = tk.StringVar()
        n_bodies_entry = ttk.Entry(top_frame, textvariable=n_bodies_var, width=10,
                                validate="key", validatecommand=(numeric_validate, "%P"))
        n_bodies_entry.grid(row=0, column=1, padx=5)
        
        generate_button = ttk.Button(top_frame, text="Generate bodies", command=self.create_fields)
        generate_button.grid(row=0, column=2, padx=5)
        
        # Create fields frame
        fields_frame = ttk.Frame(root, padding=10)
        fields_frame.pack(fill="both", expand=True)
        
        # Create submit button
        submit_button = ttk.Button(root, text="Get going!", command=self.collect_data, state="disabled")
        
        root.mainloop()

    def main(self):
        """Main entry point"""
        return self.initialize_system_selection()

if __name__ == "__main__":
    test_system = GUI_coordinator()
    selected_type = test_system.main()
    debug_switch = True
    if debug_switch:
        print(f"Selected system type: {selected_type}")
        if selected_type == "custom" and test_system.requested_gravitational_system_data:
            print("Requested data:", test_system.requested_gravitational_system_data)