import customtkinter as customtkinter
import tkinter as tk
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

image_path = "OOR/CG Reports.jpg"

def show_root_window():
    # Close the welcome window
    welcome_window.destroy()
    
    # Show the main root window
    root.deiconify()

# Hide the main window until the welcome window vanishes
root = customtkinter.CTk()
root.withdraw()

# Create the welcome window
welcome_window = tk.Toplevel()
welcome_window.title("Welcome")
welcome_window.geometry("500x350")

# Load an image
image = Image.open(image_path)
image = image.resize((500, 350), Image.LANCZOS)  # Resize the image to fit the window
photo = ImageTk.PhotoImage(image)

# Display the image in the welcome window
label = tk.Label(welcome_window, image=photo)
label.pack()

# Schedule the welcome window to close after 3 seconds (3000 milliseconds)
welcome_window.after(3000, show_root_window)

root.title('Francisco')
root.geometry("900x500")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

def login():
    print("Test")

def exit_program():
    root.quit()

# Adjust the number of columns in the grid to allow centering
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)

frame.grid_columnconfigure(4, weight=1)
frame.grid_columnconfigure(5, weight=1)
frame.grid_columnconfigure(6, weight=1)
# frame.grid_columnconfigure(7, weight=1)

label1 = customtkinter.CTkLabel(master=frame, text="CG Reports", font=("Roboto", 24))
label1.grid(row=0, column=2, columnspan=2, pady=12, padx=10)

label2 = customtkinter.CTkLabel(master=frame, text="Select Open Orders Rerports:", font=("Roboto", 16))
label2.grid(row=1, column=1, columnspan=2, pady=12, padx=10)

checkbox_oor_usac = customtkinter.CTkCheckBox(master=frame, text="OOR USAC")
checkbox_oor_usac.grid(row=2, column=1, columnspan=2, pady=12, padx=10)

checkbox_oor_wex = customtkinter.CTkCheckBox(master=frame, text="OOR WEX")
checkbox_oor_wex.grid(row=3, column=1, columnspan=2, pady=12, padx=10)

checkbox_oor_dmec = customtkinter.CTkCheckBox(master=frame, text="OOR DMEC")
checkbox_oor_dmec.grid(row=4, column=1, columnspan=2, pady=12, padx=10)

checkbox_oor_clfy = customtkinter.CTkCheckBox(master=frame, text="OOR CLFY")
checkbox_oor_clfy.grid(row=5, column=1, columnspan=2, pady=12, padx=10)

button_gen_oor = customtkinter.CTkButton(master=frame, text="Generate", command=login)
button_gen_oor.grid(row=6, column=1, columnspan=2, pady=12, padx=10)



label3 = customtkinter.CTkLabel(master=frame, text="Select End Of Day Reports:", font=("Roboto", 16))
label3.grid(row=1, column=3, columnspan=2, pady=12, padx=10)

checkbox_eod_usac = customtkinter.CTkCheckBox(master=frame, text="EOD USAC")
checkbox_eod_usac.grid(row=2, column=3, columnspan=2, pady=12, padx=10)

checkbox_eod_wex = customtkinter.CTkCheckBox(master=frame, text="EOD WEX")
checkbox_eod_wex.grid(row=3, column=3, columnspan=2, pady=12, padx=10)

checkbox_eod_dmec = customtkinter.CTkCheckBox(master=frame, text="EOD DMEC")
checkbox_eod_dmec.grid(row=4, column=3, columnspan=2, pady=12, padx=10)

checkbox_eod_clfy = customtkinter.CTkCheckBox(master=frame, text="EOD CLFY")
checkbox_eod_clfy.grid(row=5, column=3, columnspan=2, pady=12, padx=10)

button_gen_eod = customtkinter.CTkButton(master=frame, text="Generate", command=login)
button_gen_eod.grid(row=6, column=3, columnspan=2, pady=12, padx=10)

# button4 = customtkinter.CTkButton(master=frame, text="CLFY OOR", command=login)
# button4.grid(row=4, column=1, columnspan=2, pady=12, padx=10)

# button5 = customtkinter.CTkButton(master=frame, text="Create EOD Reports", command=login)
# button5.grid(row=5, column=1, columnspan=2, pady=12, padx=10)

# button5 = customtkinter.CTkButton(master=frame, text="Send EOD Reports", command=login)
# button5.grid(row=6, column=1, columnspan=2, pady=12, padx=10)

# button6 = customtkinter.CTkButton(master=frame, text="Exit", command=exit_program)
# button6.grid(row=7, column=1, columnspan=2, pady=12, padx=10)



root.mainloop()