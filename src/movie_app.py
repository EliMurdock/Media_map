# package imports
import customtkinter
from PIL import Image
import requests
from io import BytesIO

#file project imports
from movie_recc import MovieRecommender
from login import LoginGUI
from database import get_last_search, update_last_search



# main application class, runs everything for the window
class MovieGUI(customtkinter.CTk):
    def __init__(self):
        #sets appearance and basic parameters for the window
        #Initializes login, starts the application hidden
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.title("Media Map")
        self.loginGUI = LoginGUI(self)
        self.withdraw()
        self.create_widgets()

    # sets the user on login and retrieves data for their last saved search
    def set_user(self, username):
        self.username = username
        self.username_label.configure(text=f"User: {username}")
        last_search = get_last_search(username)
        if last_search != None:
            self.update_movies(last_search)

    # main function for creating application, creates UI within GUI
    def create_widgets(self):
        #search bar frame
        self.search_bar_frame = customtkinter.CTkFrame(master=self, height=50, width=800)
        self.search_bar_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="n")

        # search elements (bar and search button)
        self.search_bar = customtkinter.CTkEntry(master=self.search_bar_frame, width=700, placeholder_text="Search for a movie", justify="left")
        self.search_button = customtkinter.CTkButton(master=self.search_bar_frame, text="Search", command=lambda: self.search_for_movie(self.search_bar.get()))
        self.search_bar.grid(row=0, column=0, padx=10, pady=5)
        self.search_button.grid(row=0, column=1, padx=10, pady=5)

        # username, hides in corner of window
        self.username_label = customtkinter.CTkLabel(master=self, text_color='blue', text="User:", justify='right', font=("Roberto", 18))
        self.username_label.grid(row=0, column=1, padx=10, pady=5, sticky="ne")

        # main movie details frame
        self.movie_details_frame = customtkinter.CTkFrame(master=self, height=650, width=450)
        self.movie_details_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")
        self.movie_details_frame.grid_propagate(False)

        # main movie image, creates placeholder image
        mv_img = Image.open("data/mp.png").resize((240, 360))
        mv_img_tk = customtkinter.CTkImage(mv_img, size=(240, 360))
        self.poster_label = customtkinter.CTkLabel(master=self.movie_details_frame, text="", image=mv_img_tk)
        self.poster_label.grid(row=0, column=0, padx=10, pady=10)

        # frame to the right of the main movie poster
        # holds most important details
        self.details_text_frame = customtkinter.CTkFrame(master=self.movie_details_frame)
        self.details_text_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # 
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
        self.overview_label = customtkinter.CTkLabel(master=self.movie_details_frame, text="Overview: ", wraplength=400)
        self.overview_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        self.production_companies_label = customtkinter.CTkLabel(master=self.movie_details_frame, text="Production Companies: ", wraplength=400)
        self.production_companies_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        self.languages_label = customtkinter.CTkLabel(master=self.movie_details_frame, text="Languages: ")
        self.languages_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        self.keywords_label = customtkinter.CTkLabel(master=self.movie_details_frame, text="Keywords: ", wraplength=400)
        self.keywords_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        # Recommended movies frames
        self.recommended_movies_frame = customtkinter.CTkFrame(master=self)
        self.recommended_movies_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        self.recommended_frames = []
        img = Image.open("data/mp.png").resize((120, 180))
        img_tk = customtkinter.CTkImage(img, size=(120, 180))
        for i in range(10):
            frame = customtkinter.CTkFrame(master=self.recommended_movies_frame, height=320, width=180)
            frame.grid(row=i % 2, column=i // 2, padx=5, pady=5, sticky="n")
            frame.grid_propagate(False)


            poster_button = customtkinter.CTkButton(master=frame, image=img_tk, text="", width=120, height=180, corner_radius=0, command=lambda: self.on_poster_click())
            poster_button.grid(row=0, column=0, padx=25, pady=5)

            title_label = customtkinter.CTkLabel(master=frame, text="Title: ", width=120, wraplength=180)
            title_label.grid(row=1, column=0, sticky="w")
            genres_label = customtkinter.CTkLabel(master=frame, text="Genres: ", width=120, wraplength=180)
            genres_label.grid(row=2, column=0, sticky="w")
            vote_average_label = customtkinter.CTkLabel(master=frame, text="Rating: ", width=120)
            vote_average_label.grid(row=3, column=0, sticky="w")
            overview_label = customtkinter.CTkLabel(master=frame, text="Overview: ", width=100, wraplength=180)
            overview_label.grid(row=4, column=0, sticky="w")

            self.recommended_frames.append({
                "frame": frame,
                "poster": poster_button,
                "title": title_label,
                "genres": genres_label,
                "vote_average": vote_average_label,
                "overview": overview_label
            })

    def on_poster_click(self):
        print(f"Empty poster clicked!")

    def get_poster(self, poster_path):
        poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}"
        response = requests.get(poster_url)
        response.raise_for_status()  # Check for request errors
        
        # Open the image using PIL
        image_content = BytesIO(response.content)
        return image_content


    def search_for_movie(self, movie_name):
        # get movie data from the movie reccomender
        recommender = MovieRecommender()
        movie_list = recommender.recommend_movies(movie_name)
        #saves the search in the database
        update_last_search(self.username, movie_list)
        self.update_movies(movie_list)


    def update_movies(self, movie_list):
        movie_data = movie_list[0]
        recommended_data = movie_list[1:]

        # Update main movie details
        self.update_movie_details(movie_data)

        # Update recommended movies
        self.update_recommended_movies(recommended_data)


    def update_movie_details(self, movie_data):
        # Load movie poster
        poster_image = Image.open(self.get_poster(movie_data["poster_path"])).resize((240, 360))
        poster = customtkinter.CTkImage(light_image=poster_image, size=(240, 360))
        self.poster_label.configure(image=poster)
        self.poster_label.image = poster

        # Update movie details text
        self.title_label.configure(text=f"Title: {movie_data['title']}")
        self.tagline_label.configure(text=f"Tagline: {movie_data['tagline']}")
        self.release_date_label.configure(text=f"Release Date: {movie_data['release_date']}")
        self.vote_average_label.configure(text=f"Rating: {movie_data['vote_average']}")
        self.popularity_label.configure(text=f"Popularity: {movie_data['popularity']}")
        self.runtime_label.configure(text=f"Runtime: {movie_data['runtime']} min")
        self.genres_label.configure(text=f"Genres: {movie_data['genres']}")
        self.overview_label.configure(text=f"Overview: {movie_data['overview']}")
        self.production_companies_label.configure(text=f"Production Companies: {movie_data['production_companies']}")
        self.languages_label.configure(text=f"Languages: {movie_data['spoken_languages']}")
        self.keywords_label.configure(text=f"Keywords: {movie_data['keywords']}")


    def update_recommended_movies(self, recommended_movies):
        for i, movie in enumerate(recommended_movies):
            poster_image = Image.open(self.get_poster(movie["poster_path"])).resize((120, 180))
            poster = customtkinter.CTkImage(light_image=poster_image, size=(120, 180))
            self.recommended_frames[i]["poster"].configure(image=poster,command=lambda m=movie: self.search_for_movie(m['title']))
            self.recommended_frames[i]["poster"].image = poster
            self.recommended_frames[i]["title"].configure(text=f"Title: {movie['title']}")
            self.recommended_frames[i]["genres"].configure(text=f"Genres: {movie['genres']}")
            self.recommended_frames[i]["vote_average"].configure(text=f"Rating: {movie['vote_average']}")
            self.recommended_frames[i]["overview"].configure(text=f"Overview: {movie['overview']}")





if __name__ == "__main__":
    app = MovieGUI()
    app.mainloop()

