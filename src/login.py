import customtkinter
import socket
import time
from database import add_user

class LoginGUI(customtkinter.CTkToplevel):
    def __init__(self, movie_app):
        super().__init__()
        self.movie_app = movie_app
        self.title("Media Map Login")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.create_login_window()

    def create_login_window(self):
        self.geometry("500x350")

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label = customtkinter.CTkLabel(master=self.frame, text="Login", font=("Roberto", 24))
        self.label.pack(pady=(30,0), padx=10)

        self.incorrect = customtkinter.CTkLabel(master=self.frame, text="",text_color='red', font=("Roberto", 12))
        self.incorrect.pack(pady=0,padx=0)

        self.entry1 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Username")
        self.entry1.pack(pady=12, padx=10)

        self.entry2 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
        self.entry2.pack(pady=12, padx=10)

        self.button = customtkinter.CTkButton(master=self.frame, text="Login", command=self.login)
        self.button.pack(pady=12, padx=10)

        self.button = customtkinter.CTkButton(master=self.frame, text="Add User", command=self.add_new_user)
        self.button.pack(pady=6, padx=10)

    def add_new_user(self):
        username = self.entry1.get()
        password = self.entry2.get()
        print(f'User added: {username}')
        add_user(username,password)


    def login(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 9999))

        username = self.entry1.get()
        password = self.entry2.get()
        
        client.send(username.encode())
        time.sleep(1)
        client.send(password.encode())

        response = client.recv(1024).decode()
        print(response)
        client.close()

        if response == "Login successful":
            self.close_login(username)
        else:
            self.incorrect.configure(text='Incorrect username/password')

    def close_login(self, username):
        self.destroy()
        self.movie_app.set_user(username)
        self.movie_app.deiconify()

if __name__ == "__main__":
    root = customtkinter.CTk()
    log = LoginGUI(root)
    root.mainloop()