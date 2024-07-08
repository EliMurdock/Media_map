import customtkinter
from PIL import Image

def search_for_movie():
    pass


def create_main_window():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    root = customtkinter.CTk()
    root.geometry("1200x600")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)


    entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Search Bar", width = 400)
    entry1.pack(pady=12, padx=10)


    button = customtkinter.CTkButton(master=frame, text="search")
    button.pack(pady=12, padx=10)

    # create placeholder image
    m_p = Image.open("data/mp.png").resize((120, 180))
    movie_placeholder = customtkinter.CTkImage(light_image=m_p, size=(120, 180))

    button = customtkinter.CTkButton(master=root,
        text='',
        command=search_for_movie,
        width=120,
        height=180,
        border_width=0,
        corner_radius=0,
        image=movie_placeholder)
    button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    root.mainloop()


if __name__ == "__main__":
    create_main_window()



