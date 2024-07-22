import customtkinter
import requests
from PIL import Image, ImageTk
import io

class BookGUI(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.title("Search Book")
        self.geometry("450x320")
        self.create_widgets()

    def create_widgets(self):
        # Search bar and button
        self.search_bar = customtkinter.CTkEntry(self, placeholder_text="Enter book title")
        self.search_bar.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.search_button = customtkinter.CTkButton(self, text="Search", command=self.search_book)
        self.search_button.grid(row=0, column=1, padx=10, pady=10)

        # Placeholder image
        placeholder_img = Image.open("data/mp.png").resize((180, 240))
        self.image = customtkinter.CTkImage(placeholder_img, size=(180, 240))
        self.image_label = customtkinter.CTkLabel(self, image=self.image, text="")
        self.image_label.grid(row=1, column=0, padx=10, pady=10, rowspan=4)

        # Book details
        self.details_frame = customtkinter.CTkFrame(self, height=240, width=180)
        self.details_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.title_label = customtkinter.CTkLabel(self.details_frame, text="Title:", wraplength=235)
        self.title_label.grid(row=0, column=0, sticky="w")

        self.author_label = customtkinter.CTkLabel(self.details_frame, text="Author:", wraplength=235)
        self.author_label.grid(row=1, column=0, sticky="w")

        self.genre_label = customtkinter.CTkLabel(self.details_frame, text="Genre:", wraplength=235)
        self.genre_label.grid(row=3, column=0, sticky="w")

        self.preview_label = customtkinter.CTkLabel(self.details_frame, text="Preview:", wraplength=235)
        self.preview_label.grid(row=4, column=0, sticky="w")

        self.publisher_label = customtkinter.CTkLabel(self.details_frame, text="Publisher:", wraplength=235)
        self.publisher_label.grid(row=2, column=0, sticky="w")

        self.pages_label = customtkinter.CTkLabel(self.details_frame, text="Pages:", wraplength=235)
        self.pages_label.grid(row=6, column=0, sticky="w")


    def search_book(self):
        book_title = self.search_bar.get()
        if book_title:
            response = requests.get(f"https://openlibrary.org/search.json?title={book_title}")
            if response.status_code == 200:
                data = response.json()
                if data["docs"]:
                    book = data["docs"][0]
                    self.update_book_details(book)
                else:
                    self.update_book_details(None)
            else:
                print("Failed to fetch data from Open Library API")

    def update_book_details(self, book):
        if book:
            title = book.get("title", "N/A")
            author = ", ".join(book.get("author_name", ["N/A"]))
            genre = book.get("subject", ["N/A"])[0] if book.get("subject") else "N/A"
            preview = book.get("first_sentence", ["N/A"])[0] if book.get("first_sentence") else "N/A"
            publisher = book.get("publisher", ["N/A"])[0] if book.get("publisher") else "N/A"
            cover_id = book.get("cover_i", None)
            pages = book.get("number_of_pages_median", "No Page Count")

            self.title_label.configure(text=f"Title: {title}")
            self.author_label.configure(text=f"Author: {author}")
            self.genre_label.configure(text=f"Genre: {genre}")
            self.preview_label.configure(text=f"Preview: {preview}")
            self.publisher_label.configure(text=f"Publisher: {publisher}")
            self.pages_label.configure(text=f"Pages: {pages}")

            if cover_id:
                cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                cover_image = Image.open(io.BytesIO(requests.get(cover_url).content)).resize((180, 240))
                cover_image_tk = customtkinter.CTkImage(cover_image, size=(180, 240))
                self.image_label.configure(image=cover_image_tk)
            else:
                self.image_label.configure(image=self.image)
        else:
            self.image_label.configure(image=self.image)
            self.title_label.configure(text="Title: N/A")
            self.author_label.configure(text="Author: N/A")
            self.genre_label.configure(text="Genre: N/A")
            self.preview_label.configure(text="Preview: N/A")
            self.publisher_label.configure(text="Publisher: N/A")
            self.pages_label.configure(text="Pages: N/A")
            
