import wikipedia
import requests
import json
from PIL import ImageTk, Image
import tkinter as tk
import urllib.request
import io
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(search_term):
   try:
      result = wikipedia.search(search_term, results=1)
      wikipedia.set_lang('en')
      wkpage = wikipedia.WikipediaPage(title=result[0])
      title = wkpage.title
      response = requests.get(WIKI_REQUEST + title)
      json_data = json.loads(response.text)
      img_link = list(json_data['query']['pages'].values())[0]['original']['source']
      return img_link        
   except:
      return 0

def display_image_from_url(url):
   root = tk.Tk()
   root.title("Displaying Images from URL in Tkinter")
   root.geometry("700x400")
   try:
      with urllib.request.urlopen(url) as u:
         raw_data = u.read()
   except Exception as e:
      print(f"Error fetching image: {e}")
      return

   try:
      image = Image.open(io.BytesIO(raw_data))
      img = image.resize((450, 350))
      photo = ImageTk.PhotoImage(img)
   except Exception as e:
      print(f"Error opening image: {e}")
      return

   label = tk.Label(root, image=photo)
   label.pack()
   root.mainloop()

def main():
   chunksize = 1000  # Adjust this according to your system's memory
   combined_features_list = []
   titles_list = []

   # Read CSV in chunks
   for chunk in pd.read_csv('movies.csv', chunksize=chunksize):
      chunk = chunk.fillna('')
      combined_features = chunk['genres'] + ' ' + chunk['overview'] + ' ' + chunk['production_companies'] + ' ' + chunk['release_date']
      combined_features_list.extend(combined_features)
      titles_list.extend(chunk['title'])

   vectorizer = TfidfVectorizer()
   feature_vectors = vectorizer.fit_transform(combined_features_list)
   feature_vectors = csr_matrix(feature_vectors)  # Convert to sparse matrix

   # movie_name = input("Enter your favorite movie: ")
   movie_name = "Robin Hood"

   close_match = difflib.get_close_matches(movie_name, titles_list, n=1)
   if not close_match:
      print("No match found")
      return

   index_of_movie_match = titles_list.index(close_match[0])
   similarity = cosine_similarity(feature_vectors[index_of_movie_match], feature_vectors)

   sim_score = list(enumerate(similarity[0]))
   sorted_similar_movies = sorted(sim_score, key=lambda x: x[1], reverse=True)

   print('Movies for you:')
   for i, movie in enumerate(sorted_similar_movies[:10], 1):
      index = movie[0]
      title_from_index = titles_list[index]
      print(f"{i}. {title_from_index}")

   wiki_image = get_wiki_image('Fox')
   display_image_from_url(wiki_image)

if __name__ == "__main__":
   main()
