import customtkinter

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, main_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_app = main_app
        self.geometry("400x300")
        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

        # Add a button to close this window and open main window
        self.button_close = customtkinter.CTkButton(self, text="Close Toplevel", command=self.close_toplevel)
        self.button_close.pack(pady=10)

    def close_toplevel(self):
        self.destroy()  # Destroy this window
        self.main_app.deiconify()  # Show the main app window

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")

        # Initialize ToplevelWindow first
        self.toplevel_window = ToplevelWindow(self)
        self.withdraw()  # Hide the main app window initially

        # Add a button to reopen ToplevelWindow
        self.button_1 = customtkinter.CTkButton(self, text="Open Toplevel", command=self.open_toplevel)
        self.button_1.pack(side="top", padx=20, pady=20)

    def open_toplevel(self):
        # Check if the window is destroyed or not
        if not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
        else:
            self.toplevel_window.deiconify()  # Show existing window if hidden

if __name__ == "__main__":
    app = App()
    app.mainloop()
