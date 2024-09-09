# gui_oo_menu.py

import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import data_processing

# Define the path for the input folder
input_folder = os.path.join(os.path.dirname(__file__), 'input')
output_folder = os.path.join(os.path.dirname(__file__), 'output', 'oor')

# Function to open the input folder in file explorer
def open_input_folder():
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)  # Create the folder if it doesn't exist
    # Open the folder using the default file explorer
    if os.name == 'nt':  # For Windows
        os.startfile(input_folder)
    elif os.name == 'posix':  # For macOS or Linux
        subprocess.run(['open', input_folder]) if os.uname().sysname == 'Darwin' else subprocess.run(['xdg-open', input_folder])

# Function to open the output folder in file explorer
def open_output_folder():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the folder if it doesn't exist
    # Open the folder using the default file explorer
    if os.name == 'nt':  # For Windows
        os.startfile(output_folder)
    elif os.name == 'posix':  # For macOS or Linux
        subprocess.run(['open', output_folder]) if os.uname().sysname == 'Darwin' else subprocess.run(['xdg-open', output_folder])

# Create main GUI window
root = tk.Tk()
root.title("Open Orders Report Generator")
root.geometry("300x450")  # Set a fixed window size to keep the same width

# Function to exit the program
def exit_program():
    root.destroy()

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Add "Setup" menu with "Load Data" option
setup_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=setup_menu)
setup_menu.add_command(label="View Input Folder", command=open_input_folder)
setup_menu.add_command(label="View Output Folder", command=open_output_folder)
setup_menu.add_command(label='Exit', command=exit_program)


# Define the selected report type for the reports
report_type = tk.StringVar(value="Open Orders")

# Function to handle report generation for USAC
def generate_usac():
    data_processing.generate_report(data_processing.USAC, report_type.get())
    messagebox.showinfo("Success", f"USAC {report_type.get()} report generated!")

# Function to handle report generation for WEX
def generate_wex():
    data_processing.generate_report(data_processing.WEX, report_type.get())
    messagebox.showinfo("Success", f"WEX {report_type.get()} report generated!")

# Function to handle report generation for DMEC
def generate_dmec():
    data_processing.generate_report(data_processing.DMEC, report_type.get())
    messagebox.showinfo("Success", f"DMEC {report_type.get()} report generated!")

# Function to handle report generation for CLFYP
def generate_clfyp():
    data_processing.generate_report(data_processing.CLFYP, report_type.get())
    messagebox.showinfo("Success", f"CLFYP {report_type.get()} report generated!")

# Function to handle generation of all reports
def generate_all():
    data_processing.generate_all_reports(report_type.get())
    messagebox.showinfo("Success", f"All {report_type.get()} reports generated!")



# Create radio buttons to allow the user to select the report type
tk.Label(root, text="Select Report Type:").pack(pady=10)
tk.Radiobutton(root, text="Open Orders", variable=report_type, value="Open Orders").pack(anchor="w", padx=30)
tk.Radiobutton(root, text="BKO", variable=report_type, value="BKO").pack(anchor="w", padx=30)
tk.Radiobutton(root, text="All Orders", variable=report_type, value="All Orders").pack(anchor="w", padx=30)

# Label to describe report generation section
tk.Label(root, text="Generate reports for:").pack(pady=10)

# Create buttons for generating reports for each channel
tk.Button(root, text="USAC", command=generate_usac, width=20).pack(pady=5)
tk.Button(root, text="WEX", command=generate_wex, width=20).pack(pady=5)
tk.Button(root, text="DMEC", command=generate_dmec, width=20).pack(pady=5)
tk.Button(root, text="CLFYP", command=generate_clfyp, width=20).pack(pady=5)

# Create button for generating all reports at once
tk.Button(root, text="All", command=generate_all, width=20, fg="red").pack(pady=10)

# Create an Exit button
tk.Button(root, text="Cancel", command=exit_program, width=20, fg="blue").pack(pady=15)

# Add copyright label at the bottom
copyright_label = tk.Label(root, text="© 2024 @mr.fjfranco - All rights reserved.", font=("Arial", 8))
copyright_label.pack(side="bottom", pady=5)

# Start the Tkinter event loop
root.mainloop()
