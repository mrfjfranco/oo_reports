import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import data_processing


# Define the path for the input folder
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
input_folder = os.path.join(base_dir, 'input', 'oor')
output_folder = os.path.join(base_dir, 'output', 'oor')
print(f"Base directory: {base_dir}")
print(f"Input folder: {input_folder}")
print(f"Output folder: {output_folder}")

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


# Function to show a pop-up with the report generation result
def show_result_popup(result):
    # Create a new pop-up window
    result_popup = tk.Toplevel()
    result_popup.title("Report Generation Result")
    
    # Display the result text
    result_label = tk.Label(result_popup, text=result, padx=10, pady=10, justify="left")
    result_label.pack()

    # Button to open the output folder
    open_folder_button = tk.Button(result_popup, text="Open Reports Folder", command=open_output_folder)
    open_folder_button.pack(pady=5)

    # OK button to close the pop-up
    ok_button = tk.Button(result_popup, text="OK", command=result_popup.destroy)
    ok_button.pack(pady=10)


# Function to handle report generation for USAC
def generate_usac():
    result = ""
    if open_orders_var.get():
        result += data_processing.generate_report(data_processing.USAC, "Open Orders") + "\n"
    if bko_var.get():
        result += data_processing.generate_report(data_processing.USAC, "BKO") + "\n"
    if all_orders_var.get():
        result += data_processing.generate_report(data_processing.USAC, "All Orders") + "\n"
    
    if result.strip():
        show_result_popup(result)
    else:
        show_result_popup("USAC report generation failed.")


# Function to handle report generation for WEX
def generate_wex():
    result = ""
    if open_orders_var.get():
        result += data_processing.generate_report(data_processing.WEX, "Open Orders") + "\n"
    if bko_var.get():
        result += data_processing.generate_report(data_processing.WEX, "BKO") + "\n"
    if all_orders_var.get():
        result += data_processing.generate_report(data_processing.WEX, "All Orders") + "\n"
    
    if result.strip():
        show_result_popup(result)
    else:
        show_result_popup("WEX report generation failed.")


# Function to handle report generation for DMEC
def generate_dmec():
    result = ""
    if open_orders_var.get():
        result += data_processing.generate_report(data_processing.DMEC, "Open Orders") + "\n"
    if bko_var.get():
        result += data_processing.generate_report(data_processing.DMEC, "BKO") + "\n"
    if all_orders_var.get():
        result += data_processing.generate_report(data_processing.DMEC, "All Orders") + "\n"
    
    if result.strip():
        show_result_popup(result)
    else:
        show_result_popup("DMEC report generation failed.")


# Function to handle report generation for CLFYP
def generate_clfyp():
    result = ""
    if open_orders_var.get():
        result += data_processing.generate_report(data_processing.CLFYP, "Open Orders") + "\n"
    if bko_var.get():
        result += data_processing.generate_report(data_processing.CLFYP, "BKO") + "\n"
    if all_orders_var.get():
        result += data_processing.generate_report(data_processing.CLFYP, "All Orders") + "\n"
    
    if result.strip():
        show_result_popup(result)
    else:
        show_result_popup("CLFYP report generation failed.")


# Function to handle generation of all reports
def generate_all():
    result = ""
    if open_orders_var.get():
        result += data_processing.generate_all_reports("Open Orders") + "\n"
    if bko_var.get():
        result += data_processing.generate_all_reports("BKO") + "\n"
    if all_orders_var.get():
        result += data_processing.generate_all_reports("All Orders") + "\n"
    
    if result.strip():
        show_result_popup(result)
    else:
        show_result_popup("Report generation failed for all reports.")


# Create main GUI window
root = tk.Tk()
root.title("Open Orders Report Generator")
root.geometry("300x450+100+100")  # Adjusted window size

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


# Define the variables for each report type
open_orders_var = tk.BooleanVar(value=False)
bko_var = tk.BooleanVar(value=False)
all_orders_var = tk.BooleanVar(value=False)

# Create checkboxes to allow the user to select multiple report types
tk.Label(root, text="Select Report Type(s):").pack(pady=10)
tk.Checkbutton(root, text="Open Orders", variable=open_orders_var).pack(anchor="w", padx=30)
tk.Checkbutton(root, text="BKO", variable=bko_var).pack(anchor="w", padx=30)
tk.Checkbutton(root, text="All Orders", variable=all_orders_var).pack(anchor="w", padx=30)

# Label to describe report generation section
tk.Label(root, text="Generate reports for:").pack(pady=10)

# Create buttons for generating reports for each channel
tk.Button(root, text="USAC", command=generate_usac, width=10).pack(pady=5)
tk.Button(root, text="WEX", command=generate_wex, width=10).pack(pady=5)
tk.Button(root, text="DMEC", command=generate_dmec, width=10).pack(pady=5)
tk.Button(root, text="CLFYP", command=generate_clfyp, width=10).pack(pady=5)

# Create button for generating all reports at once
tk.Button(root, text="All", command=generate_all, width=10, fg="blue").pack(pady=15)

# Create an Exit button
tk.Button(root, text="Cancel", command=exit_program, fg="red").pack(pady=15)

# Add copyright label at the bottom
copyright_label = tk.Label(root, text="© 2024 @mr.fjfranco - All rights reserved.", font=("Arial", 8))
copyright_label.pack(side="bottom", pady=5)

# Start the Tkinter event loop
root.mainloop()
