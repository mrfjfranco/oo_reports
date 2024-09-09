# gui_eod_menu.py

import tkinter as tk
from tkinter import messagebox
import data_processing

# Create main GUI window
root = tk.Tk()
root.title("Report Generator")
root.geometry("300x450")  # Set a fixed window size to keep the same width

# Define the selected report type for the reports
report_type = tk.StringVar(value="Open Orders")