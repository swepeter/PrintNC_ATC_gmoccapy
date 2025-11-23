#!/usr/bin/env python3

# Import necessary modules
import tkinter as tk
from tkinter import messagebox
import linuxcnc # LinuxCNC Python module
import hal # HAL Python module

# It's good practice to get references to LinuxCNC command and status objects
# The 'self' parameter in the M-code function refers to the interpreter instance.
# We'll pass it to helper functions if they need to interact with LinuxCNC.

def m150_function(self, **words):
    """
    This function is called when M150 is executed in G-code.
    It displays a Yes/No message box.
    """
    # Create a hidden Tkinter root window
    # This prevents a blank Tkinter window from appearing alongside the message box.
    root = tk.Tk()
    root.withdraw()

    # Display the message box
    # askyesno returns True for Yes, False for No
    result = messagebox.askyesno(
        "User Confirmation",
        "Tool change complete. Ready to continue?",
        parent=root # Attach to the hidden root
    )

    # Destroy the root window after the message box is closed
    root.destroy()

    # Now, you can use the 'result' to control G-code flow.
    # LinuxCNC Python interface allows setting G-code parameters.
    # Let's say you want to set parameter #5000 based on user input.
    # True (Yes) can be 1.0, False (No) can be 0.0

    if result:
        self.execute("G10 L2 P5000 1.0 (User selected YES)", 1) # Set parameter #5000 to 1.0
        # You could also use linuxcnc.command().set_parameter(5000, 1.0)
        # but self.execute directly manipulates the G-code interpreter's parameters.
        self.display("User confirmed: YES. Continuing program.")
    else:
        self.execute("G10 L2 P5000 0.0 (User selected NO)", 1) # Set parameter #5000 to 0.0
        self.display("User confirmed: NO. Program might stop or take alternative action.")
        # You might want to halt the program here if 'No' means a critical stop
        # You can signal an error or use M2/M30 through self.execute()
        # For example, to stop the program:
        # self.execute("M2", 1) # Or M30
        # self.set_errormsg("Operation cancelled by user.")

    # Return INTERP_OK to signal that the M-code executed successfully.
    # This is important for LinuxCNC to resume G-code execution.
    # from interpreter import INTERP_OK (if you need it)
    return True # Or interpreter.INTERP_OK if imported


# You can add other M-code functions here, e.g., m102_function, m103_function, etc.
# Each would be remapped in the INI file.