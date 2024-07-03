import os
import customtkinter as ctk
from tkinter import PhotoImage, Tk

# Initialize the main window
root = Tk()
root.title("Custom Tkinter Example")
root.geometry("800x600")  # Set the window size
root.configure(bg='black')  # Set the background color to black

# Set customtkinter theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (default), "green", "dark-blue"

# Function to handle search button click
def search_for_movie():
    print("Search button clicked")

# Search bar and button frame
search_frame = ctk.CTkFrame(master=root, bg_color='black')
search_frame.pack(pady=10, padx=10, fill='x')

# Search entry
search_entry = ctk.CTkEntry(master=search_frame, width=400, placeholder_text="Search for a movie...")
search_entry.pack(side='left', padx=(0, 10))

# Search button
search_button = ctk.CTkButton(master=search_frame, text="Search", command=search_for_movie)
search_button.pack(side='left')

# Grid frame for buttons
grid_frame = ctk.CTkFrame(master=root, bg_color='black')
grid_frame.pack(pady=20, padx=10, expand=True, fill='both')

# Function to create a button with an image (optional)
def create_button_with_image(text, row, column):
    # Assuming 'mp.png' is in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, 'mp.png')

    if os.path.exists(image_path):
        image = PhotoImage(file=image_path)
    else:
        image = None

    button = ctk.CTkButton(
        master=grid_frame,
        text=text,
        image=image,
        width=200,
        height=100,
        corner_radius=8,
        fg_color='gray20',  # Button background color
        hover_color='gray30',  # Button hover color
        text_color='white'  # Button text color
    )
    button.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')

# Create 10 buttons in a grid (2 rows, 5 columns)
for i in range(2):
    for j in range(5):
        create_button_with_image(f"Button {i*5 + j + 1}", i, j)

# Configure grid weights
for i in range(2):
    grid_frame.grid_rowconfigure(i, weight=1)
for j in range(5):
    grid_frame.grid_columnconfigure(j, weight=1)

# Run the Tkinter event loop
root.mainloop()
