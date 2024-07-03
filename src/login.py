import customtkinter
import sqlite3

#for creating db
import hashlib
import socket


def login():
    print("Test")


def create_sql_db():
    conn = sqlite3.connect("data/userdata.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL)
    """)

    username1, password1 = "deliveryman", hashlib.sha256("package1!".encode()).hexdigest()
    username2, password2 = "critic", hashlib.sha256("movie".encode()).hexdigest()

    cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username1, password1))
    cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username2, password2))

    conn.commit()

    
def create_login_window():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    root = customtkinter.CTk()
    root.geometry("500x350")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="Login", font=("Roberto", 24))
    label.pack(pady=20, padx=10)

    entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
    entry1.pack(pady=12, padx=10)

    entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
    entry2.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=frame, text="Login", command=login)
    button.pack(pady=12, padx=10)

    root.mainloop()



if __name__ == "__main__":
    create_login_window()





