import customtkinter
from PIL import Image
from io import BytesIO

class MovieGUI:
    def __init__(self, root):
        self.root = root
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.create_widgets()

    def create_widgets(self):
        # Search bar and button
        self.search_bar = customtkinter.CTkEntry(master=self.root, width=400, placeholder_text="Search for a movie")
        self.search_button = customtkinter.CTkButton(master=self.root, text="Search", command=self.search_for_movie)
        self.search_bar.grid(row=0, column=0, padx=10, pady=10)
        self.search_button.grid(row=0, column=1, padx=10, pady=10)

        # Main movie details frame
        self.movie_details_frame = customtkinter.CTkFrame(master=self.root)
        self.movie_details_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        self.poster_label = customtkinter.CTkLabel(master=self.movie_details_frame)
        self.poster_label.grid(row=0, column=0, padx=10, pady=10)

        self.details_text_frame = customtkinter.CTkFrame(master=self.movie_details_frame)
        self.details_text_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.title_label = customtkinter.CTkLabel(master=self.details_text_frame, text="Title: ")
        self.title_label.grid(row=0, column=0, sticky="w")
        self.tagline_label = customtkinter.CTkLabel(master=self.details_text_frame, text="Tagline: ")
        self.tagline_label.grid(row=1, column=0, sticky="w")
        self.release_date_label = customtkinter.CTkLabel(master=self.details_text_frame, text="Release Date: ")
        self.release_date_label.grid(row=2, column=0, sticky="w")
        self.vote_average_label = customtkinter.CTkLabel(master=self.details_text_frame, text="Vote Average: ")
        self.vote_average_label.grid(row=3, column=0, sticky="w")
        self.popularity_label = customtkinter.CTkLabel(master=self.details_text_frame, text="Popularity: ")
        self.popularity_label.grid(row=4, column=0, sticky="w")
        self.runtime_label = customtkinter.CTkLabel(master=self.details_text_frame, text="Runtime: ")
        self.runtime_label.grid(row=5, column=0, sticky="w")
        self.genres_label = customtkinter.CTkLabel(master=self.details_text_frame, text="Genres: ")
        self.genres_label.grid(row=6, column=0, sticky="w")

        # Overview and other labels below the poster
        self.overview_label = customtkinter.CTkLabel(master=self.movie_details_frame, text="Overview: ")
        self.overview_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        self.production_companies_label = customtkinter.CTkLabel(master=self.movie_details_frame, text="Production Companies: ")
        self.production_companies_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        self.languages_label = customtkinter.CTkLabel(master=self.movie_details_frame, text="Languages: ")
        self.languages_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        self.keywords_label = customtkinter.CTkLabel(master=self.movie_details_frame, text="Keywords: ")
        self.keywords_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        # Recommended movies frames
        self.recommended_movies_frame = customtkinter.CTkFrame(master=self.root)
        self.recommended_movies_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        self.recommended_frames = []
        for i in range(10):
            frame = customtkinter.CTkFrame(master=self.recommended_movies_frame, height=320, width=180)
            frame.grid(row=i % 2, column=i // 2, padx=5, pady=5, sticky="n")
            frame.grid_propagate(False)

            img = Image.open("data/mp.png").resize((120, 180))
            img_tk = customtkinter.CTkImage(img, size=(120, 180))
            poster_button = customtkinter.CTkButton(master=frame, image=img_tk, text="", width=120, height=180, corner_radius=0, command=lambda i=i: self.on_poster_click(i))
            poster_button.grid(row=0, column=0, padx=25, pady=5)

            title_label = customtkinter.CTkLabel(master=frame, text="Title: ", width=120)
            title_label.grid(row=1, column=0, sticky="w")
            genres_label = customtkinter.CTkLabel(master=frame, text="Genres: ", width=120)
            genres_label.grid(row=2, column=0, sticky="w")
            vote_average_label = customtkinter.CTkLabel(master=frame, text="Vote Average: ", width=120)
            vote_average_label.grid(row=3, column=0, sticky="w")
            overview_label = customtkinter.CTkLabel(master=frame, text="Overview: ", width=100, wraplength=120)
            overview_label.grid(row=4, column=0, sticky="w")

            self.recommended_frames.append({
                "frame": frame,
                "poster": poster_button,
                "title": title_label,
                "genres": genres_label,
                "vote_average": vote_average_label,
                "overview": overview_label
            })

    def on_poster_click(self, index):
        print(f"Poster {index} clicked")

    def search_for_movie(self):
        # Dummy data for demonstration; replace with actual movie data fetching
        movie_data = {
            "poster": "data/mp.png",  # Local path or URL to movie poster image
            "title": "Example Movie",
            "tagline": "This is an example tagline.",
            "release_date": "2022-01-01",
            "vote_average": 8.5,
            "popularity": 500,
            "runtime": 120,
            "genres": "Action, Adventure",
            "overview": "This is an example overview of the movie.",
            "production_companies": "Example Production Company",
            "languages": "English",
            "keywords": "example, movie"
        }

        # Update main movie details
        self.update_movie_details(movie_data)

        # Dummy recommended movies data; replace with actual recommendations fetching
        recommended_movies = [
            {
                "poster": "data/mp.png",  # Local path or URL to recommended movie poster
                "title": f"Recommended Movie {i+1}",
                "genres": "Genre1, Genre2",
                "vote_average": 7.5 + i * 0.1,
                "overview": "This is an example overview of the recommended movie."
            }
            for i in range(10)
        ]

        # Update recommended movies
        self.update_recommended_movies(recommended_movies)

    def update_movie_details(self, movie_data):
        # Load movie poster
        poster_image = Image.open(movie_data["poster"]).resize((240, 360))
        poster = customtkinter.CTkImage(light_image=poster_image, size=(240, 360))
        self.poster_label.configure(image=poster)
        self.poster_label.image = poster

        # Update movie details text
        self.title_label.configure(text=f"Title: {movie_data['title']}")
        self.tagline_label.configure(text=f"Tagline: {movie_data['tagline']}")
        self.release_date_label.configure(text=f"Release Date: {movie_data['release_date']}")
        self.vote_average_label.configure(text=f"Vote Average: {movie_data['vote_average']}")
        self.popularity_label.configure(text=f"Popularity: {movie_data['popularity']}")
        self.runtime_label.configure(text=f"Runtime: {movie_data['runtime']} min")
        self.genres_label.configure(text=f"Genres: {movie_data['genres']}")
        self.overview_label.configure(text=f"Overview: {movie_data['overview']}")
        self.production_companies_label.configure(text=f"Production Companies: {movie_data['production_companies']}")
        self.languages_label.configure(text=f"Languages: {movie_data['languages']}")
        self.keywords_label.configure(text=f"Keywords: {movie_data['keywords']}")

    def update_recommended_movies(self, recommended_movies):
        for i, movie in enumerate(recommended_movies):
            poster_image = Image.open(movie["poster"]).resize((120, 180))
            poster = customtkinter.CTkImage(light_image=poster_image, size=(120, 180))
            self.recommended_frames[i]["poster"].configure(image=poster)
            self.recommended_frames[i]["poster"].image = poster
            self.recommended_frames[i]["title"].configure(text=f"Title: {movie['title']}")
            self.recommended_frames[i]["genres"].configure(text=f"Genres: {movie['genres']}")
            self.recommended_frames[i]["vote_average"].configure(text=f"Vote Average: {movie['vote_average']}")
            self.recommended_frames[i]["overview"].configure(text=f"Overview: {movie['overview']}")

# Initialize the main window
root = customtkinter.CTk()
app = MovieGUI(root)
app.search_for_movie()
root.mainloop()
