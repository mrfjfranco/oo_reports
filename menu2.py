import customtkinter as customtkinter
import tkinter as tk
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


def show_root_window():
    welcome_window.destroy()
    root.deiconify()


root = customtkinter.CTk()
root.title('Francisco')
root.geometry("500x350")


# Create the welcome window
welcome_window = tk.Toplevel()
welcome_window.title("Welcome")
welcome_window.geometry("512x512")


image = Image.open("CG Reports.jpg")
image = image.resize((512, 512), Image.LANCZOS)  # Resize the image to fit the window
photo = ImageTk.PhotoImage(image)

# Display the image in the welcome window
label = tk.Label(welcome_window, image=photo)
label.pack()

# Schedule the welcome window to close after 3 seconds (3000 milliseconds)
welcome_window.after(3000, show_root_window)

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


label = customtkinter.CTkLabel(master=frame, text="Select your option:", font=("Roboto", 24))
label.grid(row=0, column=1, columnspan=2, pady=12, padx=10)

button1 = customtkinter.CTkButton(master=frame, text="T4", command=login)
button1.grid(row=1, column=1, columnspan=2, pady=12, padx=10)

button2 = customtkinter.CTkButton(master=frame, text="T5", command=login)
button2.grid(row=2, column=1, columnspan=2, pady=12, padx=10)

button3 = customtkinter.CTkButton(master=frame, text="C7", command=login)
button3.grid(row=3, column=1, columnspan=2, pady=12, padx=10)

button4 = customtkinter.CTkButton(master=frame, text="VZ", command=login)
button4.grid(row=4, column=1, columnspan=2, pady=12, padx=10)

button5 = customtkinter.CTkButton(master=frame, text="QC Check", command=login)
button5.grid(row=4, column=1, columnspan=2, pady=12, padx=10)

button5 = customtkinter.CTkButton(master=frame, text="Exit", command=exit_program)
button5.grid(row=4, column=1, columnspan=2, pady=12, padx=10)


root.mainloop()